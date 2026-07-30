#!/bin/bash

# Updated topic name to match your specific blue car
TOPIC="/model/vehicle_blue/cmd_vel"

for i in {1..4}
do
  echo "Step $i: Moving Forward"
  ros2 topic pub --once $TOPIC geometry_msgs/msg/Twist "{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
  sleep 2

  echo "Step $i: Stopping"
  ros2 topic pub --once $TOPIC geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
  sleep 1

  echo "Step $i: Turning"
  ros2 topic pub --once $TOPIC geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.0}}"
  sleep 1.5
done

echo "Square Finished!"

