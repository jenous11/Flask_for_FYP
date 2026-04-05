# Cyberbullying Detection - Flask API

A REST API built with Flask that serves a trained SVM model for cyberbullying text classification.

## What it does
- Accepts POST requests with text input
- Returns prediction: "Cyberbullying" or "Not Cyberbullying"
- Model trained on Kaggle cyberbullying dataset

## Tech Stack
- Python, Flask, Scikit-learn, Joblib

## How to run
1. Install dependencies: `pip install flask scikit-learn joblib nltk`
2. Run: `python app.py`
3. API runs on `http://127.0.0.1:5000`

## Endpoint
POST `/predict`
Body: `{"prediction": "your text here"}`
Response: `{"result": "Cyberbullying"}`
