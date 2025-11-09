"""
Tool registry for OpenAI function calling.
Defines all available tools and maps them to their implementations.
"""
import json
from typing import Dict, Any, Callable
from tools.fitness_calc import (
    calculate_bmi,
    calculate_tdee,
    calculate_macros,
    calculate_one_rep_max,
    calculate_body_fat_navy,
    calculate_heart_rate_zones,
    calculate_hydration
)
from tools.workout_tools import (
    generate_workout,
    get_exercise_recommendations,
    calculate_progressive_overload
)
from tools.nutrition_tools import (
    generate_meal_plan,
    get_nutrition_info,
    calculate_meal_macros,
    get_healthy_alternatives
)


# OpenAI function definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_bmi",
            "description": "Calculate Body Mass Index (BMI) and provide health assessment with recommendations",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight_kg": {
                        "type": "number",
                        "description": "Weight in kilograms"
                    },
                    "height_cm": {
                        "type": "number",
                        "description": "Height in centimeters"
                    }
                },
                "required": ["weight_kg", "height_cm"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_tdee",
            "description": "Calculate Total Daily Energy Expenditure (TDEE) and daily calorie needs based on activity level",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight_kg": {"type": "number", "description": "Weight in kilograms"},
                    "height_cm": {"type": "number", "description": "Height in centimeters"},
                    "age": {"type": "integer", "description": "Age in years"},
                    "gender": {"type": "string", "enum": ["male", "female"], "description": "Gender"},
                    "activity_level": {
                        "type": "string",
                        "enum": ["sedentary", "light", "moderate", "active", "very_active"],
                        "description": "Physical activity level"
                    }
                },
                "required": ["weight_kg", "height_cm", "age", "gender", "activity_level"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_macros",
            "description": "Calculate macronutrient distribution (protein, carbs, fat) based on calorie goal and fitness objective",
            "parameters": {
                "type": "object",
                "properties": {
                    "calories": {"type": "number", "description": "Daily calorie target"},
                    "goal": {
                        "type": "string",
                        "enum": ["muscle_gain", "fat_loss", "maintenance"],
                        "description": "Fitness goal"
                    },
                    "weight_kg": {"type": "number", "description": "Body weight in kg"}
                },
                "required": ["calories", "goal", "weight_kg"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_one_rep_max",
            "description": "Calculate one rep max (1RM) and training zone recommendations for strength training",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight": {"type": "number", "description": "Weight lifted"},
                    "reps": {"type": "integer", "description": "Number of repetitions performed"}
                },
                "required": ["weight", "reps"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_body_fat_navy",
            "description": "Estimate body fat percentage using US Navy method based on body measurements",
            "parameters": {
                "type": "object",
                "properties": {
                    "gender": {"type": "string", "enum": ["male", "female"]},
                    "waist_cm": {"type": "number", "description": "Waist circumference in cm"},
                    "neck_cm": {"type": "number", "description": "Neck circumference in cm"},
                    "height_cm": {"type": "number", "description": "Height in cm"},
                    "hip_cm": {"type": "number", "description": "Hip circumference in cm (required for females)"}
                },
                "required": ["gender", "waist_cm", "neck_cm", "height_cm"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_heart_rate_zones",
            "description": "Calculate heart rate training zones for cardio workouts",
            "parameters": {
                "type": "object",
                "properties": {
                    "age": {"type": "integer", "description": "Age in years"}
                },
                "required": ["age"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_hydration",
            "description": "Calculate daily water intake recommendations based on weight and activity",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight_kg": {"type": "number", "description": "Body weight in kg"},
                    "activity_level": {
                        "type": "string",
                        "enum": ["sedentary", "moderate", "active"],
                        "description": "Activity level"
                    }
                },
                "required": ["weight_kg"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_workout",
            "description": "Generate a personalized workout plan based on goals, experience level, and available equipment",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal": {
                        "type": "string",
                        "enum": ["muscle_gain", "strength", "fat_loss", "endurance", "general_fitness"],
                        "description": "Primary fitness goal"
                    },
                    "level": {
                        "type": "string",
                        "enum": ["beginner", "intermediate", "advanced"],
                        "description": "Experience level"
                    },
                    "days_per_week": {
                        "type": "integer",
                        "description": "Number of workout days per week (3-6)",
                        "minimum": 3,
                        "maximum": 6
                    },
                    "equipment": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Available equipment (e.g., dumbbells, barbell, bodyweight, cables, machine)"
                    },
                    "duration_minutes": {
                        "type": "integer",
                        "description": "Target workout duration in minutes"
                    }
                },
                "required": ["goal", "level", "days_per_week", "equipment"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_exercise_recommendations",
            "description": "Get exercise recommendations for specific muscle groups with equipment and experience level",
            "parameters": {
                "type": "object",
                "properties": {
                    "muscle_group": {
                        "type": "string",
                        "enum": ["chest", "back", "legs", "shoulders", "arms", "core"],
                        "description": "Target muscle group"
                    },
                    "equipment": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Available equipment"
                    },
                    "level": {
                        "type": "string",
                        "enum": ["beginner", "intermediate", "advanced"],
                        "description": "Experience level"
                    }
                },
                "required": ["muscle_group", "equipment", "level"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_progressive_overload",
            "description": "Calculate how to progress in strength training with progressive overload",
            "parameters": {
                "type": "object",
                "properties": {
                    "current_weight": {"type": "number", "description": "Current working weight"},
                    "current_reps": {"type": "integer", "description": "Current reps performed"},
                    "target_reps": {"type": "integer", "description": "Target rep range (upper limit)"},
                    "progression_type": {
                        "type": "string",
                        "enum": ["weight", "reps", "both"],
                        "description": "Type of progression"
                    }
                },
                "required": ["current_weight", "current_reps", "target_reps"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_meal_plan",
            "description": "Generate a daily meal plan based on macronutrient targets and dietary preferences",
            "parameters": {
                "type": "object",
                "properties": {
                    "calories": {"type": "number", "description": "Daily calorie target"},
                    "protein_g": {"type": "number", "description": "Daily protein target in grams"},
                    "carbs_g": {"type": "number", "description": "Daily carbs target in grams"},
                    "fat_g": {"type": "number", "description": "Daily fat target in grams"},
                    "meals_per_day": {
                        "type": "integer",
                        "description": "Number of meals per day (3-6)",
                        "minimum": 3,
                        "maximum": 6
                    },
                    "dietary_preference": {
                        "type": "string",
                        "enum": ["balanced", "high_protein", "low_carb", "vegetarian"],
                        "description": "Dietary preference"
                    }
                },
                "required": ["calories", "protein_g", "carbs_g", "fat_g"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_nutrition_info",
            "description": "Get detailed nutrition information for common foods",
            "parameters": {
                "type": "object",
                "properties": {
                    "food_item": {"type": "string", "description": "Name of the food item"}
                },
                "required": ["food_item"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_healthy_alternatives",
            "description": "Get healthier alternatives to common foods with explanations",
            "parameters": {
                "type": "object",
                "properties": {
                    "food_item": {"type": "string", "description": "Food to find alternatives for"}
                },
                "required": ["food_item"]
            }
        }
    }
]


# Function mapping
FUNCTION_MAP: Dict[str, Callable] = {
    "calculate_bmi": calculate_bmi,
    "calculate_tdee": calculate_tdee,
    "calculate_macros": calculate_macros,
    "calculate_one_rep_max": calculate_one_rep_max,
    "calculate_body_fat_navy": calculate_body_fat_navy,
    "calculate_heart_rate_zones": calculate_heart_rate_zones,
    "calculate_hydration": calculate_hydration,
    "generate_workout": generate_workout,
    "get_exercise_recommendations": get_exercise_recommendations,
    "calculate_progressive_overload": calculate_progressive_overload,
    "generate_meal_plan": generate_meal_plan,
    "get_nutrition_info": get_nutrition_info,
    "get_healthy_alternatives": get_healthy_alternatives
}


def execute_function(function_name: str, arguments: Dict[str, Any]) -> Any:
    """
    Execute a function by name with given arguments.

    Args:
        function_name: Name of the function to execute
        arguments: Dictionary of arguments to pass to the function

    Returns:
        Result from the function execution
    """
    func = FUNCTION_MAP.get(function_name)
    if func:
        try:
            return func(**arguments)
        except Exception as e:
            return {"error": f"Function execution failed: {str(e)}"}
    else:
        return {"error": f"Function '{function_name}' not found"}
