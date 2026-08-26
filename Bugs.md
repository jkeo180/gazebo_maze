# Bug Log — obstacle_avoider.py

## Symptom
Robot drove straight into walls in the maze instead of detecting them and turning.
Console repeatedly logged "Path clear, moving forward" even when a wall was directly ahead.

## Investigation
Confirmed LiDAR itself was working (`ros2 topic echo /scan --once` showed real,
non-inf range values). So the sensor was fine — the bug was in how the data
was being used, not the sensor.

## Bug 1 — Wrong front-window indices (logic bug)
**Root cause:** `angle_min = -π` and `angle_max = π` for this LiDAR, meaning the
scan wraps at ±180°. That puts index `0` and the last index of `ranges[]`
**behind** the robot, not in front of it. "Straight ahead" (0°) is actually the
**middle** index of the array.
**Original code:** `front_ranges = ranges[0:20] + ranges[-20:]` — always checked
behind the robot.
**Fix:** compute the front index from the array length directly:
```python
front_index = len(ranges) // 2
front_ranges = ranges[front_index - 20 : front_index + 20]
```
This stays correct even if the LiDAR's resolution (point count) changes later.

## Bug 2 — Node never built (build-config bug)
**Root cause:** `obstacle_avoider.py` existed as a file, but was never added to
`entry_points` / `console_scripts` in `setup.py`. ROS2 had no way to know it
should be built into a runnable executable.
**Symptom:** `ros2 run py_pubsub obstacle_avoider` → `No executable found`
**Fix:** added `'obstacle_avoider = py_pubsub.obstacle_avoider:main',` to
`entry_points` in `src/py_pubsub/setup.py`, then rebuilt.

## Bug 3 — File in wrong directory (packaging bug)
**Root cause:** even after registering the entry point, the file itself was
sitting at the top level of the repo instead of inside the actual Python
package folder (`src/py_pubsub/py_pubsub/`), so Python's import system
couldn't find the module.
**Symptom:** `ModuleNotFoundError: No module named 'py_pubsub.obstacle_avoider'`
**Fix:** `cp obstacle_avoider.py src/py_pubsub/py_pubsub/obstacle_avoider.py`,
rebuilt, re-sourced.

## Outcome
Robot correctly detects walls ahead and turns; completed the maze successfully
after all three fixes were applied in sequence.

## Takeaway
Three independent bug classes stacked on top of each other — a logic error,
a build-configuration gap, and a packaging/path error — each masking whether
the previous fix had actually taken effect. Isolating them one layer at a
time (confirm sensor data → confirm logic → confirm build → confirm import
path) was what made this solvable instead of just "it doesn't work."