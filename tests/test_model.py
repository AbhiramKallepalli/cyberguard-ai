import pickle
import numpy as np
import pytest
from sklearn.ensemble import IsolationForest


@pytest.fixture
def loaded_model():
    with open("outputs/model.pkl", "rb") as f:
        model = pickle.load(f)
    return model


def test_model_loads_successfully(loaded_model):
    assert loaded_model is not None
    assert isinstance(loaded_model, IsolationForest)


def test_model_has_expected_feature_count(loaded_model):
    assert loaded_model.n_features_in_ > 0


def test_model_predict_returns_scores(loaded_model):
    n_features = loaded_model.n_features_in_
    fake_data = np.random.rand(10, n_features)
    scores = loaded_model.decision_function(fake_data)
    assert len(scores) == 10
    assert isinstance(scores, np.ndarray)


def test_model_predict_labels_are_valid(loaded_model):
    n_features = loaded_model.n_features_in_
    fake_data = np.random.rand(10, n_features)
    labels = loaded_model.predict(fake_data)
    assert set(labels).issubset({-1, 1})


def test_model_scores_vary(loaded_model):
    n_features = loaded_model.n_features_in_
    fake_data = np.random.rand(50, n_features)
    scores = loaded_model.decision_function(fake_data)
    assert len(set(scores)) > 1