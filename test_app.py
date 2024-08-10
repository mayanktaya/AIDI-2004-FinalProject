# tests/test_app.py

import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test the index page"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Crop Recommendation System" in response.data  # Checking for title in index.html

def test_predict(client):
    """Test the predict functionality with specific input values"""
    response = client.post('/predict', data={
        'Nitrogen': '67',
        'Phosporus': '58',
        'Potassium': '39',
        'Temperature': '25',
        'Humidity': '80',
        'Ph': '5',
        'Rainfall': '220'
    })
    assert response.status_code == 200
    assert b"Recommended Crop for cultivation is:" in response.data  # Check for the result section title
    assert b"Apple" in response.data  # Expected output from the model