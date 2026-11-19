# Lab 7: Fuzzing for Input Validation Bugs — Amusement Park Ride Access

**Course:** Software Engineering (SE) Lab  
**Student Name:** Jayanth Kumar P  
**SRN:** PES1UG24CS199  
**Assigned Repository:** [SETAPESU26/L6_L7_11_amusement_park_ride_access](https://github.com/SETAPESU26/L6_L7_11_amusement_park_ride_access)  
**Submission Repository:** [JayanthKumarP88/SE-CS199](https://github.com/JayanthKumarP88/SE-CS199)  

---

## Overview

This lab explores **fuzz testing** (or property-based testing) as an automated dynamic security and quality assurance technique. Using Python's **Hypothesis** fuzzing library, pseudo-random malformed, boundary, unexpected, and extreme inputs are synthesized to expose hidden edge-case bugs and unhandled runtime exceptions.

The application under test is `processor.py`, which provides three core functions for amusement park operations:
1. `validate_height_and_fastpass(rider_spec)`: Parses and validates rider height and FastPass eligibility.
2. `compute_dispatch_throughput(ride_metric_str)`: Calculates ride dispatch throughput rate (riders/minute).
3. `resolve_safety_restraint_code(zone_code)`: Resolves safety restraint hardware types by ride zone code.

---

## Deliverables

| Deliverable | Description | Link |
| :--- | :--- | :--- |
| **PDF Document** | Complete B&W formatted report with terminal screenshots & analysis | [`Lab7_Fuzz_Testing_Report_JayanthKumarP.pdf`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%207/Lab7_Fuzz_Testing_Report_JayanthKumarP.pdf) |
| **Fixed Application** | Defensively hardened Python script | [`processor.py`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%207/processor.py) |
| **Updated Test Code** | Completed Hypothesis property fuzz testing test suite | [`test_processor.py`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%207/test_processor.py) |
| **Student Handout** | Official lab instructions & guidelines | [`Lab_7_FuzzTesting_Student_Handout.pdf`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%207/Lab_7_FuzzTesting_Student_Handout.pdf) |
| **Step 2 Screenshot** | Execution of buggy `processor.py` | [`screenshots/step2_buggy_processor.png`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%207/screenshots/step2_buggy_processor.png) |
| **Step 4 Screenshot** | Hypothesis test cases failing against buggy code | [`screenshots/step4_failing_tests.png`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%207/screenshots/step4_failing_tests.png) |
| **Step 5 Screenshot** | Execution of fixed `processor.py` | [`screenshots/step5_fixed_processor.png`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%207/screenshots/step5_fixed_processor.png) |
| **Step 6 Screenshot** | Hypothesis test cases passing against hardened code | [`screenshots/step6_passing_tests.png`](file:///c:/Users/vegit/Downloads/SE-CS199/Lab%207/screenshots/step6_passing_tests.png) |

---

## Directory Structure

```
Lab 7/
├── .gitignore
├── Lab_7_FuzzTesting_Student_Handout.pdf
├── Lab7_Fuzz_Testing_Report_JayanthKumarP.pdf
├── processor.py
├── README.md
├── test_processor.py
└── screenshots/
    ├── step2_buggy_processor.png
    ├── step4_failing_tests.png
    ├── step5_fixed_processor.png
    └── step6_passing_tests.png
```

---

## Fuzz Testing Summary: Defects Uncovered & Fixes Applied

| Function | Minimal Failing Input Discovered by Hypothesis | Exception Type | Root Cause | Defensive Fix Applied |
| :--- | :--- | :--- | :--- | :--- |
| `validate_height_and_fastpass` | `s = None`<br/>`s = ""` | `AttributeError`<br/>`ValueError` | `.strip()` on None; `.split(':')` expects 2 elements but gets 1. | Added `isinstance(rider_spec, str)` check, validated presence of `:` delimiter, verified 2 split parts, validated integer height range (0-300), and checked `pass_map` membership. |
| `compute_dispatch_throughput` | `s = None`<br/>`s = "/"`<br/>`s = "10/0"` | `AttributeError`<br/>`ValueError`<br/>`ZeroDivisionError` | Missing delimiter check; empty string converted to float; division by 0 cycle minutes. | Validated type is string, confirmed `/` delimiter, verified 2 split parts, wrapped in `try/except (ValueError, ZeroDivisionError, OverflowError)`, guarded against `cycle_mins <= 0`, safely returning `0.0`. |
| `resolve_safety_restraint_code` | `s = None`<br/>`s = ""` | `AttributeError`<br/>`KeyError` | `.strip()` on None; unlisted or empty 3-character prefix causes KeyError. | Validated string type, safely retrieved restraint type using `.get(prefix, "Unknown Restraint / Invalid Code")`. |

---

## How to Run

### 1. Install Dependencies
```bash
python -m pip install hypothesis pytest
```

### 2. Run the Application
```bash
python processor.py
```

### 3. Run Hypothesis Fuzz Tests
```bash
pytest test_processor.py
```
*(Runs hundreds of randomly generated Unicode strings, empty strings, and `None` values to verify no uncaught crashes occur.)*
