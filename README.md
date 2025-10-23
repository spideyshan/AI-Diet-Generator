🤖 AI Personalized Diet Plan API This project is a Python-based API that generates personalized 7-day diet plans for patients.
It uses a hybrid approach:
A Machine Learning model (Random Forest) predicts the patient's primary dietary needs (e.g., "Low_Carb", "Low_Sodium") based on their health profile.
A Rule-Based Generator filters a large food database based on the patient's socio-economic status (cost), allergies, and the ML model's prediction to build a custom meal plan.
🏗 How It Works (Architecture) This system is a Hybrid Expert System that combines machine learning with a rule-based engine.
Patient Request (JSON): The user sends a POST request to the /generate_plan endpoint with the patient's data (age, BMI, disease, allergies, cost preference).
ML Classification (The "Brain"): The Flask app (app.py) loads the pre-trained ML model (diet_model.pkl) and the encoder (disease_encoder.pkl). It uses this model to predict the target diet type (e.g., "Low_Sodium") for the patient.
Rule-Based Generation (The "Engine"): The app then passes the patient's full record and the ML model's prediction to the generator.py script.
Food Filtering: The generator filters the foods.csv database in three stages:
Filters by Cost: Keeps only food marked low, medium, or high based on the patient's ses.
Filters by Allergy: Removes all food containing the patient's allergies.
Prioritizes by Health Goal: Scores the remaining food, giving preference to items that match the ML model's target (e.g., low_sodium).
Plan Assembly: The generator randomly assembles a 7-day plan from the remaining, approved food items and sends it back as a JSON response.
🗂 File Structure app.py: The main Flask server. It loads the ML model and foods.csv into memory, defines the /generate_plan API endpoint, and handles all web requests.
train_model.py: A one-time script used to train the ML model. It reads diet_recommendations_dataset.csv, trains a RandomForestClassifier, and saves the final diet_model.pkl and disease_encoder.pkl files.
generator.py: The core logic for building the diet plan. Its create_diet_plan() function performs all the filtering (cost, allergy) and assembly of the 7-day plan.
generate_foods.py: A utility script to auto-generate a large, 500-item foods.csv file for robust testing.
requirements.txt: A list of all Python libraries needed for the project (flask, pandas, scikit-learn, joblib).
diet_recommendations_dataset.csv: (Training Data) The dataset used to train the ML model. It connects patient profiles (age, BMI, disease) to a recommended diet.
foods.csv: (Application Data) The main "knowledge base" or "inventory" of all food items. Includes cost, nutrition, allergy tags, and disease tags.
diet_model.pkl: (Saved Model) The pre-trained ML model file, saved by train_model.py.
disease_encoder.pkl: (Saved Encoder) The pre-trained LabelEncoder file, which converts text diseases (like "Diabetes") into numbers for the model.
🚀 Getting Started: How to Run Follow these steps to set up and run the project on your local machine.
1. Clone the Repository Bash
git clone https://github.com/your-username/your-repo-name.git cd your-repo-name 2. Set Up a Virtual Environment It is highly recommended to use a virtual environment to manage dependencies.
On macOS / Linux:
Bash
Create the environment

python3 -m venv venv
Activate the environment

source venv/bin/activate On Windows (Command Prompt):
Bash
Create the environment

python -m venv venv
Activate the environment

.\venv\Scripts\activate 3. Install Dependencies Once your environment is active, install all the required libraries:
Bash
pip install -r requirements.txt 4. Prepare Your Data You need two data files:
diet_recommendations_dataset.csv: This file is required to train your model. Make sure it's in the project folder.
foods.csv: This file is your food database. If you don't have one, you can run the generator script to create a 500-item sample file:
Bash
python generate_foods.py 5. Train the ML Model You must run this script once before starting the server. It will create the diet_model.pkl and disease_encoder.pkl files.
Bash
python train_model.py You should see an output like: Starting model training... Model Accuracy: 100.00% Model and encoder saved as 'diet_model.pkl' and 'disease_encoder.pkl'
1. Run the Flask Server You are now ready to start the API!
Bash
flask run The server will start and be accessible at http://127.0.0.1:5000.
🧪 How to Test the API You can test the API using a tool like Postman, Insomnia, or curl from your terminal.
You must send a POST request to the http://127.0.0.1:5000/generate_plan endpoint with a JSON body.
Test with curl (macOS / Linux) Open a new terminal and run this command:
Bash
curl -X POST http://127.0.0.1:5000/generate_plan -H "Content-Type: application/json" -d '{ "age": 45, "bmi": 32, "disease": "Diabetes_Type_2", "ses": "low", "allergies": ["gluten"], "goal": "inflammation_reduction" }' Test with curl (Windows Command Prompt) Windows requires " to be escaped with a .
DOS
curl -X POST http://127.0.0.1:5000/generate_plan ^ -H "Content-Type: application/json" ^ -d "{ "age": 45, "bmi": 32, "disease": "Diabetes_Type_2", "ses": "low", "allergies": ["gluten"], "goal": "inflammation_reduction" }" ✅ Successful Response (HTTP 200) If it works, you will get a JSON response with your plan:
JSON
{ "patient_record": { "age": 45, "allergies": [ "gluten" ], "bmi": 32, "disease": "Diabetes_Type_2", "goal": "inflammation_reduction", "ses": "low" }, "predicted_diet_goal": "Low_Carb", "weekly_plan": { "friday": { "breakfast": [ "Oats", "Canned Black Beans" ], "dinner": [ "Canned Lentils", "Canned Black Beans" ], "lunch": [ "Canned Lentils", "Carrot" ] }, "monday": { ... }, "saturday": { ... }, "sunday": { ... }, "thursday": { ... }, "tuesday": { ... }, "wednesday": { ... } } } ❌ Error Response (HTTP 400) If your filters are too strict and no food is found, you will get this error:
JSON
{ "error": "No food available for this patient's severe restrictions." } 📊 Dataset Credits This project relies on open-source data. Full credit goes to the original creators.
Patient Training Data:
Kaggle: Diet Recommendations Dataset by Ziya
Food Database (Sources for foods.csv):
USDA FoodData Central: Used for foundational nutritional information.
Open Food Facts: Used for allergen and cost-related data.

Postman Testing:
<img width="1277" height="796" alt="Screenshot 2025-10-23 at 11 34 27 PM" src="https://github.com/user-attachments/assets/cc0243e6-9bb5-45a5-9655-5591ac8e7b6a" />

Breakdown of python program files:
Here's a breakdown of exactly how your generator.py program works.

Think of it as a smart filter or a funnel. It takes the entire list of foods from foods.csv and runs it through a series of rules to find only the items that are safe, affordable, and effective for that specific patient.

Here is the step-by-step logic of the create_diet_plan function:

1. Filtering by Socio-Economic Status (Affordability) 💰
Input: The patient's ses (e.g., "low", "med", or "high").

Action: The code checks this ses value and creates an allowed_costs list.

If ses is "low", the list is ['low'].

If ses is "med", the list is ['low', 'medium'].

If ses is "high", the list is ['low', 'medium', 'high'].

Result: It filters the food database, keeping only the foods whose cost_tier is in this allowed_costs list.

2. Filtering by Allergies (Safety) 🥜
Input: The patient's allergies list (e.g., ["gluten", "dairy"]).

Action: The code loops through each item in this list. For each allergy (like "gluten"), it finds every row in the allergy_tags column that contains the word "gluten" and removes that row.

Result: The list of foods gets smaller. Now, it only contains items that are affordable and safe for the patient (e.g., no gluten, no dairy).

3. Prioritizing by Health Goals (Effectiveness) ❤️‍🩹
Input: The ML model's prediction (e.g., "Low_Carb") and the patient's goal (e.g., "inflammation_reduction").

Action: The code looks at the disease_tags for every remaining food item and gives it a score:

+2 points if it matches the ML model's prediction (e.g., disease_tags contains "Low_Carb").

+1 point if it matches the patient's secondary goal (e.g., disease_tags contains "inflammation_reduction").

0 points if it matches neither.

Result: The code creates two new lists: a high_priority_food list (foods with a score > 0) and a regular_food list (foods with a score of 0). This ensures the diet plan will be built using the most effective foods first.

4. Assembling the 7-Day Plan (Generation) 🗓️
Input: The high_priority_food and regular_food lists.

Action: The code loops 7 times (for each day of the week) and 3 times per day (for breakfast, lunch, and dinner). In each meal, it does the following:

Tries to pick a random food from the high_priority_food list.

Picks a second random food from the regular_food list (to add variety).

If either list is empty, it just picks from the other list.

Result: It builds a 7-day, 3-meal-per-day plan (a dictionary) and sends it back as the final output.


The train_model.py script is a one-time-use program. Its only job is to create and save the "brain" (the ML model) that your Flask API will use.

It reads your patients.csv file, learns patterns from it, and saves those learned patterns into the diet_model.pkl file.

Here is how it works, step-by-step.

1. Load the Training Data 📚
Action: The script uses pandas.read_csv('patients.csv') to load your patient data into memory.

Result: You have a table (a DataFrame) with columns like age, bmi, disease, and Diet_Recommendation.

2. Preprocess the Data (The "Translator") 🔄
Problem: Machine learning models can't understand text like "Diabetes_Type_2" or "Hypertension". They only understand numbers.

Action: The script uses LabelEncoder to solve this. It creates a "translator" that converts the text in the disease column into numbers.

"Diabetes_Type_2" might become 0

"Hypertension" might become 1

"Anemia" might become 2

Result: A new column, disease_encoded, is created with these numbers. The script also saves this "translator" as disease_encoder.pkl so your Flask app can use it later to understand new patient inputs.

3. Define the Goal 🎯
Action: The script separates the data into two parts:

Features (X): The inputs or "questions." These are the age, bmi, and disease_encoded columns.

Target (y): The "answer" the model needs to learn. This is the Diet_Recommendation column (e.g., "Low_Carb").

4. Split the Data for Testing 📝
Problem: How do you know if your model is smart or just "memorized" the answers? You test it.

Action: The script uses train_test_split to divide the data.

Training Set (80%): The model gets to see this data to learn the patterns.

Testing Set (20%): This data is hidden from the model. It's used at the end for a "final exam" to see how accurate the model is on data it's never seen before.

5. Train the Model 🧠
Action: This is the most important line: model.fit(X_train, y_train).

You create a RandomForestClassifier, which is like a team of decision-makers.

The .fit() command tells the model to "learn" by looking at all the "questions" (X_train) and "answers" (y_train) in the training set.

Result: The model adjusts its internal logic to find the patterns that connect a patient's age, BMI, and disease to a specific diet recommendation.

6. Save the Final "Brain" 💾
Action: After training, the script uses joblib.dump(model, 'diet_model.pkl').

Result: It saves the fully trained, "smart" model object into a single file: diet_model.pkl.

This file is the final product. Your app.py loads this file to make predictions, so you never have to run the training script again (unless you get more patient data).


Only patients.csv is used for training the machine learning model.

patients.csv (Training Data): This file teaches the ML model (diet_model.pkl) to find patterns. It learns the rules (e.g., "a patient with diabetes needs a low-carb diet").
