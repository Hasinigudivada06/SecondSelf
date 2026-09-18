import math


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(value, maximum))


def simulate(
    current_skill,
    current_study,
    current_projects,
    current_exercise,
    future_study,
    future_projects,
    future_exercise,
    duration_months
):
    """
    Simulates possible future development.

    IMPORTANT:
    These are simulation indicators, not scientifically validated
    predictions of a person's actual future.
    """

    months = list(range(duration_months + 1))

    skill = []
    projects = []
    consistency = []
    balance = []

    # Starting values
    skill_value = float(current_skill)
    project_value = float(current_projects * 10)

    for month in months:

        if month > 0:

            # ---- SKILL GROWTH ----
            study_effect = future_study / 4

            project_effect = future_projects / 2

            growth = (
                2.2 * study_effect +
                1.4 * project_effect
            )

            # Diminishing returns as skill increases
            growth *= (1 - skill_value / 130)

            skill_value += growth

            # ---- PROJECT EXPERIENCE ----
            project_value += future_projects * 5

            # ---- CONSISTENCY ----
            target_load = min(future_study / 6, 1)

            exercise_component = future_exercise / 7

            consistency_value = (
                45 +
                target_load * 35 +
                exercise_component * 20
            )

            # ---- BALANCE ----
            study_pressure = max(
                0,
                future_study - 3
            )

            balance_value = (
                85
                - study_pressure * 9
                + future_exercise * 3
            )

        else:

            consistency_value = 60

            balance_value = 70

        skill.append(round(clamp(skill_value), 1))
        projects.append(round(clamp(project_value), 1))
        consistency.append(round(clamp(consistency_value), 1))
        balance.append(round(clamp(balance_value), 1))

    return {
        "months": months,
        "skill": skill,
        "projects": projects,
        "consistency": consistency,
        "balance": balance,

        "final": {
            "skill": round(skill[-1]),
            "projects": round(projects[-1]),
            "consistency": round(consistency[-1]),
            "balance": round(balance[-1])
        }
    }


if __name__ == "__main__":

    result = simulate(
        current_skill=50,
        current_study=2,
        current_projects=1,
        current_exercise=3,

        future_study=4,
        future_projects=2,
        future_exercise=2,

        duration_months=6
    )

    print("\nSECONDSELF SIMULATION\n")

    print("Final Results:")
    print(result["final"])

    print("\nMonthly Skill:")
    print(result["skill"])