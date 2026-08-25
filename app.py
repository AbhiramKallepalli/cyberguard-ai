from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, login_manager
from datetime import datetime
import os
import json
import ollama

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cyberguard-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cyberguard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

from models import User, Scan, FlaggedEvent, LLMResponse
from preprocessing import validate_and_preprocess
from model import run_scan

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def dashboard():
    scans = Scan.query.filter_by(
        user_id=current_user.id
    ).order_by(Scan.scanned_at.desc()).all()
    return render_template('dashboard.html', scans=scans)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please log in.')
            return redirect(url_for('login'))
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! Please log in.')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template('upload.html')

    if 'file' not in request.files:
        flash('No file selected.')
        return redirect(url_for('upload'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected.')
        return redirect(url_for('upload'))

    if not (file.filename.endswith('.csv') or file.filename.endswith('.txt')):
        flash('Only .csv or .txt files are accepted.')
        return redirect(url_for('upload'))

    # Validate and preprocess in memory
    try:
        df, row_count = validate_and_preprocess(file.stream, file.filename)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('upload'))

    # Save scan record to database
    scan = Scan(
        user_id=current_user.id,
        filename=secure_filename(file.filename),
        total_events=row_count,
        flagged_count=0
    )
    db.session.add(scan)
    db.session.commit()

    # Run the ML model on the preprocessed data
    try:
        flagged_events = run_scan(df)
    except Exception as e:
        flash(f'Scan failed: {str(e)}')
        return redirect(url_for('upload'))

    # Save each flagged event to the database
    for event in flagged_events:
        fe = FlaggedEvent(
            scan_id=scan.id,
            anomaly_score=event['anomaly_score'],
            risk_category=event['risk_category'],
            plain_english=event['plain_english'],
            top_factors=event['top_factors']
        )
        db.session.add(fe)

    # Update scan with final counts
    scan.flagged_count = len(flagged_events)
    db.session.commit()

    flash(f'Scan complete! {len(flagged_events)} suspicious events detected out of {row_count} records.')
    return redirect(url_for('scan_results', scan_id=scan.id))

@app.route('/scan/<int:scan_id>')
@login_required
def scan_results(scan_id):
    scan = Scan.query.get_or_404(scan_id)
    flagged_events = FlaggedEvent.query.filter_by(
        scan_id=scan_id
    ).order_by(FlaggedEvent.anomaly_score.asc()).all()
    return render_template(
        'scan_results.html',
        scan=scan,
        flagged_events=flagged_events
    )

@app.route('/event/<int:event_id>')
@login_required
def event_detail(event_id):
    event = FlaggedEvent.query.get_or_404(event_id)
    top_factors = event.top_factors.split(',') if event.top_factors else []
    llm_responses = LLMResponse.query.filter_by(event_id=event_id).all()
    return render_template(
        'event_detail.html',
        event=event,
        top_factors=top_factors,
        llm_responses=llm_responses
    )

@app.route('/ask/<int:event_id>', methods=['POST'])
@login_required
def ask_llm(event_id):
    event = FlaggedEvent.query.get_or_404(event_id)
    data = request.get_json()
    question = data.get('question', '').strip()

    if not question:
        return json.dumps({'error': 'No question provided'}), 400

    # Build structured prompt grounded in event data
    prompt = f"""You are a home network security assistant helping a non-technical homeowner.

Here is the network event you are explaining:
- Risk Level: {event.risk_category}
- Anomaly Score: {event.anomaly_score:.4f} (more negative = more suspicious)
- What happened: {event.plain_english}
- Top contributing factors: {event.top_factors}

The homeowner is asking: {question}

Give a clear, plain English answer in 2-3 sentences. Do not use technical jargon.
Reference the specific anomaly score and risk factors above in your answer.
Suggest one practical action the homeowner can take."""

    # Call Phi-3 Mini via Ollama
    try:
        response = ollama.chat(
            model='phi3:mini',
            messages=[{'role': 'user', 'content': prompt}]
        )
        answer = response['message']['content'].strip()
    except Exception as e:
        return json.dumps({'error': f'LLM error: {str(e)}'}), 500

    # Save Q&A to database
    llm_response = LLMResponse(
        event_id=event_id,
        question=question,
        response=answer
    )
    db.session.add(llm_response)
    db.session.commit()

    return json.dumps({'answer': answer})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)