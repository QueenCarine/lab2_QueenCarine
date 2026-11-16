import csv
import sys
import os

COLUMNS = ['assignment', 'group', 'score', 'weight']
GROUPS = ('Formative', 'Summative')
PASS_MARK = 50.0


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    Skips blank rows and reports malformed rows clearly.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    if os.path.getsize(filename) == 0:
        print(f"Error: The file '{filename}' is empty. Add grade data and try again.")
        sys.exit(1)

    assignments = []
    problems = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                print(f"Error: '{filename}' has no header row.")
                sys.exit(1)

            headers = [h.strip().lower() for h in reader.fieldnames if h]
            missing = [c for c in COLUMNS if c not in headers]
            if missing:
                print(f"Error: Missing column(s): {', '.join(missing)}.")
                print(f"Expected header: {','.join(COLUMNS)}")
                sys.exit(1)

            for line_no, raw in enumerate(reader, start=2):
                row = {(k or '').strip().lower(): (v or '').strip() for k, v in raw.items()}

                # Skip completely empty rows
                if not any(row.values()):
                    continue

                name = row['assignment']
                group = row['group'].title()

                if not name:
                    problems.append(f"Line {line_no}: assignment name is missing.")
                    continue
                if group not in GROUPS:
                    problems.append(
                        f"Line {line_no} ({name}): group '{row['group']}' must be "
                        f"'Formative' or 'Summative'.")
                    continue
                try:
                    score = float(row['score'])
                except ValueError:
                    problems.append(
                        f"Line {line_no} ({name}): score '{row['score']}' is not a number (e.g., 85).")
                    continue
                try:
                    weight = float(row['weight'])
                except ValueError:
                    problems.append(
                        f"Line {line_no} ({name}): weight '{row['weight']}' is not a number (e.g., 20).")
                    continue

                assignments.append({
                    'assignment': name,
                    'group': group,
                    'score': score,
                    'weight': weight
                })
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)

    if problems:
        print("Error: Invalid data found in the CSV file:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)

    if not assignments:
        print("Error: The file has headers but no grade rows.")
        sys.exit(1)

    return assignments


def evaluate_grades(data):
    """
    Validates the data, calculates the final grade and GPA,
    decides PASSED/FAILED and lists resubmission options.
    """
    print("\n--- Processing Grades ---")

    # a) Check if all scores are percentage based (0-100)
    invalid_scores = [d for d in data if d['score'] < 0 or d['score'] > 100]
    if invalid_scores:
        print("Error: Scores must be between 0 and 100. Invalid assignment(s):")
        for d in invalid_scores:
            print(f"  - {d['assignment']}: {d['score']}")
        return

    # b) Validate total weights (Total=100, Summative=40, Formative=60)
    formative = [d for d in data if d['group'] == 'Formative']
    summative = [d for d in data if d['group'] == 'Summative']

    formative_weight = sum(d['weight'] for d in formative)
    summative_weight = sum(d['weight'] for d in summative)
    total_weight = formative_weight + summative_weight

    weight_errors = []
    if abs(total_weight - 100) > 1e-6:
        weight_errors.append(f"Total weight is {total_weight:g}, expected 100.")
    if abs(formative_weight - 60) > 1e-6:
        weight_errors.append(f"Formative weight is {formative_weight:g}, expected 60.")
    if abs(summative_weight - 40) > 1e-6:
        weight_errors.append(f"Summative weight is {summative_weight:g}, expected 40.")
    if weight_errors:
        print("Error: Invalid weights:")
        for e in weight_errors:
            print(f"  - {e}")
        return

    # c) Calculate the Final Grade and GPA
    formative_grade = sum(d['score'] * d['weight'] / 100 for d in formative)
    summative_grade = sum(d['score'] * d['weight'] / 100 for d in summative)
    total_grade = formative_grade + summative_grade
    gpa = (total_grade / 100) * 5.0

    # d) Determine Pass/Fail status (>= 50% in BOTH categories)
    f_pct = formative_grade / formative_weight * 100
    s_pct = summative_grade / summative_weight * 100
    passed = f_pct >= PASS_MARK and s_pct >= PASS_MARK

    # e) Check for failed formative assignments (< 50%)
    #          and determine which one(s) have the highest weight for
    failed_formatives = [d for d in formative if d['score'] < PASS_MARK]
    resubmit = []
    if failed_formatives:
        highest_weight = failed_formatives[0]['weight']
        for d in failed_formatives:
            if d['weight'] > highest_weight:
                highest_weight = d['weight']
        resubmit = [d for d in failed_formatives if d['weight'] == highest_weight]

    # f) Print the final decision (PASSED / FAILED) and resubmission options
    print(f"Formative Total: {formative_grade:.2f}/60 ({f_pct:.1f}%)")
    print(f"Summative Total: {summative_grade:.2f}/40 ({s_pct:.1f}%)")
    print(f"Total Grade: {total_grade:.2f}/100")
    print(f"GPA: {gpa:.2f}")
    print(f"Overall Standing: {'PASSED' if passed else 'FAILED'}")

    if resubmit:
        print("\nEligible for resubmission (highest-weight failed formative):")
        for d in resubmit:
            print(f"  - {d['assignment']} (score: {d['score']:g}, weight: {d['weight']:g})")
    elif not passed:
        print("\nAll formatives are passed - no resubmission required.")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)