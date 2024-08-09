from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load the models and other necessary files
rf_model = joblib.load('random_forest_model.pkl')
gb_model = joblib.load('gradient_boosting_model.pkl')
xgb_model = joblib.load('xgboost_model.pkl')
scaler = joblib.load('scaler_minmax.pkl')  # Assuming you are using MinMaxScaler
label_encoder = joblib.load('label_encoder.pkl')

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get data from form
        nitrogen = float(request.form['Nitrogen'])
        phosphorus = float(request.form['Phosporus'])
        potassium = float(request.form['Potassium'])
        temperature = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['Ph'])
        rainfall = float(request.form['Rainfall'])
        
        # Prepare input data
        features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
        features_scaled = scaler.transform(features)
        
        # Predict using one of the models (e.g., Random Forest)
        prediction = rf_model.predict(features_scaled)
        crop = label_encoder.inverse_transform(prediction)[0]
        
        return render_template('index.html', result=crop)

if __name__ == '__main__':
    app.run(debug=True)
