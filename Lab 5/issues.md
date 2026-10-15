# Static Code Analysis Findings — Issue Table

**Course:** Software Engineering (SE) Lab  
**Lab:** Lab 5 — Static Code Analysis  
**Student Name:** Jayanth Kumar P  
**SRN:** PES1UG24CS199  
**Assigned Repository:** [SETAPESU26/L5_12_room_scheduler](https://github.com/SETAPESU26/L5_12_room_scheduler)  
**File Analyzed:** `scheduler_system.py`  

---

## Identified Issues & Remediation Summary

| Issue Code / Name | Tool | Type / Severity | Line(s) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **B605**: `start_process_with_a_shell` | Bandit | Security Vulnerability (High) | 43 | `os.system("cat " + file)` invokes a subshell to display file contents. This introduces command injection risks if file paths are manipulated and causes runtime crashes on Windows (`'cat' is not recognized`). | Removed `os.system` and unused `import os`. Replaced with safe native Python file reading using `with open(file, "r", encoding="utf-8") as f_in: print(f_in.read(), end="")`. |
| **B110**: `try_except_pass` / **W0702**: `bare-except` / **E722**: `bare 'except'` | Bandit, Pylint, Flake8 | Security & Reliability (Low/Warning) | 27–28 | Catch-all `except:` block silently suppressing exceptions with `pass`. Masks critical bugs (e.g., `KeyboardInterrupt`, `KeyError`, `TypeError`) and renders debugging impossible. | Replaced broad exception silencing with explicit membership validation (`if reservation_id not in reservations: return False`) and proper equipment deallocation. |
| **W0102**: `dangerous-default-value` | Pylint | Bug / Logic Flaw (Warning) | 11 | Mutable default argument `equipment_list=[]` retains state across multiple function invocations because default objects are instantiated once at function definition. | Replaced default parameter with `equipment_list=None` and dynamically initialized inside the function: `if equipment_list is None: equipment_list = []`. |
| **R1732**: `consider-using-with` & **W1514**: `unspecified-encoding` | Pylint | Resource Management & Portability (Refactor) | 35, 40 | File streams opened via `f = open(...)` without context management (`with`) risk leaking file descriptors upon exceptions. Omitting encoding leads to OS-dependent encoding mismatches (e.g., CP1252 vs UTF-8). | Refactored all file operations to employ context managers (`with open(file, mode, encoding="utf-8") as f:`), ensuring deterministic closure and cross-platform consistency. |
| **C0114**: `missing-module-docstring` & **C0116**: `missing-function-docstring` | Pylint | Documentation & Standard (Convention) | 1, 11, 22, 30, 34, 39, 45 | Missing PEP 257 docstrings for the module and all function definitions, obscuring purpose, arguments, and return types. | Added comprehensive docstrings to the module and each function detailing their functionality, parameters, and return types. |
| **C0103**: `invalid-name` (`logConflicts`) | Pylint | Naming Style (Convention) | 39 | Function name `logConflicts` violates PEP 8 snake_case naming conventions for functions. | Renamed function to `log_conflicts`. |
| **W0603**: `global-statement` & **C0103**: `invalid-name` (`next_reservation`) | Pylint | Design / Code Quality (Warning) | 9, 12 | Use of `global next_reservation` to mutate a scalar integer across function calls; constant casing violation. | Encapsulated mutable state within a module-level dictionary `STATE = {"next_reservation": 1}`, removing the need for global reassignment statements. |
| **C0206**: `consider-using-dict-items` & **C0209**: `consider-using-f-string` | Pylint | Pythonic Idioms (Convention) | 13, 15 | Direct iteration by indexing keys (`reservations[r]`) and legacy `%s` string interpolation. | Iterated directly over values (`for res in reservations.values():`) and modernized formatting with Python f-strings (`f"{room_id} double-booked at {slot_str}"`). |
| **E501**: `line-too-long` & **C0301**: `line-too-long` | Flake8, Pylint | Style & Readability (Convention) | 14, 18, 40 | Lines exceeded standard maximum lengths (79 characters for Flake8, 100 characters for Pylint), reducing split-view readability. | Formatted dictionary definitions and string literals across multiple indented lines, strictly complying with the <= 79 character limit. |
| **E302** / **E305**: `expected 2 blank lines` & **F841**: `unused-variable` | Flake8, Pylint | Formatting & Dead Code (Style/Warning) | 11, 22, 46, 47, 49, 59 | Missing standard PEP 8 two blank lines between top-level functions and main execution guard; assigned variables `a`, `a_more`, `c` never read. | Enforced exactly two blank lines between top-level declarations, and eliminated dead variables by replacing them with `_` or utilizing them in output. |

---

## Verification Summary

| Static Analysis Tool | Baseline (Before) | Cleaned Version (After) | Status |
| :--- | :--- | :--- | :--- |
| **Bandit** | 1 High (`B605`), 1 Low (`B110`) | **0 issues** across all severity levels | **PASSED** |
| **Pylint** | **5.60 / 10.00** | **10.00 / 10.00** (+4.40 improvement) | **PASSED** |
| **Flake8** | 13 style/syntax violations | **0 violations** (completely clean) | **PASSED** |
