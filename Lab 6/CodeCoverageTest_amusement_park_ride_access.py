"""Test suite for achieving 100% code (line) coverage on amusement_park_ride_access.py."""

import pytest
from amusement_park_ride_access import (
    process_ride_admissions,
    inspect_safety_restraints,
)


def test_invalid_groups_non_list():
    """Verify ValueError when groups is not a list."""
    with pytest.raises(ValueError, match="Invalid groups list or pass fee"):
        process_ride_admissions("not a list", 10.0)


def test_invalid_express_pass_fee_negative():
    """Verify ValueError when express_pass_fee is negative."""
    with pytest.raises(ValueError, match="Invalid groups list or pass fee"):
        process_ride_admissions([], -5.0)


def test_group_closed():
    """Verify that a closed group is skipped."""
    groups = [
        {
            "is_open": False,
            "ride_type": "family",
            "patrons": [{"height_cm": 150}],
        }
    ]
    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_ADMISSIONS"


def test_unknown_ride_type():
    """Verify rejection of patron with unknown ride type."""
    groups = [
        {
            "is_open": True,
            "ride_type": "unknown_coaster",
            "patrons": [{"height_cm": 150}],
        }
    ]
    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_ADMISSIONS"


def test_roller_coaster_with_health_warning_break():
    """Verify roller coaster breaks when a patron has a health warning."""
    groups = [
        {
            "is_open": True,
            "ride_type": "roller_coaster",
            "patrons": [
                {"height_cm": 160, "health_warning": True, "is_child": False}
            ],
        }
    ]
    result = process_ride_admissions(groups, 5.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_ADMISSIONS"


def test_water_ride_with_health_warning_and_fast_lane():
    """Verify water ride with health warning and fast lane fee."""
    groups = [
        {
            "is_open": True,
            "ride_type": "water_ride",
            "has_fast_lane": True,
            "patrons": [
                {"height_cm": 140, "health_warning": True, "is_child": False}
            ],
        }
    ]
    result = process_ride_admissions(groups, 12.0)
    assert result["total_revenue"] == 12.0
    assert result["status"] == "COMPLETED"


def test_invalid_height_and_under_height():
    """Verify rejection for height <= 0 and height < 120."""
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "patrons": [
                {"height_cm": 0, "health_warning": False, "is_child": False},
                {"height_cm": 110, "health_warning": False, "is_child": True},
            ],
        }
    ]
    result = process_ride_admissions(groups, 0.0)
    assert result["total_revenue"] == 0.0
    assert result["status"] == "ZERO_ADMISSIONS"


def test_child_and_adult_patrons_completed():
    """Verify ticket pricing for child and adult patrons."""
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "patrons": [
                {"height_cm": 130, "health_warning": False, "is_child": True},
                {"height_cm": 170, "health_warning": False, "is_child": False},
            ],
        }
    ]
    result = process_ride_admissions(groups, 0.0)
    assert result["total_revenue"] == 16.0  # 6.0 + 10.0
    assert result["status"] == "COMPLETED"


def test_safety_audit_status():
    """Verify SAFETY_AUDIT triggered when rejected_patrons > 4."""
    groups = [
        {
            "is_open": True,
            "ride_type": "family",
            "patrons": [
                {"height_cm": -1},
                {"height_cm": 0},
                {"height_cm": 90},
                {"height_cm": 100},
                {"height_cm": 110},
                {"height_cm": 150},
            ],
        }
    ]
    result = process_ride_admissions(groups, 0.0)
    assert result["status"] == "SAFETY_AUDIT"
    assert result["total_revenue"] == 10.0


def test_inspect_safety_restraints_no_data():
    """Verify NO_DATA when restraint_streams is empty or None."""
    assert inspect_safety_restraints([]) == "NO_DATA"
    assert inspect_safety_restraints(None) == "NO_DATA"


def test_inspect_safety_restraints_emergency_lock():
    """Verify EMERGENCY_LOCK when unlatched streak reaches 2."""
    streams = [[1, 0, 0, 1]]
    assert inspect_safety_restraints(streams) == "EMERGENCY_LOCK"


def test_inspect_safety_restraints_safe():
    """Verify SAFE when streaks are reset by latched sensors."""
    streams = [[1, 0, 1, 0, 1]]
    assert inspect_safety_restraints(streams) == "SAFE"
