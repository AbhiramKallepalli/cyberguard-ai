# Scenario 3 — Unauthenticated Access

**Input:** Logged out, then manually navigated to 127.0.0.1:5000 (dashboard route) without authentication.

**Expected (per spec):** Redirect to login page, no data exposed.

**Actual:** Immediately redirected to /login?next=%2F with message "Please log in to access this page." No dashboard data, scan history, or user information was visible at any point.

**Result:** PASS — matches expected outcome exactly.