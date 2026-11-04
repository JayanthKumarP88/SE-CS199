"""Main test module for amusement park ride access system.

Achieves 100% Code Coverage and 100% Branch Coverage.
"""

import pytest
from amusement_park_ride_access import (
    process_ride_admissions,
    inspect_safety_restraints,
)

# Import all tests from both suites so running pytest on test_amusement_park.py
# achieves comprehensive 100% line & branch coverage
from CodeCoverageTest_amusement_park_ride_access import *  # noqa: F401, F403
from BranchCoverageTest_amusement_park_ride_access import *  # noqa: F401, F403


def test_starter_example_compatibility():
    """Retain and verify the original starter example test case."""
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "has_fast_lane": False,
            "patrons": [
                {"height_cm": 150, "health_warning": False, "is_child": False}
            ],
        }
    ]
    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 10.0
    assert result["status"] == "COMPLETED"
