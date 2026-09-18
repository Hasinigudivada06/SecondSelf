import re
from simulator import simulate

def parse_what_if(user_text, current_profile):
    """
    Convert a simple natural-language What-If request
    into a structured scenario.

    This local parser is intentionally simple and reliable.
    """

    text = user_text.lower()

    # Start with current profile values
    study_hours = current_profile.get("study_hours_per_day", 2)
    projects = current_profile.get("projects_per_month", 1)
    exercise = current_profile.get("exercise_days_per_week", 3)

    duration = 6

    # Find study hours
    study_match = re.search(
        r'(\d+(?:\.\d+)?)\s*(?:hours?|hrs?)\s*(?:a|per|each)\s*day',
        text
    )

    if study_match:
        study_hours = float(study_match.group(1))

    # Find projects per month
    project_match = re.search(
        r'(\d+)\s*projects?\s*(?:a|per|each)\s*month',
        text
    )

    if project_match:
        projects = float(project_match.group(1))

    # Find exercise days
    exercise_match = re.search(
        r'(\d+)\s*(?:days?|times?)\s*(?:a|per|each)\s*week',
        text
    )

    if "exercise" in text and exercise_match:
        exercise = float(exercise_match.group(1))

    # Find duration
    duration_match = re.search(
        r'(\d+)\s*months?',
        text
    )

    if duration_match:
        duration = int(duration_match.group(1))

    # Keep values in safe ranges
    study_hours = max(0, min(12, study_hours))
    projects = max(0, min(10, projects))
    exercise = max(0, min(7, exercise))
    duration = max(1, min(24, duration))

    return {
        "study_hours_per_day": study_hours,
        "projects_per_month": projects,
        "exercise_days_per_week": exercise,
        "duration_months": duration
    }


def run_what_if(user_text, current_profile):
    """Run the complete natural-language What-If simulation pipeline.

    This is the single UI-facing entry point: it parses the user's request,
    runs the deterministic simulator, and returns both outputs.
    """
    scenario = parse_what_if(user_text, current_profile)
    simulation = simulate({
        "current": current_profile,
        "scenario": scenario,
    })

    return {
        "scenario": scenario,
        "simulation": simulation,
    }


if __name__ == "__main__":

    current_profile = {
        "skill_level": 50,
        "study_hours_per_day": 2,
        "projects_per_month": 1,
        "exercise_days_per_week": 3
    }

    user_request = (
        "What if I study 4 hours a day and complete "
        "2 projects every month for 6 months?"
    )

    result = run_what_if(user_request, current_profile)

    print("\nSECONDSELF WHAT-IF RESULT")
    print(result["scenario"])

    print("\nSIMULATION RESULT")

    for month in result["simulation"]["months"]:
        print(month)
