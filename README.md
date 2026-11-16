# Lab 2: ALU Transcript Generator

A Python application and a Bash script that calculate a student's final academic standing from a CSV of course grades, then archive the data.

## Files
- `grade-evaluator.py`: validates the data, calculates the GPA, decides PASSED/FAILED and lists resubmission options.
- `organizer.sh`: archives `grades.csv` with a timestamp, creates a fresh empty `grades.csv`, and logs the action to `organizer.log`.
- `grades.csv`: sample data with columns `assignment,group,score,weight`.

## How to run

### Grade evaluator
```bash
python3 grade-evaluator.py
```
Enter the CSV filename when prompted (e.g., `grades.csv`).

### Organizer
```bash
bash organizer.sh
```
This moves `grades.csv` into `archive/` as `grades_YYYYMMDD-HHMMSS.csv`, creates a new empty `grades.csv`, and appends an entry to `organizer.log`. Back up your data before running it.

## What the evaluator does
- **Validation:** scores must be 0-100. Weights must total 100, with Formative = 60 and Summative = 40.
- **GPA:** `(Total Grade / 100) * 5.0`
- **Pass/Fail:** a student passes only with at least 50% in BOTH the Formative and Summative categories.
- **Resubmission:** among failed formative assignments (score below 50), the one(s) with the highest weight are eligible. If several tie, all are listed.
- **Error handling:** missing or empty file, missing columns, blank rows, non-numeric values and invalid groups all produce clear messages instead of crashes.

## Sample output
```
--- Processing Grades ---
Formative Total: 34.00/60 (56.7%)
Summative Total: 26.00/40 (65.0%)
Total Grade: 60.00/100
GPA: 3.000
Final Decision: PASSED

Eligible for resubmission (highest-weight failed formative):
  - Group Exercise (score: 40, weight: 20)
  - Functions and Debugging Lab (score: 45, weight: 20)
```

## Testing
The logic was cross-checked against the provided ALU transcript sheet. For its sample data, the program gives Formative 44.40, Summative 32.50, GPA 3.845, PASSED, with Discussion Forum eligible for resubmission, matching the sheet.

## Notes
No external libraries are used, only Python's built-in `csv`, `sys` and `os`.