import pandas as pd
import joblib
from flask import Flask, request, jsonify
from generator import create_diet_plan

app = Flask(__name__)

# --- Load Models and Databases ONCE at startup ---
try:
    print("Loading ML model...")
    MODEL = joblib.load('diet_model.pkl')
    print("Loading encoder...")
    DISEASE_ENCODER = joblib.load('disease_encoder.pkl')
    print("ML model and encoder loaded.")
except FileNotFoundError:
    print("ERROR: Model or encoder files not found. Run train_model.py first.")
    MODEL = None
    DISEASE_ENCODER = None

try:
    print("Loading food database...")
    FOOD_DB = pd.read_csv('foods.csv')
    print(f"Food database loaded with {len(FOOD_DB)} items.")
except FileNotFoundError:
    print("ERROR: foods.csv not found. Please create it.")
    FOOD_DB = None

# --- API Endpoint ---
@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    
    if MODEL is None or FOOD_DB is None or DISEASE_ENCODER is None:
        return jsonify({"error": "Server is not ready. Missing model or database."}), 500

    # 1. Get patient record from the API request
    patient_record = request.get_json()
    
    if not patient_record:
        return jsonify({"error": "No patient data provided"}), 400

    # Example input validation
    required_fields = ['age', 'bmi', 'disease', 'ses', 'allergies']
    if not all(field in patient_record for field in required_fields):
        return jsonify({"error": f"Missing required fields: {required_fields}"}), 400

    try:
        # 2. Use the ML Model to Predict Diet Type
        
        # A. Format the input for the model
        age = patient_record['age']
        bmi = patient_record['bmi']
        
        # B. Use the saved encoder to transform the disease name
        disease_name = patient_record['disease']
        disease_encoded = DISEASE_ENCODER.transform([disease_name])[0]
        
        # C. Create the feature vector
        model_input = [[age, bmi, disease_encoded]]
        
        # D. Predict!
        ml_target_diet = MODEL.predict(model_input)[0]
        print(f"ML Model prediction: {ml_target_diet}")

        # 3. Use the Generator to Build the Plan
        # It uses the full patient_record AND the ML prediction
        final_plan = create_diet_plan(
            patient_record=patient_record,
            ml_target_diet=ml_target_diet,
            food_db=FOOD_DB
        )
        
        # 4. Return the final plan
        response = {
            "patient_record": patient_record,
            "predicted_diet_goal": ml_target_diet,
            "weekly_plan": final_plan
        }
        return jsonify(response)

    except ValueError as ve:
        # This catches the error from the generator if no food is found
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        # Catch-all for other errors
        return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Set host='0.0.0.0' to make it accessible on your network
    app.run(debug=True, host='0.0.0.0', port=5001)