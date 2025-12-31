# R1 Robot System Notes

This documentation provides a comprehensive guide to understanding robot systems, from basic concepts to advanced implementation details.

## Table of Contents

1. [Overview](./01_overview/)
   - [What is a Robot?](./01_overview/what_is_a_robot.md)
   - [Autonomy Levels](./01_overview/autonomy_levels.md)

2. [System Architecture](./02_system_architecture/)
   - [High-Level Pipeline](./02_system_architecture/high_level_pipeline.md)
   - [Perception, Planning, and Control](./02_system_architecture/perception_planning_control.md)
   - [Real-time vs AI Systems](./02_system_architecture/realtime_vs_ai.md)

3. [Coordinate Frames](./03_coordinate_frames/)
   - [Frames and Transforms](./03_coordinate_frames/frames_and_transforms.md)
   - [Common Mistakes](./03_coordinate_frames/common_mistakes.md)

4. [Sensors](./04_sensors/)
   - [Camera](./04_sensors/camera.md)
   - [LiDAR](./04_sensors/lidar.md)
   - [IMU](./04_sensors/imu.md)

5. [Control](./05_control/)
   - [Classical Control](./05_control/classical_control.md)
   - [Learning-Based Control](./05_control/learning_based_control.md)

6. [Software Stack](./06_software_stack/)
   - [ROS2 Mental Model](./06_software_stack/ros2_mental_model.md)
   - [Simulation](./06_software_stack/simulation.md)
   - [Deployment](./06_software_stack/deployment.md)

## Quick Start

If you're new to robotics, start with the [Overview](./01_overview/what_is_a_robot.md) section to understand fundamental concepts.

For developers working on robot systems, the [System Architecture](./02_system_architecture/) section provides the foundation for understanding how components interact.

## Diagrams

Visual references are available in the [diagrams](./diagrams/) directory:
- `robot_pipeline.png` - High-level system pipeline
- `ros_graph.png` - ROS2 node communication graph
- `frames.png` - Coordinate frame transformations

## Contributing

This documentation is designed to be a living resource. As the system evolves, these notes should be updated to reflect current practices and learnings.


