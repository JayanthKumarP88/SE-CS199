# Lab 5: Static Code Analysis — Conference Room & Equipment Scheduler

**Course:** Software Engineering (SE) Lab  
**Student Name:** Jayanth Kumar P  
**SRN:** PES1UG24CS199  
**Assigned Template Repository:** [SETAPESU26/L5_12_room_scheduler](https://github.com/SETAPESU26/L5_12_room_scheduler)  
**Main Submission Repository:** [JayanthKumarP88/SE-CS199](https://github.com/JayanthKumarP88/SE-CS199)  

---

## Overview

This lab focuses on enhancing Python code quality, security, and maintainability by applying industry-standard static code analysis tools:
- **Bandit:** AST-based security vulnerability and threat auditor.
- **Pylint:** Strict code reviewer for logic errors, design smells, and structural flaws.
- **Flake8:** PEP 8 style, syntax, and formatting checker.

The target system is `scheduler_system.py`, a conference room and equipment scheduler that reserves rooms for time slots, allocates equipment pools, logs booking conflicts, and exports schedules to JSON.

---

## Deliverables & Analysis Artifacts

| Deliverable | Description | Link |
| :--- | :--- | :--- |
| **Cleaned Script** | Fully refactored and verified Python script | [`scheduler_system.py`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%205/scheduler_system.py) |
| **Issue Documentation** | Comprehensive table of identified issues, severities, and fixes | [`issues.md`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%205/issues.md) |
| **Reflection Report** | Detailed answers to the four lab reflection questions | [`reflection.md`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%205/reflection.md) |
| **Student Handout** | Official lab handout instructions | [`Lab_5_Static_Code_Analysis_Student_handout.pdf`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%205/Lab_5_Static_Code_Analysis_Student_handout.pdf) |
| **Pylint Reports** | Before (5.60/10) vs After (**10.00/10**) analysis reports | [`reports/before/pylint_report.txt`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%205/reports/before/pylint_report.txt) \| [`reports/after/pylint_report.txt`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%205/reports/after/pylint_report.txt) |
| **Bandit Reports** | Before (1 High, 1 Low) vs After (**0 issues**) reports | [`reports/before/bandit_report.txt`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%205/reports/before/bandit_report.txt) \| [`reports/after/bandit_report.txt`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%205/reports/after/bandit_report.txt) |
| **Flake8 Reports** | Before (13 violations) vs After (**0 violations**) reports | [`reports/before/flake8_report.txt`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%205/reports/before/flake8_report.txt) \| [`reports/after/flake8_report.txt`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%205/reports/after/flake8_report.txt) |

---

## Directory Structure

```
Lab 5/
├── .gitignore
├── issues.md
├── Lab_5_Static_Code_Analysis_Student_handout.pdf
├── README.md
├── reflection.md
├── scheduler_system.py
└── reports/
    ├── before/
    │   ├── bandit_report.txt
    │   ├── flake8_report.txt
    │   └── pylint_report.txt
    └── after/
        ├── bandit_report.txt
        ├── flake8_report.txt
        └── pylint_report.txt
```

---

## Results & Quality Metrics Comparison

```
+--------------------+-------------------------+-------------------------+
| Metric / Tool      | Baseline (Before)       | Cleaned (After Fixes)   |
+--------------------+-------------------------+-------------------------+
| Pylint Score       | 5.60 / 10.00            | 10.00 / 10.00 (+4.40)   |
| Bandit Issues      | 1 High (B605), 1 Low    | 0 issues (Clean)        |
| Flake8 Violations  | 13 style/syntax errors  | 0 violations (Clean)    |
| Program Execution  | Failed (cat not found)  | Passed successfully     |
+--------------------+-------------------------+-------------------------+
```

---

## How to Run

### 1. Prerequisites & Virtual Environment
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install pylint bandit flake8
```

### 2. Run Static Analysis Tools
```bash
# Bandit security audit
python -m bandit -r scheduler_system.py

# Pylint quality evaluation
python -m pylint scheduler_system.py

# Flake8 style compliance check
python -m flake8 scheduler_system.py
```

### 3. Run the Program
```bash
python scheduler_system.py
```

---

## 3-Commit Progression Summary

1. **Commit 1 (`fix(security)`):** Resolved Bandit vulnerabilities — replaced unsafe `os.system("cat ...")` shell process with native Python file reading (`B605`), and eliminated bare `except: pass` exception suppression (`B110`).
2. **Commit 2 (`fix(quality)`):** Resolved Pylint design & logic issues — replaced mutable default argument `equipment_list=[]` (`W0102`), added PEP 257 docstrings, encapsulated state to remove global mutation warnings, applied `with open(...)` context managers, and elevated score to **10.00/10**.
3. **Commit 3 (`style(pep8)`):** Resolved Flake8 formatting issues — enforced PEP 8 line length limits (<= 79 chars), ensured two blank lines between top-level functions, removed unused variables, generated final reports, and added complete issue tracking and reflection documentation.
