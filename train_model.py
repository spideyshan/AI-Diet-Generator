import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

print("Starting model training...")

# 1. Load data
try:
    # This line is correct
    data = pd.read_csv('diet_recommendations_dataset.csv')
except FileNotFoundError:
    # You can update this error message to be more accurate
    print("Error: diet_recommendations_dataset.csv not found.")
    exit()

# 2. Preprocess Data
# Convert categorical data (disease) into numbers
le_disease = LabelEncoder()

# --- FIX 1 ---
# Use the correct column name 'Disease_Type' from your CSV file
data['disease_encoded'] = le_disease.fit_transform(data['Disease_Type'])

# Define features (X) and target (y)
# --- FIX 2 ---
# Use the *new* numeric column 'disease_encoded' for training, not the text one
features = ['Age', 'BMI', 'disease_encoded']
target = 'Diet_Recommendation'

# This line has a typo in your original file. 
# Make sure your CSV has 'Age' and 'BMI' (capitalized) or fix them here.
X = data[features] 
y = data[target]

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the Model
# A Random Forest is a great choice for this
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Check accuracy (optional, but good practice)
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# 6. Save the Model
# We also save the 'encoder' to use in the API
joblib.dump(model, 'diet_model.pkl')
joblib.dump(le_disease, 'disease_encoder.pkl')

print("Model and encoder saved as 'diet_model.pkl' and 'disease_encoder.pkl'")