GitHub README
ROS2 Autonomous Maze Robot
Overview

This project is an autonomous differential-drive robot built using ROS 2 Jazzy and Gazebo Sim. The robot uses LiDAR and odometry to navigate through a maze while avoiding collisions using a finite-state control system.

The goal of this project was not only to build a working robot, but to gain a deeper understanding of robotics simulation, physics, and debugging.

Demo

🎥 Video
video link:

📷 Screenshots

Robot navigating the maze
Gazebo simulation
LiDAR visualization
ROS2 terminal output
Features
Differential drive robot
ROS2 Jazzy
Gazebo Sim
LiDAR sensor
Odometry
Wall avoidance controller
Finite State Machine
Autonomous maze navigation
Technologies Used
Python
ROS2 Jazzy
Gazebo Sim
SDF
Linux (WSL)
Git
What I Learned

This project became much more than writing a controller.

During development I learned how to debug:

Robot physics
Joint configuration
Wheel orientation
Wheel inertia
Collision geometry
Differential drive plugins
Odometry
LiDAR configuration
ROS2 publishers/subscribers
Gazebo simulation issues
SDF model structure

Many of the problems required isolating a single variable, testing a hypothesis, observing the results, and repeating until the robot behaved correctly.

Challenges

Some of the biggest challenges included:

Wheels separating from the chassis
Incorrect wheel axes
Incorrect inertia values
Robot bucking under acceleration
Robot detecting walls too early
Gazebo GUI issues
XML/SDF debugging
Physics tuning

Each issue provided a better understanding of how robot simulation works.

Future Improvements
Improve wheel geometry
Replace wall avoidance with SLAM
Add Nav2 navigation
Implement waypoint navigation
Add camera-based perception
Tune physics for smoother motion
Project Status

✅ MVP Complete

The robot successfully completes the maze autonomously.

Future work will focus on improving simulation realism and expanding navigation capabilities.
