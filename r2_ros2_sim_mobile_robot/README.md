# ROS2 Mobile Robot Simulation

A complete ROS2 simulation setup for a differential drive mobile robot using Gazebo.

## Project Structure

```
r2_ros2_sim_mobile_robot/
│
├── README.md
│
├── robot_description/
│   ├── urdf/
│   │   └── mobile_robot.urdf
│   └── meshes/
│
├── sim/
│   ├── gazebo_worlds/
│   │   └── empty.world
│   └── launch/
│       └── sim.launch.py
│
├── ros2_ws/
│   └── src/
│       └── mobile_robot/
│           ├── mobile_robot/
│           │   ├── __init__.py
│           │   ├── teleop_node.py
│           │   ├── simple_controller.py
│           │   └── logger_node.py
│           │
│           ├── launch/
│           │   └── bringup.launch.py
│           │
│           ├── package.xml
│           └── setup.py
│
└── diagrams/
    ├── system_overview.png
    └── ros_graph.png
```

## Overview

This project demonstrates a complete ROS2 setup for simulating and controlling a mobile robot:

- **Robot Description**: URDF file defining the robot's physical properties
- **Simulation**: Gazebo world and launch files
- **Control**: ROS2 nodes for teleoperation, control, and logging
- **Integration**: Launch files to bring up the entire system

## Prerequisites

- ROS2 (Humble or later recommended)
- Gazebo Classic or Ignition Gazebo
- Python 3.8+
- Required ROS2 packages:
  - `geometry_msgs`
  - `sensor_msgs`
  - `nav_msgs`
  - `std_msgs`
  - `rclpy`

## Quick Start

### 1. Build the ROS2 Workspace

```bash
cd ros2_ws
colcon build
source install/setup.bash
```

### 2. Launch Simulation

```bash
ros2 launch sim sim.launch.py
```

This will:
- Start Gazebo with the empty world
- Spawn the mobile robot
- Launch all control nodes

### 3. Control the Robot

Use the teleoperation node to control the robot:

```bash
ros2 run mobile_robot teleop_node
```

Or use the controller node for autonomous movement:

```bash
ros2 run mobile_robot simple_controller
```

### 4. Monitor Logs

The logger node will publish robot state information:

```bash
ros2 topic echo /robot/log
```

## Nodes

### teleop_node.py

Keyboard teleoperation node that publishes velocity commands to `/cmd_vel`.

**Topics:**
- Publishes: `/cmd_vel` (geometry_msgs/Twist)

**Usage:**
- Arrow keys: Move forward/backward
- Left/Right arrows: Rotate

### simple_controller.py

Simple controller node that subscribes to velocity commands and controls the robot.

**Topics:**
- Subscribes: `/cmd_vel` (geometry_msgs/Twist)
- Publishes: `/wheel_left/cmd_vel`, `/wheel_right/cmd_vel` (std_msgs/Float64)

### logger_node.py

Logging node that monitors robot state and publishes logs.

**Topics:**
- Subscribes: `/odom` (nav_msgs/Odometry)
- Publishes: `/robot/log` (std_msgs/String)

## Launch Files

### sim.launch.py

Main simulation launch file that:
1. Starts Gazebo with the empty world
2. Spawns the robot from URDF
3. Launches all control nodes

### bringup.launch.py

Brings up all ROS2 nodes (teleop, controller, logger) without the simulation.

## Robot Description

The robot is defined in `robot_description/urdf/mobile_robot.urdf` as a differential drive robot with:
- Base link with inertial properties
- Two wheels (left and right)
- Caster wheel for stability
- Gazebo plugins for physics and control

## Topics Overview

- `/cmd_vel`: Velocity commands (geometry_msgs/Twist)
- `/odom`: Odometry data (nav_msgs/Odometry)
- `/wheel_left/cmd_vel`: Left wheel command (std_msgs/Float64)
- `/wheel_right/cmd_vel`: Right wheel command (std_msgs/Float64)
- `/robot/log`: Robot state logs (std_msgs/String)

## Development

### Adding New Nodes

1. Create your node in `ros2_ws/src/mobile_robot/mobile_robot/`
2. Update `setup.py` to include the new entry point
3. Rebuild: `cd ros2_ws && colcon build`

### Modifying Robot Description

Edit `robot_description/urdf/mobile_robot.urdf` and restart the simulation.

## Troubleshooting

- **Gazebo doesn't start**: Ensure Gazebo is installed and `GAZEBO_MODEL_PATH` is set
- **Nodes not found**: Make sure you've sourced the workspace: `source install/setup.bash`
- **URDF errors**: Check the URDF file with `check_urdf mobile_robot.urdf`

## License

This project is provided as-is for educational purposes.
