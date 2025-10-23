import csv
import random

# Define the 8 columns you need
HEADER = ['name', 'cost_tier', 'calories_100g', 'protein_100g', 'carbs_100g', 'fat_100g', 'allergy_tags', 'disease_tags']

# --- Define Food Prototypes ---
# This ensures the data is realistic (e.g., vegetables are low-cal, meat is high-protein)
FOOD_CATEGORIES = {
    'vegetable': {
        'items': ['Broccoli', 'Spinach', 'Carrot', 'Bell Pepper', 'Zucchini', 'Onion', 'Garlic', 'Tomato', 'Cucumber', 'Lettuce', 'Kale', 'Cabbage', 'Cauliflower', 'Mushroom', 'Asparagus', 'Celery'],
        'nutrition': {'cal': (10, 60), 'pro': (1, 5), 'carb': (2, 12), 'fat': (0, 1)},
        'allergy': ['none'],
        'disease': ['anti_inflammatory', 'low_sodium', 'low_glycemic']
    },
    'fruit': {
        'items': ['Apple', 'Banana', 'Orange', 'Grapes', 'Strawberries', 'Blueberries', 'Avocado', 'Pineapple', 'Mango', 'Watermelon', 'Lemon', 'Lime', 'Peach', 'Pear'],
        'nutrition': {'cal': (40, 100), 'pro': (0, 2), 'carb': (10, 25), 'fat': (0, 3)},
        'allergy': ['none'],
        'disease': ['anti_inflammatory', 'low_glycemic']
    },
    'protein_meat': {
        'items': ['Chicken Breast', 'Ground Beef', 'Pork Chop', 'Turkey', 'Lamb', 'Steak', 'Sausage', 'Bacon'],
        'nutrition': {'cal': (120, 300), 'pro': (15, 30), 'carb': (0, 2), 'fat': (5, 25)},
        'allergy': ['none'],
        'disease': ['high_protein', 'high_iron']
    },
    'protein_fish': {
        'items': ['Salmon', 'Tuna', 'Cod', 'Tilapia', 'Shrimp', 'Sardines', 'Mackerel', 'Trout'],
        'nutrition': {'cal': (100, 250), 'pro': (18, 30), 'carb': (0, 1), 'fat': (2, 20)},
        'allergy': ['shellfish'], # Will apply to shrimp, but fine for this sim
        'disease': ['high_protein', 'omega_3', 'anti_inflammatory']
    },
    'protein_plant': {
        'items': ['Lentils', 'Black Beans', 'Chickpeas', 'Tofu', 'Tempeh', 'Edamame', 'Kidney Beans', 'Pinto Beans'],
        'nutrition': {'cal': (100, 180), 'pro': (8, 18), 'carb': (15, 30), 'fat': (1, 9)},
        'allergy': ['soy'], # For tofu/tempeh
        'disease': ['low_glycemic', 'diabetes_friendly', 'high_protein', 'high_iron']
    },
    'grain': {
        'items': ['White Rice', 'Brown Rice', 'Quinoa', 'Oats', 'Whole Wheat Bread', 'White Bread', 'Pasta', 'Barley', 'Couscous', 'Millet'],
        'nutrition': {'cal': (110, 390), 'pro': (2, 15), 'carb': (25, 80), 'fat': (1, 7)},
        'allergy': ['gluten'], # For wheat/barley
        'disease': ['low_glycemic', 'high_glycemic'] # Will be assigned
    },
    'dairy': {
        'items': ['Milk', 'Cheddar Cheese', 'Mozzarella Cheese', 'Greek Yogurt', 'Yogurt', 'Cottage Cheese', 'Butter'],
        'nutrition': {'cal': (40, 410), 'pro': (3, 25), 'carb': (3, 10), 'fat': (1, 35)},
        'allergy': ['dairy'],
        'disease': ['high_protein']
    },
    'fats_nuts': {
        'items': ['Almonds', 'Walnuts', 'Peanuts', 'Olive Oil', 'Coconut Oil', 'Flax Seeds', 'Chia Seeds', 'Cashews', 'Pistachios'],
        'nutrition': {'cal': (550, 900), 'pro': (5, 25), 'carb': (10, 30), 'fat': (45, 100)},
        'allergy': ['nuts'],
        'disease': ['anti_inflammatory', 'high_protein']
    }
}

def generate_foods(filename='foods.csv', num_items=500):
    """Generates a CSV file with realistic-ish food data."""
    
    print(f"Generating {num_items} food items for {filename}...")
    food_list = []
    
    for _ in range(num_items):
        # 1. Pick a random category and item
        cat_name, cat_data = random.choice(list(FOOD_CATEGORIES.items()))
        item_name = random.choice(cat_data['items'])
        
        # 2. Assign cost
        cost = random.choice(['low', 'medium', 'high'])
        
        # 3. Generate realistic nutrition
        n_range = cat_data['nutrition']
        calories = random.randint(n_range['cal'][0], n_range['cal'][1])
        protein = random.randint(n_range['pro'][0], n_range['pro'][1])
        carbs = random.randint(n_range['carb'][0], n_range['carb'][1])
        fat = random.randint(n_range['fat'][0], n_range['fat'][1])
        
        # 4. Assign tags
        allergy_tags = list(cat_data['allergy'])
        disease_tags = list(cat_data['disease'])
        
        # 5. Add specific tags based on name (to refine the data)
        if 'Bread' in item_name or 'Pasta' in item_name or 'Barley' in item_name or 'Couscous' in item_name:
            allergy_tags = ['gluten']
        if 'White Rice' in item_name or 'White Bread' in item_name:
            disease_tags = ['high_glycemic']
        if 'Brown Rice' in item_name or 'Oats' in item_name or 'Quinoa' in item_name:
            disease_tags = ['low_glycemic', 'diabetes_friendly']
            allergy_tags = ['none']
            
        if 'Tofu' in item_name or 'Tempeh' in item_name or 'Edamame' in item_name:
            allergy_tags = ['soy']
        
        if 'Almonds' in item_name or 'Walnuts' in item_name or 'Peanuts' in item_name or 'Cashews' in item_name or 'Pistachios' in item_name:
            allergy_tags = ['nuts']
            
        if 'Shrimp' in item_name:
            allergy_tags = ['shellfish']

        # 6. Add cost variations
        if cost == 'low':
            # Add a 'Canned' prefix
            if cat_name in ['vegetable', 'fruit', 'protein_plant', 'protein_fish']:
                item_name = f"Canned {item_name}"
                if 'low_sodium' in disease_tags:
                    disease_tags.remove('low_sodium') # Canned is not low sodium
        
        if cost == 'high':
            if cat_name in ['vegetable', 'fruit', 'protein_meat']:
                item_name = f"Organic {item_name}"
        
        # 7. Format tags as strings
        allergy_str = ';'.join(list(set(allergy_tags))) # Use set to remove duplicates
        disease_str = ';'.join(list(set(disease_tags)))
        
        # 8. Add to our list
        food_list.append([
            item_name, cost, calories, protein, carbs, fat, allergy_str, disease_str
        ])

    # 9. Write all data to the CSV file
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(HEADER) # Write the header row
            writer.writerows(food_list) # Write all 500 food rows
            
        print(f"--- SUCCESS! ---")
        print(f"Created {filename} with {len(food_list)} items.")
    
    except PermissionError:
        print("\n--- ERROR! ---")
        print(f"Could not write to {filename}. Is the file open in another program (like Excel)?")
    except Exception as e:
        print(f"\nAn unknown error occurred: {e}")

# --- Run the script ---
if __name__ == "__main__":
    generate_foods(filename='foods.csv', num_items=500)