import pandas as pd
import random

def create_diet_plan(patient_record, ml_target_diet, food_db):
    """
    Main function to generate a diet plan.
    """
    
    # --- 1. Filter by Socio-Economic Status ---
    # The 'ses' in the patient record is 'low', 'medium', or 'high'
    ses_filter = patient_record['ses']
    
    # Include foods at the patient's cost tier or lower
    allowed_costs = ['low']
    if ses_filter == 'medium':
        allowed_costs.append('medium')
    elif ses_filter == 'high':
        allowed_costs.append('medium')
        allowed_costs.append('high')
        
    allowed_food = food_db[food_db['cost_tier'].isin(allowed_costs)].copy()

    # --- 2. Filter by Allergies ---
    allergies = patient_record.get('allergies', [])
    if allergies:
        for allergy in allergies:
            if allergy and allergy.strip():
                # Remove rows where the 'allergy_tags' column CONTAINS the allergy
                allowed_food = allowed_food[~allowed_food['allergy_tags'].str.contains(allergy, na=False)]

    # --- 3. Filter by Disease / Inflammation ---
    # We use the ML model's prediction
    # (e.g., "Low_Carb", "High_Iron", "anti_inflammatory")
    
    # Prioritize foods that match the ML target or patient goal
    patient_goal = patient_record.get('goal', '') # e.g., 'inflammation_reduction'
    
    # Create a priority score
    def calculate_score(row):
        score = 0
        tags = row['disease_tags']
        
        # --- THIS IS THE FIX ---
        # Check if tags is NaN (an empty cell) and replace with an empty string
        if pd.isna(tags):
            tags = ""
        # --- END OF FIX ---
            
        if ml_target_diet in tags:
            score += 2 # Strong match from ML
        if patient_goal in tags:
            score += 1 # Good match for patient goal
        return score

    allowed_food['priority'] = allowed_food.apply(calculate_score, axis=1)
    
    # Separate into high-priority and regular
    high_priority_food = allowed_food[allowed_food['priority'] > 0]
    regular_food = allowed_food[allowed_food['priority'] == 0]

    if high_priority_food.empty:
        print("Warning: No high-priority foods found. Using regular list.")
        high_priority_food = regular_food
        if regular_food.empty:
            raise ValueError("No food available for this patient's severe restrictions.")

    # --- 4. Build the 7-Day Plan ---
    # This is a simple heuristic (rule-based) assembler
    plan = {"monday": {}, "tuesday": {}, "wednesday": {}, 
            "thursday": {}, "friday": {}, "saturday": {}, "sunday": {}}
    
    meals = ["breakfast", "lunch", "dinner"]
    
    for day in plan:
        for meal in meals:
            # Pick 2 items for the meal
            # We use .sample() to pick random items from the filtered list
            # We prioritize the high_priority list
            if not high_priority_food.empty:
                item1 = high_priority_food.sample(1)['name'].values[0]
            else:
                item1 = regular_food.sample(1)['name'].values[0]

            if not regular_food.empty:
                item2 = regular_food.sample(1)['name'].values[0]
            else:
                item2 = high_priority_food.sample(1)['name'].values[0]

            plan[day][meal] = [item1, item2]

    return plan