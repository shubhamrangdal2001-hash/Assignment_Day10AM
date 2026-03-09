# Part D - AI-Augmented Task
# Improved version of the AI-generated grade merger function
# Added type hints, docstrings, edge case handling, safe .get() usage

from collections import defaultdict


# ─────────────────────────────────────────────
# Improved Version (written after AI critique)
# ─────────────────────────────────────────────
def merge_grade_report(
    sem1: dict[str, float],
    sem2: dict[str, float]
) -> dict:
    """
    Merges student grade data from two semesters into a single report.

    Args:
        sem1: Dict mapping subject names to grades for semester 1.
              Example: {'Math': 8.5, 'Science': 7.0}
        sem2: Dict mapping subject names to grades for semester 2.
              Example: {'Math': 9.0, 'English': 7.5}

    Returns:
        A dict with:
            - combined_gpa   : average of all grades across both semesters
            - grade_trend    : 'improving', 'declining', or 'stable'
            - common_subjects: subjects present in both semesters with both grades
            - sem1_only      : subjects only in semester 1
            - sem2_only      : subjects only in semester 2

    Edge cases handled:
        - Empty dicts: returns safe defaults, no crash
        - Single semester: trend set to 'not enough data'
        - Missing subjects: reported separately
        - All values accessed via .get() for safety
    """

    # edge case: both empty
    if not sem1 and not sem2:
        return {
            'combined_gpa':    0.0,
            'grade_trend':     'not enough data',
            'common_subjects': {},
            'sem1_only':       {},
            'sem2_only':       {},
        }

    all_grades = list(sem1.values()) + list(sem2.values())
    combined_gpa = round(sum(all_grades) / len(all_grades), 2) if all_grades else 0.0

    # trend: compare average of sem1 vs sem2 (only if both non-empty)
    if sem1 and sem2:
        avg1 = sum(sem1.values()) / len(sem1)
        avg2 = sum(sem2.values()) / len(sem2)
        diff = avg2 - avg1
        if diff > 0.2:
            trend = 'improving'
        elif diff < -0.2:
            trend = 'declining'
        else:
            trend = 'stable'
    else:
        trend = 'not enough data'

    # common subjects: use set intersection, access via .get()
    common_keys = set(sem1.keys()) & set(sem2.keys())
    common_subjects = {
        subj: {'sem1': sem1.get(subj), 'sem2': sem2.get(subj)}
        for subj in common_keys
    }

    sem1_only = {s: g for s, g in sem1.items() if s not in common_keys}
    sem2_only = {s: g for s, g in sem2.items() if s not in common_keys}

    return {
        'combined_gpa':    combined_gpa,
        'grade_trend':     trend,
        'common_subjects': common_subjects,
        'sem1_only':       sem1_only,
        'sem2_only':       sem2_only,
    }


# ─────────────────────────────────────────────
# Demo
# ─────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 55)
    print("  PART D — SEMESTER GRADE REPORT MERGER")
    print("=" * 55)

    sem1 = {'Math': 7.5, 'Science': 6.8, 'English': 8.0, 'History': 7.0}
    sem2 = {'Math': 8.5, 'Science': 7.5, 'Physics': 8.0}

    print("\n[Test 1] Normal case")
    report = merge_grade_report(sem1, sem2)
    for k, v in report.items():
        print(f"    {k}: {v}")

    print("\n[Test 2] Improving trend")
    r2 = merge_grade_report({'Math': 5.0}, {'Math': 9.0})
    print(f"    combined_gpa: {r2['combined_gpa']}, trend: {r2['grade_trend']}")

    print("\n[Test 3] Empty sem1")
    r3 = merge_grade_report({}, {'Math': 8.0})
    print(f"    combined_gpa: {r3['combined_gpa']}, trend: {r3['grade_trend']}")

    print("\n[Test 4] Both empty")
    r4 = merge_grade_report({}, {})
    print(f"    {r4}")
