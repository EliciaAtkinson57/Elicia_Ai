"""
Nutrition planning and meal generation tools.
"""
import json
from typing import Dict, List, Any
import random


def generate_meal_plan(
    calories: float,
    protein_g: float,
    carbs_g: float,
    fat_g: float,
    meals_per_day: int = 3,
    dietary_preference: str = "balanced"
) -> Dict[str, Any]:
    """
    Generate a daily meal plan based on macronutrient targets.

    Args:
        calories: Daily calorie target
        protein_g: Daily protein target in grams
        carbs_g: Daily carbs target in grams
        fat_g: Daily fat target in grams
        meals_per_day: Number of meals (3-6)
        dietary_preference: balanced, high_protein, low_carb, vegetarian

    Returns:
        Dictionary with meal plan and nutritional breakdown
    """
    # Calculate per-meal macros
    cals_per_meal = calories / meals_per_day
    protein_per_meal = protein_g / meals_per_day
    carbs_per_meal = carbs_g / meals_per_day
    fat_per_meal = fat_g / meals_per_day

    meal_names = {
        3: ["Breakfast", "Lunch", "Dinner"],
        4: ["Breakfast", "Lunch", "Snack", "Dinner"],
        5: ["Breakfast", "Morning Snack", "Lunch", "Afternoon Snack", "Dinner"],
        6: ["Breakfast", "Morning Snack", "Lunch", "Afternoon Snack", "Dinner", "Evening Snack"]
    }

    meals = []
    for meal_name in meal_names.get(meals_per_day, meal_names[3]):
        meals.append({
            "meal": meal_name,
            "target_calories": round(cals_per_meal, 0),
            "target_macros": {
                "protein": round(protein_per_meal, 1),
                "carbs": round(carbs_per_meal, 1),
                "fat": round(fat_per_meal, 1)
            },
            "suggestions": _get_meal_suggestions(meal_name, dietary_preference)
        })

    return {
        "total_daily_targets": {
            "calories": calories,
            "protein_g": protein_g,
            "carbs_g": carbs_g,
            "fat_g": fat_g
        },
        "meals_per_day": meals_per_day,
        "dietary_preference": dietary_preference,
        "meals": meals,
        "hydration_reminder": "Drink 8-10 glasses of water throughout the day",
        "tips": [
            "Prep meals in advance for consistency",
            "Adjust portion sizes to hit your macros",
            "Include vegetables with every meal",
            "Choose whole food sources when possible"
        ]
    }


def _get_meal_suggestions(meal_name: str, dietary_preference: str) -> List[str]:
    """Helper function to get meal suggestions."""
    suggestions = {
        "Breakfast": [
            "Egg whites with oatmeal and berries",
            "Greek yogurt with granola and banana",
            "Whole grain toast with avocado and eggs",
            "Protein smoothie with oats and fruit",
            "Cottage cheese with nuts and honey"
        ],
        "Lunch": [
            "Grilled chicken breast with brown rice and vegetables",
            "Salmon with quinoa and asparagus",
            "Turkey wrap with whole wheat tortilla and salad",
            "Lean beef stir-fry with mixed vegetables",
            "Tuna salad with whole grain crackers"
        ],
        "Dinner": [
            "Baked chicken with sweet potato and broccoli",
            "Lean steak with quinoa and green beans",
            "Grilled fish with wild rice and roasted vegetables",
            "Turkey meatballs with pasta and marinara",
            "Shrimp with brown rice and stir-fried vegetables"
        ],
        "Snack": [
            "Protein shake",
            "Apple with almond butter",
            "Greek yogurt with berries",
            "Rice cakes with peanut butter",
            "Protein bar",
            "Mixed nuts and dried fruit"
        ],
        "Morning Snack": [
            "Protein shake",
            "Banana with peanut butter",
            "Hard-boiled eggs",
            "Greek yogurt"
        ],
        "Afternoon Snack": [
            "Protein bar",
            "Apple with almond butter",
            "Cottage cheese with fruit",
            "Hummus with vegetables"
        ],
        "Evening Snack": [
            "Casein protein shake",
            "Cottage cheese",
            "Greek yogurt",
            "Small portion of nuts"
        ]
    }

    return suggestions.get(meal_name, suggestions["Snack"])[:3]


def get_nutrition_info(food_item: str) -> Dict[str, Any]:
    """
    Get nutrition information for common foods.

    Args:
        food_item: Name of the food

    Returns:
        Nutrition information per 100g serving
    """
    # Common foods database (per 100g)
    nutrition_db = {
        "chicken breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
        "salmon": {"calories": 208, "protein": 20, "carbs": 0, "fat": 13},
        "egg": {"calories": 143, "protein": 13, "carbs": 1, "fat": 10},
        "greek yogurt": {"calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4},
        "oatmeal": {"calories": 389, "protein": 17, "carbs": 66, "fat": 7},
        "brown rice": {"calories": 370, "protein": 7.5, "carbs": 77, "fat": 2.9},
        "broccoli": {"calories": 34, "protein": 2.8, "carbs": 7, "fat": 0.4},
        "sweet potato": {"calories": 86, "protein": 1.6, "carbs": 20, "fat": 0.1},
        "banana": {"calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3},
        "almonds": {"calories": 579, "protein": 21, "carbs": 22, "fat": 50},
        "avocado": {"calories": 160, "protein": 2, "carbs": 9, "fat": 15},
        "quinoa": {"calories": 368, "protein": 14, "carbs": 64, "fat": 6},
        "tuna": {"calories": 130, "protein": 28, "carbs": 0, "fat": 1},
        "beef": {"calories": 250, "protein": 26, "carbs": 0, "fat": 15},
        "turkey": {"calories": 135, "protein": 30, "carbs": 0, "fat": 0.7},
        "cottage cheese": {"calories": 98, "protein": 11, "carbs": 3.4, "fat": 4.3},
        "milk": {"calories": 42, "protein": 3.4, "carbs": 5, "fat": 1},
        "apple": {"calories": 52, "protein": 0.3, "carbs": 14, "fat": 0.2},
        "peanut butter": {"calories": 588, "protein": 25, "carbs": 20, "fat": 50},
        "spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fat": 0.4},
        "pasta": {"calories": 371, "protein": 13, "carbs": 75, "fat": 1.5},
        "bread": {"calories": 265, "protein": 9, "carbs": 49, "fat": 3.2},
        "cheese": {"calories": 402, "protein": 25, "carbs": 1.3, "fat": 33}
    }

    food_lower = food_item.lower().strip()
    nutrition = nutrition_db.get(food_lower)

    if nutrition:
        return {
            "food": food_item.title(),
            "serving_size": "100g",
            "nutrition": nutrition,
            "found": True
        }
    else:
        return {
            "food": food_item,
            "found": False,
            "message": "Food not found in database. Try a more common food item or check spelling."
        }


def calculate_meal_macros(ingredients: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate total macros for a meal with multiple ingredients.

    Args:
        ingredients: List of dicts with 'food' and 'grams' keys

    Returns:
        Total nutrition for the meal
    """
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    ingredient_breakdown = []

    for ingredient in ingredients:
        food_name = ingredient.get("food", "")
        grams = ingredient.get("grams", 0)

        food_data = get_nutrition_info(food_name)

        if food_data.get("found"):
            nutrition = food_data["nutrition"]
            multiplier = grams / 100

            cals = nutrition["calories"] * multiplier
            protein = nutrition["protein"] * multiplier
            carbs = nutrition["carbs"] * multiplier
            fat = nutrition["fat"] * multiplier

            total_calories += cals
            total_protein += protein
            total_carbs += carbs
            total_fat += fat

            ingredient_breakdown.append({
                "food": food_name,
                "grams": grams,
                "calories": round(cals, 1),
                "protein": round(protein, 1),
                "carbs": round(carbs, 1),
                "fat": round(fat, 1)
            })

    return {
        "ingredients": ingredient_breakdown,
        "total": {
            "calories": round(total_calories, 1),
            "protein_g": round(total_protein, 1),
            "carbs_g": round(total_carbs, 1),
            "fat_g": round(total_fat, 1)
        }
    }


def get_healthy_alternatives(food_item: str) -> Dict[str, Any]:
    """
    Suggest healthier alternatives to common foods.

    Args:
        food_item: Food to find alternatives for

    Returns:
        Healthier alternatives with reasons
    """
    alternatives = {
        "white rice": {
            "alternatives": ["Brown rice", "Quinoa", "Cauliflower rice"],
            "reason": "Higher fiber, more nutrients, better for blood sugar"
        },
        "white bread": {
            "alternatives": ["Whole grain bread", "Ezekiel bread", "Oat bread"],
            "reason": "More fiber, slower digestion, more vitamins"
        },
        "pasta": {
            "alternatives": ["Whole wheat pasta", "Lentil pasta", "Zucchini noodles"],
            "reason": "Higher protein/fiber, lower calories"
        },
        "soda": {
            "alternatives": ["Sparkling water", "Green tea", "Water with lemon"],
            "reason": "Zero calories, no sugar, better hydration"
        },
        "chips": {
            "alternatives": ["Air-popped popcorn", "Veggie chips", "Rice cakes"],
            "reason": "Lower calories, less fat, more filling"
        },
        "ice cream": {
            "alternatives": ["Greek yogurt with fruit", "Protein ice cream", "Frozen banana"],
            "reason": "Higher protein, lower sugar, fewer calories"
        },
        "candy": {
            "alternatives": ["Dark chocolate", "Fruit", "Dates"],
            "reason": "Natural sugars, antioxidants, fiber"
        },
        "fried chicken": {
            "alternatives": ["Grilled chicken", "Baked chicken", "Air-fried chicken"],
            "reason": "Less fat, fewer calories, same protein"
        }
    }

    food_lower = food_item.lower().strip()
    alt_data = alternatives.get(food_lower)

    if alt_data:
        return {
            "original_food": food_item,
            "alternatives": alt_data["alternatives"],
            "reason": alt_data["reason"],
            "found": True
        }
    else:
        return {
            "original_food": food_item,
            "found": False,
            "message": "No specific alternatives in database. General tip: Choose whole foods over processed, grilled over fried."
        }
