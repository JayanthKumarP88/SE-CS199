"""Branch Coverage Test Suite for amusement_park_ride_access.py.

This suite is systematically designed to evaluate every decision branch,
conditional statement, and boundary condition to achieve 100% branch coverage:
- Type checking & negative fee guards (ValueError)
- Group open status (True vs False)
- All ride types: 'roller_coaster', 'water_ride', 'family', and invalid ride types
- Height validation: <= 0, 0 < height < 120, and height >= 120
- Health warnings: on roller coaster (triggers break & zero total) vs other rides
- Patron age classification: child discount (60%) vs adult full price
- Express pass fast lane fee: applied vs omitted
- Final status evaluation: SAFETY_AUDIT (> 4 rejections), ZERO_ADMISSIONS (0 revenue), COMPLETED
- Restraint streams: empty/None, streak >= 2 (EMERGENCY_LOCK), and alternating/safe streaks
"""

import pytest
from amusement_park_ride_access import (
    process_ride_admissions,
    inspect_safety_restraints,
)


class TestInputValidationBranches:
    """Test decision branches in input argument validation."""

    def test_non_list_groups_branch(self):
        """Branch: not isinstance(groups, list) is True."""
        with pytest.raises(ValueError, match="Invalid groups list or pass fee"):
            process_ride_admissions(None, 5.0)

        with pytest.raises(ValueError, match="Invalid groups list or pass fee"):
            process_ride_admissions({"not": "a list"}, 5.0)

    def test_negative_pass_fee_branch(self):
        """Branch: express_pass_fee < 0 is True."""
        with pytest.raises(ValueError, match="Invalid groups list or pass fee"):
            process_ride_admissions([], -0.01)

    def test_valid_empty_groups_zero_revenue_branch(self):
        """Branch: valid empty groups list and fee >= 0 -> ZERO_ADMISSIONS."""
        result = process_ride_admissions([], 10.0)
        assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


class TestGroupAndRideTypeBranches:
    """Test group loop control flow and ride type selection branches."""

    def test_group_not_open_skipped_branch(self):
        """Branch: not group.get('is_open') is True (skipped)."""
        groups = [
            {"is_open": False, "ride_type": "family", "patrons": [{"height_cm": 150}]},
            {"ride_type": "family", "patrons": [{"height_cm": 150}]},  # default False
        ]
        result = process_ride_admissions(groups, 5.0)
        assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}

    def test_roller_coaster_ride_type_branch(self):
        """Branch: ride_type == 'roller_coaster' (base_ticket = 25.0)."""
        groups = [
            {
                "is_open": True,
                "ride_type": "roller_coaster",
                "patrons": [{"height_cm": 140, "is_child": False}],
            }
        ]
        result = process_ride_admissions(groups, 0.0)
        assert result == {"total_revenue": 25.0, "status": "COMPLETED"}

    def test_water_ride_ride_type_branch(self):
        """Branch: ride_type == 'water_ride' (base_ticket = 18.0)."""
        groups = [
            {
                "is_open": True,
                "ride_type": "water_ride",
                "patrons": [{"height_cm": 140, "is_child": False}],
            }
        ]
        result = process_ride_admissions(groups, 0.0)
        assert result == {"total_revenue": 18.0, "status": "COMPLETED"}

    def test_family_ride_ride_type_branch(self):
        """Branch: ride_type == 'family' (base_ticket = 10.0)."""
        groups = [
            {
                "is_open": True,
                "ride_type": "family",
                "patrons": [{"height_cm": 140, "is_child": False}],
            }
        ]
        result = process_ride_admissions(groups, 0.0)
        assert result == {"total_revenue": 10.0, "status": "COMPLETED"}

    def test_default_ride_type_branch(self):
        """Branch: ride_type omitted defaults to 'family'."""
        groups = [
            {
                "is_open": True,
                "patrons": [{"height_cm": 140, "is_child": False}],
            }
        ]
        result = process_ride_admissions(groups, 0.0)
        assert result == {"total_revenue": 10.0, "status": "COMPLETED"}

    def test_invalid_ride_type_else_branch(self):
        """Branch: unrecognized ride_type triggers else (rejected_patrons += 1, continue)."""
        groups = [
            {
                "is_open": True,
                "ride_type": "haunted_house",
                "patrons": [{"height_cm": 150}],
            }
        ]
        result = process_ride_admissions(groups, 5.0)
        assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


class TestPatronValidationAndPricingBranches:
    """Test patron eligibility, height, health warnings, and tickets."""

    def test_patron_invalid_height_non_positive_branch(self):
        """Branch: height_cm <= 0 triggers rejection and continue."""
        groups = [
            {
                "is_open": True,
                "ride_type": "family",
                "patrons": [
                    {"height_cm": 0},
                    {"height_cm": -10},
                ],
            }
        ]
        result = process_ride_admissions(groups, 0.0)
        assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}

    def test_health_warning_roller_coaster_break_branch(self):
        """Branch: has_health_warning True and ride_type == 'roller_coaster' -> break & group_total = 0.0."""
        groups = [
            {
                "is_open": True,
                "ride_type": "roller_coaster",
                "has_fast_lane": True,
                "patrons": [
                    {"height_cm": 150, "health_warning": True},
                    {"height_cm": 150, "health_warning": False},  # Unreachable due to break
                ],
            }
        ]
        result = process_ride_admissions(groups, 10.0)
        # Note: break exits patrons loop; has_fast_lane still adds fee
        assert result == {"total_revenue": 10.0, "status": "COMPLETED"}

    def test_health_warning_non_roller_coaster_continue_branch(self):
        """Branch: has_health_warning True and ride_type != 'roller_coaster' -> group_total += 0.0."""
        groups = [
            {
                "is_open": True,
                "ride_type": "water_ride",
                "patrons": [
                    {"height_cm": 150, "health_warning": True},
                    {"height_cm": 150, "health_warning": False, "is_child": False},
                ],
            }
        ]
        result = process_ride_admissions(groups, 0.0)
        assert result == {"total_revenue": 18.0, "status": "COMPLETED"}

    def test_under_height_limit_branch(self):
        """Branch: height_cm < 120 triggers rejection and continue."""
        groups = [
            {
                "is_open": True,
                "ride_type": "family",
                "patrons": [
                    {"height_cm": 119},
                ],
            }
        ]
        result = process_ride_admissions(groups, 0.0)
        assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}

    def test_exact_height_limit_boundary(self):
        """Boundary test: height_cm == 120 is allowed."""
        groups = [
            {
                "is_open": True,
                "ride_type": "family",
                "patrons": [
                    {"height_cm": 120, "is_child": False},
                ],
            }
        ]
        result = process_ride_admissions(groups, 0.0)
        assert result == {"total_revenue": 10.0, "status": "COMPLETED"}

    def test_child_discount_branch(self):
        """Branch: is_child True -> base_ticket * 0.60."""
        groups = [
            {
                "is_open": True,
                "ride_type": "water_ride",  # base 18.0 * 0.60 = 10.80
                "patrons": [
                    {"height_cm": 130, "is_child": True},
                ],
            }
        ]
        result = process_ride_admissions(groups, 0.0)
        assert result == {"total_revenue": 10.8, "status": "COMPLETED"}

    def test_fast_lane_flag_branches(self):
        """Branches: has_fast_lane True vs False."""
        # True branch
        groups_fast = [
            {
                "is_open": True,
                "ride_type": "family",
                "has_fast_lane": True,
                "patrons": [{"height_cm": 150, "is_child": False}],
            }
        ]
        res_fast = process_ride_admissions(groups_fast, 7.50)
        assert res_fast["total_revenue"] == 17.50

        # False branch (default)
        groups_regular = [
            {
                "is_open": True,
                "ride_type": "family",
                "has_fast_lane": False,
                "patrons": [{"height_cm": 150, "is_child": False}],
            }
        ]
        res_regular = process_ride_admissions(groups_regular, 7.50)
        assert res_regular["total_revenue"] == 10.00


class TestFinalStatusOutcomeBranches:
    """Test final status determination branches."""

    def test_safety_audit_strictly_greater_than_four(self):
        """Branch: rejected_patrons > 4 evaluates to True."""
        groups = [
            {
                "is_open": True,
                "ride_type": "family",
                "patrons": [
                    {"height_cm": 100},  # rej 1 (<120)
                    {"height_cm": 110},  # rej 2 (<120)
                    {"height_cm": -5},   # rej 3 (<=0)
                    {"height_cm": 150, "health_warning": True},  # rej 4
                    {"height_cm": 0},    # rej 5 (<=0)
                    {"height_cm": 160, "is_child": False},
                ],
            }
        ]
        result = process_ride_admissions(groups, 0.0)
        assert result == {"total_revenue": 10.0, "status": "SAFETY_AUDIT"}

    def test_exactly_four_rejections_not_safety_audit(self):
        """Boundary: rejected_patrons == 4 does NOT trigger SAFETY_AUDIT."""
        groups = [
            {
                "is_open": True,
                "ride_type": "family",
                "patrons": [
                    {"height_cm": 100},  # rej 1
                    {"height_cm": 110},  # rej 2
                    {"height_cm": -5},   # rej 3
                    {"height_cm": 0},    # rej 4
                    {"height_cm": 160, "is_child": False},
                ],
            }
        ]
        result = process_ride_admissions(groups, 0.0)
        assert result == {"total_revenue": 10.0, "status": "COMPLETED"}

    def test_zero_admissions_status_branch(self):
        """Branch: total_revenue == 0.0 and rejected_patrons <= 4 -> ZERO_ADMISSIONS."""
        groups = [
            {
                "is_open": True,
                "ride_type": "family",
                "patrons": [],
            }
        ]
        result = process_ride_admissions(groups, 0.0)
        assert result == {"total_revenue": 0.0, "status": "ZERO_ADMISSIONS"}


class TestSafetyRestraintsBranches:
    """Test inspect_safety_restraints branches and loops."""

    def test_empty_and_falsy_restraints_branch(self):
        """Branch: not restraint_streams is True."""
        assert inspect_safety_restraints([]) == "NO_DATA"
        assert inspect_safety_restraints(None) == "NO_DATA"

    def test_sensor_emergency_lock_branch(self):
        """Branch: unlatched_streak >= 2 triggers EMERGENCY_LOCK."""
        # Consecutive zeros across streams
        streams = [
            [1, 1, 1],
            [0, 0, 1],  # two consecutive zeros
        ]
        assert inspect_safety_restraints(streams) == "EMERGENCY_LOCK"

    def test_sensor_val_non_zero_streak_reset_branch(self):
        """Branch: sensor_val != 0 resets streak to 0, ultimately returning SAFE."""
        streams = [
            [0, 1, 0, 1, 0],
            [1, 0, 1, 0],
        ]
        assert inspect_safety_restraints(streams) == "SAFE"

    def test_all_latched_sensors_safe(self):
        """Branch: all 1s stream -> SAFE."""
        streams = [[1, 1, 1, 1]]
        assert inspect_safety_restraints(streams) == "SAFE"
