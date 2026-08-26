"""
Pure LiDAR front-distance detection logic, with no ROS2/rclpy dependency.

Kept separate from obstacle_avoider.py (the ROS2 node) on purpose: this lets
the actual decision logic be unit tested directly and quickly, without
needing rclpy installed or a simulator running -- important for running
these tests in CI.
"""

import math


def get_front_distance(ranges, range_min, range_max, window=20):
    """
    Given a full LiDAR ranges array (assumed angle_min=-pi, angle_max=+pi,
    i.e. index 0 and the last index point BEHIND the robot and the middle
    index points straight ahead), return the closest valid distance within
    +/- `window` samples of straight ahead.

    Returns None if there are no valid (finite, in-range) readings in that
    window -- callers should treat None as "can't see," not "path clear."
    """
    if not ranges:
        return None

    front_index = len(ranges) // 2
    front_ranges = ranges[front_index - window: front_index + window]

    valid_ranges = [
        distance
        for distance in front_ranges
        if math.isfinite(distance) and range_min < distance < range_max
    ]

    if not valid_ranges:
        return None

    return min(valid_ranges)
