"""
Unit tests for obstacle_avoider's get_front_distance() logic.

These test the pure detection logic directly, with no rclpy/ROS2 node
required — fast, no simulation needed, runs in CI on every push.

Covers the exact bug that was found by hand: an angle_min=-pi / angle_max=+pi
scan where "front" is the MIDDLE of the ranges array, not the ends.
"""

import math
import pytest
from front_distance import get_front_distance


INF = math.inf
NAN = math.nan
RANGE_MIN = 0.08
RANGE_MAX = 10.0


def make_ranges(size, front_value, filler=INF):
    """Build a ranges array of `size` with `front_value` placed at the
    center index (i.e. straight ahead, matching angle_min=-pi layout)."""
    ranges = [filler] * size
    ranges[size // 2] = front_value
    return ranges


def test_detects_wall_directly_ahead():
    ranges = make_ranges(360, front_value=0.5)
    result = get_front_distance(ranges, RANGE_MIN, RANGE_MAX)
    assert result == pytest.approx(0.5)


def test_ignores_readings_at_array_ends_behind_robot():
    # Values at index 0 and the last index are BEHIND the robot and should
    # NOT be picked up as "front" -- this is the original bug.
    ranges = [INF] * 360
    ranges[0] = 0.2      # behind the robot
    ranges[-1] = 0.2     # behind the robot
    ranges[180] = 3.0     # actually in front, further away
    result = get_front_distance(ranges, RANGE_MIN, RANGE_MAX)
    assert result == pytest.approx(3.0)


def test_returns_none_when_all_readings_invalid():
    ranges = [INF] * 360
    result = get_front_distance(ranges, RANGE_MIN, RANGE_MAX)
    assert result is None


def test_filters_out_nan_values():
    ranges = make_ranges(360, front_value=NAN)
    result = get_front_distance(ranges, RANGE_MIN, RANGE_MAX)
    assert result is None


def test_filters_out_values_outside_range_min_max():
    # A reading right at or beyond range_max should be excluded, not
    # treated as a valid (very far) distance.
    ranges = make_ranges(360, front_value=RANGE_MAX)
    result = get_front_distance(ranges, RANGE_MIN, RANGE_MAX)
    assert result is None


def test_filters_out_values_at_or_below_range_min():
    ranges = make_ranges(360, front_value=RANGE_MIN)
    result = get_front_distance(ranges, RANGE_MIN, RANGE_MAX)
    assert result is None


def test_picks_closest_of_multiple_valid_front_readings():
    ranges = [INF] * 360
    center = 360 // 2
    ranges[center - 5] = 1.2
    ranges[center] = 0.4
    ranges[center + 5] = 2.0
    result = get_front_distance(ranges, RANGE_MIN, RANGE_MAX)
    assert result == pytest.approx(0.4)


def test_empty_ranges_returns_none():
    result = get_front_distance([], RANGE_MIN, RANGE_MAX)
    assert result is None


def test_works_with_smaller_scan_resolution():
    # Confirms the fix generalizes: front is computed from len(ranges),
    # not hardcoded, so it stays correct if LiDAR resolution changes.
    ranges = make_ranges(72, front_value=0.9)  # e.g. 5-degree resolution
    result = get_front_distance(ranges, RANGE_MIN, RANGE_MAX)
    assert result == pytest.approx(0.9)


def test_window_does_not_pick_up_readings_outside_front_cone():
    ranges = [INF] * 360
    center = 360 // 2
    ranges[center + 25] = 0.3  # just outside the default +/-20 window
    result = get_front_distance(ranges, RANGE_MIN, RANGE_MAX)
    assert result is None
