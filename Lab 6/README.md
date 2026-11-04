# Lab 6: Code and Branch Coverage Analysis — Amusement Park Ride Access

**Course:** Software Engineering (SE) Lab  
**Student Name:** Jayanth Kumar P  
**SRN:** PES1UG24CS199  
**Assigned Repository:** [SETAPESU26/L6_L7_11_amusement_park_ride_access](https://github.com/SETAPESU26/L6_L7_11_amusement_park_ride_access)  
**Submission Repository:** [JayanthKumarP88/SE-CS199](https://github.com/JayanthKumarP88/SE-CS199)  

---

## Overview

This lab focuses on measuring, analyzing, and improving software test completeness using Python's `coverage` tool and `pytest`. Testing is evaluated across two critical testing dimensions:
- **Code (Line) Coverage:** Measuring the proportion of executable statements traversed by the test suite.
- **Branch Coverage:** Measuring whether each conditional decision point (`if`, `elif`, `else`, boolean guards, loop terminations) evaluates to both `True` and `False`.

The system under test is `amusement_park_ride_access.py`, which handles:
1. Ride ticketing and admissions (`process_ride_admissions`): Validating patron height limits, health warnings, child ticket discounts, express pass fees, and safety audit thresholds.
2. Ride restraint monitoring (`inspect_safety_restraints`): Auditing continuous sensor data streams for consecutive unlatched sensor alarms (`EMERGENCY_LOCK` vs `SAFE`).

---

## Deliverables & Analysis Artifacts

| Deliverable | Description | Link |
| :--- | :--- | :--- |
| **Application Script** | The module under test | [`amusement_park_ride_access.py`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%206/amusement_park_ride_access.py) |
| **Code Coverage Test Suite** | Test cases targeting 100% statement (line) coverage | [`CodeCoverageTest_amusement_park_ride_access.py`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%206/CodeCoverageTest_amusement_park_ride_access.py) |
| **Branch Coverage Test Suite** | Test cases targeting 100% branch and boundary coverage | [`BranchCoverageTest_amusement_park_ride_access.py`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%206/BranchCoverageTest_amusement_park_ride_access.py) |
| **Master Test Script** | Complete unified test runner (imports both suites) | [`test_amusement_park.py`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%206/test_amusement_park.py) |
| **Student Handout** | Official lab instructions & guidelines | [`Lab_6_Code&BranchCoverage_Student_Handout.pdf`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%206/Lab_6_Code&BranchCoverage_Student_Handout.pdf) |
| **Code Coverage Screenshot** | Terminal output screenshot demonstrating 100% line coverage | [`screenshots/code_coverage_analysis.png`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%206/screenshots/code_coverage_analysis.png) |
| **Branch Coverage Screenshot** | Terminal output screenshot demonstrating 100% branch coverage | [`screenshots/branch_coverage_analysis.png`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%206/screenshots/branch_coverage_analysis.png) |
| **Code Coverage Report** | Plaintext terminal report for line coverage | [`reports/code_coverage_report.txt`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%206/reports/code_coverage_report.txt) |
| **Branch Coverage Report** | Plaintext terminal report for branch coverage | [`reports/branch_coverage_report.txt`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%206/reports/branch_coverage_report.txt) |
| **Initial Baseline Report** | Baseline report from starter test (48% line, 45% branch) | [`reports/initial_coverage_report.txt`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%206/reports/initial_coverage_report.txt) |

---

## Directory Structure

```
Lab 6/
├── .gitignore
├── amusement_park_ride_access.py
├── CodeCoverageTest_amusement_park_ride_access.py
├── BranchCoverageTest_amusement_park_ride_access.py
├── test_amusement_park.py
├── Lab_6_Code&BranchCoverage_Student_Handout.pdf
├── README.md
├── screenshots/
│   ├── code_coverage_analysis.png
│   └── branch_coverage_analysis.png
└── reports/
    ├── initial_coverage_report.txt
    ├── code_coverage_report.txt
    └── branch_coverage_report.txt
```

---

## Coverage Analysis & Comparison

```
+------------------------------------+--------------------+--------------------+
| Metric                             | Initial Baseline   | Final Achieved     |
+------------------------------------+--------------------+--------------------+
| Line (Statement) Coverage          | 48% (30 missed)    | 100% (0 missed)    |
| Branch Coverage                    | 45% (12 partial)   | 100% (0 missed)    |
| Passing Unit Tests                 | 1 passed           | 36 passed          |
| Missing Lines / Untested Branches  | 30 lines / 12 br   | 0 lines / 0 br     |
+------------------------------------+--------------------+--------------------+
```

### Initial Coverage (Starter Test Case):
- Total statements: 58
- Executed statements: 28 (48% coverage)
- Missed statements: 30 (`3, 10, 16, 18, 22-23, 33-34, 37-41, 43-44, 46, 51, 56, 58, 63-75`)
- Branch coverage: 45%

### Final Coverage (Targeted Test Suites):
- Total statements in module: 58 / 58 executed (**100% Line Coverage**)
- Total branches in module: 40 / 40 evaluated both True and False (**100% Branch Coverage**)
- Missing statements: **None (0)**
- Missing branches: **None (0)**

---

## Line Coverage vs. Branch Coverage: Key Takeaways

1. **Why Line Coverage is Insufficient:**
   - Line coverage checks only whether an instruction was executed at least once.
   - For example, if a conditional `if condition:` executes when `condition` is `True`, line coverage reports 100% for that block even if the `False` branch (or default fall-through) has never been tested.
2. **The Power of Branch Coverage:**
   - Branch coverage enforces testing of all decision outcomes.
   - In `amusement_park_ride_access.py`, this caught untested paths such as:
     - `height_cm < 120` vs `height_cm == 120` (boundary test).
     - Health warning breaks on `roller_coaster` vs non-breaking continuation on `water_ride` and `family`.
     - `has_fast_lane` being omitted vs being explicitly `False` or `True`.
     - `rejected_patrons > 4` (triggering `SAFETY_AUDIT`) vs `rejected_patrons == 4` (which should remain `COMPLETED`).
     - Safety sensor reading streaks: consecutive unlatched sensor zeroes (`unlatched_streak >= 2` triggering `EMERGENCY_LOCK`) vs isolated unlatched zeroes reset by latched sensors (`sensor_val != 0`).

---

## How to Run the Tests & Reproduce Reports

### 1. Environment Setup
```bash
python -m pip install coverage pytest
```

### 2. Run Code (Line) Coverage
```bash
# Execute tests and collect line coverage
python -m coverage run -m pytest CodeCoverageTest_amusement_park_ride_access.py

# Display line coverage report with missing lines
python -m coverage report -m
```

### 3. Run Branch Coverage
```bash
# Execute tests and collect branch coverage
python -m coverage run --branch -m pytest BranchCoverageTest_amusement_park_ride_access.py

# Display branch coverage report with partial branches
python -m coverage report -m
```

### 4. Run Unified Test Suite
```bash
python -m coverage run --branch -m pytest test_amusement_park.py
python -m coverage report -m
```

---

## Git Commit Progression

1. **Commit 1:** `feat(lab6): add CodeCoverageTest_amusement_park_ride_access test suite achieving 100% line coverage and screenshot`
2. **Commit 2:** `feat(lab6): add BranchCoverageTest_amusement_park_ride_access achieving 100% branch coverage, screenshots, and documentation`
