"""
Workout generation and exercise tools.
"""
import json
import random
from typing import Dict, List, Any


def generate_workout(
    goal: str,
    level: str,
    days_per_week: int,
    equipment: List[str],
    duration_minutes: int = 60
) -> Dict[str, Any]:
    """
    Generate a personalized workout plan.

    Args:
        goal: muscle_gain, strength, fat_loss, endurance, general_fitness
        level: beginner, intermediate, advanced
        days_per_week: Number of workout days (3-6)
        equipment: List of available equipment
        duration_minutes: Target workout duration

    Returns:
        Dictionary with complete workout plan
    """
    # Define workout splits based on days
    if days_per_week == 3:
        split = "Full Body (3x/week)"
        routine = ["Full Body A", "Full Body B", "Full Body C"]
    elif days_per_week == 4:
        split = "Upper/Lower Split"
        routine = ["Upper Body A", "Lower Body A", "Upper Body B", "Lower Body B"]
    elif days_per_week == 5:
        split = "Push/Pull/Legs"
        routine = ["Push Day", "Pull Day", "Legs", "Push Day", "Pull Day"]
    else:  # 6 days
        split = "Push/Pull/Legs (2x/week)"
        routine = ["Push", "Pull", "Legs", "Push", "Pull", "Legs"]

    # Determine sets and reps based on goal
    if goal == "strength":
        sets_reps = "4-5 sets of 3-6 reps"
        rest = "3-5 minutes"
    elif goal == "muscle_gain":
        sets_reps = "3-4 sets of 8-12 reps"
        rest = "60-90 seconds"
    elif goal == "endurance":
        sets_reps = "2-3 sets of 15-20 reps"
        rest = "30-45 seconds"
    elif goal == "fat_loss":
        sets_reps = "3 sets of 12-15 reps"
        rest = "45-60 seconds"
    else:  # general_fitness
        sets_reps = "3 sets of 10-12 reps"
        rest = "60 seconds"

    return {
        "split": split,
        "days_per_week": days_per_week,
        "routine": routine,
        "goal": goal,
        "level": level,
        "sets_reps_guideline": sets_reps,
        "rest_periods": rest,
        "duration_minutes": duration_minutes,
        "equipment": equipment,
        "workout_structure": {
            "warm_up": "5-10 minutes of light cardio and dynamic stretching",
            "main_workout": f"{duration_minutes - 15} minutes",
            "cool_down": "5 minutes of stretching"
        },
        "tips": [
            "Progressive overload: Gradually increase weight or reps each week",
            "Maintain proper form over heavy weight",
            "Stay hydrated throughout your workout",
            f"Rest {rest} between sets",
            "Track your progress in a workout journal"
        ]
    }


def get_exercise_recommendations(
    muscle_group: str,
    equipment: List[str],
    level: str = "intermediate"
) -> Dict[str, Any]:
    """
    Get exercise recommendations for a specific muscle group.

    Args:
        muscle_group: chest, back, legs, shoulders, arms, core, full_body
        equipment: Available equipment
        level: beginner, intermediate, advanced

    Returns:
        Dictionary with recommended exercises
    """
    # Comprehensive exercise database
    exercises = {
        "chest": {
            "beginner": [
                {"name": "Push-ups", "equipment": "bodyweight", "sets": "3", "reps": "8-12"},
                {"name": "Incline Push-ups", "equipment": "bodyweight", "sets": "3", "reps": "10-15"},
                {"name": "Dumbbell Bench Press", "equipment": "dumbbells", "sets": "3", "reps": "8-12"},
                {"name": "Dumbbell Flyes", "equipment": "dumbbells", "sets": "3", "reps": "10-12"}
            ],
            "intermediate": [
                {"name": "Barbell Bench Press", "equipment": "barbell", "sets": "4", "reps": "8-10"},
                {"name": "Incline Dumbbell Press", "equipment": "dumbbells", "sets": "3", "reps": "8-12"},
                {"name": "Cable Flyes", "equipment": "cables", "sets": "3", "reps": "12-15"},
                {"name": "Dips", "equipment": "bodyweight", "sets": "3", "reps": "8-12"}
            ],
            "advanced": [
                {"name": "Barbell Bench Press", "equipment": "barbell", "sets": "5", "reps": "5-8"},
                {"name": "Incline Barbell Press", "equipment": "barbell", "sets": "4", "reps": "8-10"},
                {"name": "Weighted Dips", "equipment": "bodyweight", "sets": "4", "reps": "6-10"},
                {"name": "Cable Crossovers", "equipment": "cables", "sets": "3", "reps": "12-15"}
            ]
        },
        "back": {
            "beginner": [
                {"name": "Dumbbell Rows", "equipment": "dumbbells", "sets": "3", "reps": "10-12"},
                {"name": "Lat Pulldowns", "equipment": "cables", "sets": "3", "reps": "10-12"},
                {"name": "Seated Cable Rows", "equipment": "cables", "sets": "3", "reps": "10-12"},
                {"name": "Back Extensions", "equipment": "bodyweight", "sets": "3", "reps": "12-15"}
            ],
            "intermediate": [
                {"name": "Pull-ups", "equipment": "bodyweight", "sets": "4", "reps": "6-10"},
                {"name": "Barbell Rows", "equipment": "barbell", "sets": "4", "reps": "8-10"},
                {"name": "T-Bar Rows", "equipment": "barbell", "sets": "3", "reps": "10-12"},
                {"name": "Face Pulls", "equipment": "cables", "sets": "3", "reps": "15-20"}
            ],
            "advanced": [
                {"name": "Weighted Pull-ups", "equipment": "bodyweight", "sets": "4", "reps": "6-8"},
                {"name": "Deadlifts", "equipment": "barbell", "sets": "4", "reps": "5-8"},
                {"name": "Pendlay Rows", "equipment": "barbell", "sets": "4", "reps": "6-8"},
                {"name": "Chest Supported Rows", "equipment": "dumbbells", "sets": "3", "reps": "10-12"}
            ]
        },
        "legs": {
            "beginner": [
                {"name": "Bodyweight Squats", "equipment": "bodyweight", "sets": "3", "reps": "12-15"},
                {"name": "Lunges", "equipment": "bodyweight", "sets": "3", "reps": "10-12 each leg"},
                {"name": "Leg Press", "equipment": "machine", "sets": "3", "reps": "12-15"},
                {"name": "Leg Curls", "equipment": "machine", "sets": "3", "reps": "12-15"}
            ],
            "intermediate": [
                {"name": "Barbell Squats", "equipment": "barbell", "sets": "4", "reps": "8-10"},
                {"name": "Romanian Deadlifts", "equipment": "barbell", "sets": "3", "reps": "10-12"},
                {"name": "Bulgarian Split Squats", "equipment": "dumbbells", "sets": "3", "reps": "10-12 each"},
                {"name": "Leg Extensions", "equipment": "machine", "sets": "3", "reps": "12-15"}
            ],
            "advanced": [
                {"name": "Back Squats", "equipment": "barbell", "sets": "5", "reps": "5-8"},
                {"name": "Front Squats", "equipment": "barbell", "sets": "4", "reps": "6-8"},
                {"name": "Deadlifts", "equipment": "barbell", "sets": "4", "reps": "5-8"},
                {"name": "Walking Lunges", "equipment": "dumbbells", "sets": "4", "reps": "12 each leg"}
            ]
        },
        "shoulders": {
            "beginner": [
                {"name": "Dumbbell Shoulder Press", "equipment": "dumbbells", "sets": "3", "reps": "10-12"},
                {"name": "Lateral Raises", "equipment": "dumbbells", "sets": "3", "reps": "12-15"},
                {"name": "Front Raises", "equipment": "dumbbells", "sets": "3", "reps": "12-15"},
                {"name": "Face Pulls", "equipment": "cables", "sets": "3", "reps": "15-20"}
            ],
            "intermediate": [
                {"name": "Overhead Press", "equipment": "barbell", "sets": "4", "reps": "8-10"},
                {"name": "Arnold Press", "equipment": "dumbbells", "sets": "3", "reps": "10-12"},
                {"name": "Lateral Raises", "equipment": "dumbbells", "sets": "4", "reps": "12-15"},
                {"name": "Reverse Flyes", "equipment": "dumbbells", "sets": "3", "reps": "12-15"}
            ],
            "advanced": [
                {"name": "Push Press", "equipment": "barbell", "sets": "4", "reps": "6-8"},
                {"name": "Seated Dumbbell Press", "equipment": "dumbbells", "sets": "4", "reps": "8-10"},
                {"name": "Cable Lateral Raises", "equipment": "cables", "sets": "4", "reps": "15-20"},
                {"name": "Upright Rows", "equipment": "barbell", "sets": "3", "reps": "10-12"}
            ]
        },
        "arms": {
            "beginner": [
                {"name": "Dumbbell Bicep Curls", "equipment": "dumbbells", "sets": "3", "reps": "10-12"},
                {"name": "Tricep Dips", "equipment": "bodyweight", "sets": "3", "reps": "8-12"},
                {"name": "Hammer Curls", "equipment": "dumbbells", "sets": "3", "reps": "10-12"},
                {"name": "Tricep Extensions", "equipment": "dumbbells", "sets": "3", "reps": "10-12"}
            ],
            "intermediate": [
                {"name": "Barbell Curls", "equipment": "barbell", "sets": "4", "reps": "8-10"},
                {"name": "Close-Grip Bench Press", "equipment": "barbell", "sets": "4", "reps": "8-10"},
                {"name": "Preacher Curls", "equipment": "dumbbells", "sets": "3", "reps": "10-12"},
                {"name": "Skull Crushers", "equipment": "barbell", "sets": "3", "reps": "10-12"}
            ],
            "advanced": [
                {"name": "Weighted Chin-ups", "equipment": "bodyweight", "sets": "4", "reps": "6-8"},
                {"name": "Close-Grip Bench Press", "equipment": "barbell", "sets": "5", "reps": "6-8"},
                {"name": "Cable Curls", "equipment": "cables", "sets": "4", "reps": "12-15"},
                {"name": "Overhead Tricep Extension", "equipment": "dumbbells", "sets": "4", "reps": "10-12"}
            ]
        },
        "core": {
            "beginner": [
                {"name": "Plank", "equipment": "bodyweight", "sets": "3", "reps": "30-60 seconds"},
                {"name": "Crunches", "equipment": "bodyweight", "sets": "3", "reps": "15-20"},
                {"name": "Bicycle Crunches", "equipment": "bodyweight", "sets": "3", "reps": "15-20"},
                {"name": "Dead Bug", "equipment": "bodyweight", "sets": "3", "reps": "10-12 each side"}
            ],
            "intermediate": [
                {"name": "Hanging Knee Raises", "equipment": "bodyweight", "sets": "3", "reps": "12-15"},
                {"name": "Russian Twists", "equipment": "bodyweight", "sets": "3", "reps": "20-30"},
                {"name": "Mountain Climbers", "equipment": "bodyweight", "sets": "3", "reps": "20-30"},
                {"name": "Cable Crunches", "equipment": "cables", "sets": "3", "reps": "15-20"}
            ],
            "advanced": [
                {"name": "Hanging Leg Raises", "equipment": "bodyweight", "sets": "4", "reps": "12-15"},
                {"name": "Ab Wheel Rollouts", "equipment": "ab_wheel", "sets": "4", "reps": "10-12"},
                {"name": "Dragon Flags", "equipment": "bodyweight", "sets": "3", "reps": "6-10"},
                {"name": "Pallof Press", "equipment": "cables", "sets": "3", "reps": "12-15 each side"}
            ]
        }
    }

    muscle_exercises = exercises.get(muscle_group.lower(), {}).get(level, [])

    # Filter by available equipment if specified
    if equipment and equipment != ["all"]:
        available_equipment = [e.lower() for e in equipment] + ["bodyweight"]
        muscle_exercises = [
            ex for ex in muscle_exercises
            if ex["equipment"].lower() in available_equipment
        ]

    return {
        "muscle_group": muscle_group,
        "level": level,
        "exercises": muscle_exercises,
        "equipment_available": equipment
    }


def calculate_progressive_overload(
    current_weight: float,
    current_reps: int,
    target_reps: int,
    progression_type: str = "weight"
) -> Dict[str, Any]:
    """
    Calculate progressive overload recommendations.

    Args:
        current_weight: Current working weight
        current_reps: Current reps performed
        target_reps: Target rep range (upper limit)
        progression_type: weight, reps, or both

    Returns:
        Progression recommendations
    """
    if progression_type == "weight":
        # If hitting upper rep range, increase weight by 2.5-5%
        if current_reps >= target_reps:
            new_weight = current_weight * 1.025  # 2.5% increase (conservative)
            recommendation = f"Increase weight to {round(new_weight, 1)} and drop reps to lower range"
        else:
            recommendation = f"Keep current weight {current_weight}, aim for {target_reps} reps"
            new_weight = current_weight
    elif progression_type == "reps":
        new_weight = current_weight
        recommendation = f"Keep weight at {current_weight}, add 1-2 reps per session"
    else:  # both
        new_weight = current_weight * 1.025
        recommendation = f"Increase weight to {round(new_weight, 1)} OR add 1-2 reps"

    return {
        "current": {
            "weight": current_weight,
            "reps": current_reps
        },
        "recommended": {
            "weight": round(new_weight, 1),
            "target_reps": target_reps
        },
        "progression_strategy": progression_type,
        "recommendation": recommendation,
        "notes": [
            "Only progress when you can complete all sets with good form",
            "Small increases are better than large jumps",
            "Aim to progress every 1-2 weeks",
            "Deload every 4-6 weeks to prevent overtraining"
        ]
    }
