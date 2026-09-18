"""Deterministic, transparent scenario simulation for SecondSelf.

This is a simple heuristic tool, not a scientific model or a prediction of
real-world outcomes.
"""


def _clamp(value, minimum=0.0, maximum=100.0):
	"""Keep a score within the documented range."""
	return max(minimum, min(maximum, float(value)))


def _number(mapping, key, default=0.0):
	"""Read a numeric input without requiring any external dependencies."""
	try:
		return float(mapping.get(key, default))
	except (TypeError, ValueError, AttributeError):
		return float(default)


def simulate(input_data):
	"""Return monthly heuristic indicators for a current state and scenario.

	Expected input::

		{
			"current": {
				"skill_level": 60,
				"study_hours_per_day": 2,
				"projects_per_month": 1,
				"exercise_days_per_week": 3,
			},
			"scenario": {
				"study_hours_per_day": 3,
				"projects_per_month": 2,
				"exercise_days_per_week": 4,
				"duration_months": 6,
			},
		}

	Scenario values replace current values for the simulated period. The
	returned ``months`` list includes month 0 (the starting point).
	"""
	if not isinstance(input_data, dict):
		raise TypeError("input_data must be a dictionary")

	current = input_data.get("current", {})
	scenario = input_data.get("scenario", {})
	if not isinstance(current, dict) or not isinstance(scenario, dict):
		raise TypeError("current and scenario must be dictionaries")

	duration = max(0, int(_number(scenario, "duration_months", 0)))
	skill = _clamp(_number(current, "skill_level", 0))
	study = max(0.0, _number(scenario, "study_hours_per_day",
							  _number(current, "study_hours_per_day", 0)))
	projects = max(0.0, _number(scenario, "projects_per_month",
								_number(current, "projects_per_month", 0)))
	exercise = max(0.0, _number(scenario, "exercise_days_per_week",
								_number(current, "exercise_days_per_week", 0)))

	months = []
	for month in range(duration + 1):
		# Each month adds a capped fraction of available study effort.
		skill_value = _clamp(skill + month * (study * 1.5))
		project_value = _clamp(projects * 20.0 + month * projects * 4.0)
		consistency_value = _clamp((study / 4.0) * 45.0 +
								   (projects / 3.0) * 30.0 +
								   (exercise / 5.0) * 25.0)
		# Balance rewards moderate exercise and a manageable study load.
		exercise_score = 100.0 - abs(exercise - 4.0) * 18.0
		study_score = 100.0 - abs(study - 3.0) * 15.0
		balance_value = _clamp((exercise_score + study_score) / 2.0)

		months.append({
			"month": month,
			"skill_growth": round(skill_value, 2),
			"project_experience": round(project_value, 2),
			"consistency": round(consistency_value, 2),
			"balance": round(balance_value, 2),
		})

	return {"months": months}
if __name__ == "__main__":
    test_input = {
        "current": {
            "skill_level": 50,
            "study_hours_per_day": 2,
            "projects_per_month": 1,
            "exercise_days_per_week": 3
        },
        "scenario": {
            "study_hours_per_day": 4,
            "projects_per_month": 2,
            "exercise_days_per_week": 3,
            "duration_months": 6
        }
    }

    result = simulate(test_input)

    print("\nSECONDSELF SIMULATION RESULT")
    print(result)
    