"""
Fitness calculation tools for health and fitness metrics.
"""
import json
from typing import Dict, Any


def calculate_bmi(weight_kg: float, height_cm: float) -> Dict[str, Any]:
    """
    Calculate Body Mass Index (BMI).

    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters

    Returns:
        Dictionary with BMI value, category, and health recommendations
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    # Determine category
    if bmi < 18.5:
        category = "Underweight"
        health_status = "Below healthy weight range"
        recommendation = "Consider consulting a nutritionist to develop a healthy weight gain plan with nutrient-dense foods."
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
        health_status = "Healthy weight range"
        recommendation = "Maintain your current weight through balanced nutrition and regular physical activity."
    elif 25 <= bmi < 30:
        category = "Overweight"
        health_status = "Above healthy weight range"
        recommendation = "Consider a balanced diet and regular exercise. Aim for 150+ minutes of moderate activity per week."
    else:
        category = "Obese"
        health_status = "Significantly above healthy weight range"
        recommendation = "Consult with healthcare professionals for a comprehensive weight management plan."

    return {
        "bmi": round(bmi, 1),
        "category": category,
        "health_status": health_status,
        "recommendation": recommendation,
        "weight_kg": weight_kg,
        "height_cm": height_cm
    }


def calculate_tdee(
    weight_kg: float,
    height_cm: float,
    age: int,
    gender: str,
    activity_level: str
) -> Dict[str, Any]:
    """
    Calculate Total Daily Energy Expenditure (TDEE).

    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        age: Age in years
        gender: 'male' or 'female'
        activity_level: sedentary, light, moderate, active, very_active

    Returns:
        Dictionary with BMR, TDEE, and calorie recommendations for different goals
    """
    # Calculate BMR using Mifflin-St Jeor Equation
    if gender.lower() == "male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    # Activity multipliers
    activity_multipliers = {
        "sedentary": 1.2,      # Little or no exercise
        "light": 1.375,        # Light exercise 1-3 days/week
        "moderate": 1.55,      # Moderate exercise 3-5 days/week
        "active": 1.725,       # Heavy exercise 6-7 days/week
        "very_active": 1.9     # Very heavy exercise, physical job
    }

    multiplier = activity_multipliers.get(activity_level.lower(), 1.2)
    tdee = bmr * multiplier

    return {
        "bmr": round(bmr, 0),
        "tdee": round(tdee, 0),
        "maintenance_calories": round(tdee, 0),
        "weight_loss": {
            "mild": round(tdee - 250, 0),  # 0.25kg per week
            "moderate": round(tdee - 500, 0),  # 0.5kg per week
            "aggressive": round(tdee - 750, 0)  # 0.75kg per week
        },
        "weight_gain": {
            "lean": round(tdee + 200, 0),  # Lean muscle gain
            "moderate": round(tdee + 350, 0),  # Balanced gain
            "bulk": round(tdee + 500, 0)  # Faster muscle gain
        },
        "activity_level": activity_level
    }


def calculate_macros(
    calories: float,
    goal: str,
    weight_kg: float
) -> Dict[str, Any]:
    """
    Calculate macronutrient distribution.

    Args:
        calories: Daily calorie target
        goal: muscle_gain, fat_loss, or maintenance
        weight_kg: Body weight in kg

    Returns:
        Dictionary with protein, carbs, and fat in grams and percentages
    """
    if goal == "muscle_gain":
        # High protein, moderate carbs, moderate fat
        protein_ratio = 0.30
        carb_ratio = 0.45
        fat_ratio = 0.25
        protein_per_kg = 2.2  # grams per kg bodyweight
    elif goal == "fat_loss":
        # High protein, moderate carbs, moderate fat
        protein_ratio = 0.40
        carb_ratio = 0.30
        fat_ratio = 0.30
        protein_per_kg = 2.4  # Higher protein for muscle preservation
    else:  # maintenance
        protein_ratio = 0.30
        carb_ratio = 0.40
        fat_ratio = 0.30
        protein_per_kg = 1.8

    # Calculate based on bodyweight (more accurate for protein)
    protein_g = weight_kg * protein_per_kg
    protein_calories = protein_g * 4

    # Adjust if protein calories exceed ratio significantly
    if protein_calories > calories * (protein_ratio + 0.1):
        protein_g = (calories * protein_ratio) / 4
        protein_calories = protein_g * 4

    # Calculate remaining calories for carbs and fats
    remaining_calories = calories - protein_calories
    carb_calories = remaining_calories * (carb_ratio / (carb_ratio + fat_ratio))
    fat_calories = remaining_calories - carb_calories

    carbs_g = carb_calories / 4
    fat_g = fat_calories / 9

    return {
        "calories": round(calories, 0),
        "protein": {
            "grams": round(protein_g, 1),
            "calories": round(protein_calories, 0),
            "percentage": round((protein_calories / calories) * 100, 1)
        },
        "carbs": {
            "grams": round(carbs_g, 1),
            "calories": round(carb_calories, 0),
            "percentage": round((carb_calories / calories) * 100, 1)
        },
        "fat": {
            "grams": round(fat_g, 1),
            "calories": round(fat_calories, 0),
            "percentage": round((fat_calories / calories) * 100, 1)
        },
        "goal": goal
    }


def calculate_one_rep_max(weight: float, reps: int) -> Dict[str, Any]:
    """
    Calculate one rep max using Epley formula.

    Args:
        weight: Weight lifted
        reps: Number of repetitions

    Returns:
        Dictionary with 1RM and training zone percentages
    """
    if reps == 1:
        one_rm = weight
    else:
        # Epley formula
        one_rm = weight * (1 + reps / 30)

    return {
        "one_rep_max": round(one_rm, 1),
        "training_zones": {
            "strength": {
                "percentage": "80-95%",
                "weight_range": f"{round(one_rm * 0.80, 1)}-{round(one_rm * 0.95, 1)}",
                "reps": "1-5",
                "purpose": "Maximum strength development"
            },
            "hypertrophy": {
                "percentage": "65-85%",
                "weight_range": f"{round(one_rm * 0.65, 1)}-{round(one_rm * 0.85, 1)}",
                "reps": "6-12",
                "purpose": "Muscle growth"
            },
            "endurance": {
                "percentage": "50-70%",
                "weight_range": f"{round(one_rm * 0.50, 1)}-{round(one_rm * 0.70, 1)}",
                "reps": "12-20+",
                "purpose": "Muscular endurance"
            }
        }
    }


def calculate_body_fat_navy(
    gender: str,
    waist_cm: float,
    neck_cm: float,
    height_cm: float,
    hip_cm: float = None
) -> Dict[str, Any]:
    """
    Calculate body fat percentage using US Navy method.

    Args:
        gender: 'male' or 'female'
        waist_cm: Waist circumference in cm
        neck_cm: Neck circumference in cm
        height_cm: Height in cm
        hip_cm: Hip circumference in cm (required for females)

    Returns:
        Dictionary with body fat percentage and category
    """
    if gender.lower() == "male":
        body_fat = (495 / (1.0324 - 0.19077 * (waist_cm - neck_cm) / 2.54 + 0.15456 * height_cm / 2.54)) - 450
    else:
        if hip_cm is None:
            return {"error": "Hip measurement required for females"}
        body_fat = (495 / (1.29579 - 0.35004 * (waist_cm + hip_cm - neck_cm) / 2.54 + 0.22100 * height_cm / 2.54)) - 450

    # Determine category
    if gender.lower() == "male":
        if body_fat < 6:
            category = "Essential fat"
        elif 6 <= body_fat < 14:
            category = "Athletes"
        elif 14 <= body_fat < 18:
            category = "Fitness"
        elif 18 <= body_fat < 25:
            category = "Average"
        else:
            category = "Obese"
    else:
        if body_fat < 14:
            category = "Essential fat"
        elif 14 <= body_fat < 21:
            category = "Athletes"
        elif 21 <= body_fat < 25:
            category = "Fitness"
        elif 25 <= body_fat < 32:
            category = "Average"
        else:
            category = "Obese"

    return {
        "body_fat_percentage": round(body_fat, 1),
        "category": category,
        "gender": gender
    }


def calculate_heart_rate_zones(age: int) -> Dict[str, Any]:
    """
    Calculate heart rate training zones.

    Args:
        age: Age in years

    Returns:
        Dictionary with max heart rate and training zones
    """
    max_hr = 220 - age

    return {
        "max_heart_rate": max_hr,
        "resting_recommendation": "60-100 bpm for adults",
        "training_zones": {
            "zone_1_recovery": {
                "percentage": "50-60%",
                "heart_rate": f"{round(max_hr * 0.50)}-{round(max_hr * 0.60)} bpm",
                "purpose": "Warm-up, cool-down, recovery",
                "intensity": "Very light"
            },
            "zone_2_fat_burn": {
                "percentage": "60-70%",
                "heart_rate": f"{round(max_hr * 0.60)}-{round(max_hr * 0.70)} bpm",
                "purpose": "Fat burning, base fitness",
                "intensity": "Light"
            },
            "zone_3_aerobic": {
                "percentage": "70-80%",
                "heart_rate": f"{round(max_hr * 0.70)}-{round(max_hr * 0.80)} bpm",
                "purpose": "Aerobic fitness, endurance",
                "intensity": "Moderate"
            },
            "zone_4_anaerobic": {
                "percentage": "80-90%",
                "heart_rate": f"{round(max_hr * 0.80)}-{round(max_hr * 0.90)} bpm",
                "purpose": "Performance, speed, power",
                "intensity": "Hard"
            },
            "zone_5_max": {
                "percentage": "90-100%",
                "heart_rate": f"{round(max_hr * 0.90)}-{max_hr} bpm",
                "purpose": "Maximum effort, sprints",
                "intensity": "Maximum"
            }
        }
    }


def calculate_hydration(weight_kg: float, activity_level: str = "moderate") -> Dict[str, Any]:
    """
    Calculate daily water intake recommendation.

    Args:
        weight_kg: Body weight in kg
        activity_level: sedentary, moderate, active

    Returns:
        Dictionary with water intake recommendations
    """
    # Base calculation: 30-35ml per kg
    base_ml = weight_kg * 33

    # Activity multipliers
    if activity_level.lower() == "sedentary":
        total_ml = base_ml
    elif activity_level.lower() == "moderate":
        total_ml = base_ml * 1.2
    else:  # active
        total_ml = base_ml * 1.5

    liters = total_ml / 1000
    oz = total_ml / 29.5735  # fluid ounces
    cups = oz / 8

    return {
        "daily_intake": {
            "liters": round(liters, 1),
            "ml": round(total_ml, 0),
            "oz": round(oz, 0),
            "cups": round(cups, 1)
        },
        "tips": [
            "Drink a glass of water upon waking",
            "Have water before each meal",
            "Carry a reusable water bottle",
            "Increase intake during exercise and hot weather",
            "Monitor urine color (pale yellow is ideal)"
        ]
    }
