# Frames and Transforms

Coordinate frames and transformations are fundamental to robotics. Everything a robot perceives and acts upon must be expressed in consistent coordinate systems.

## What is a Coordinate Frame?

A **coordinate frame** (or reference frame) defines:
- **Origin**: A point in space (0, 0, 0)
- **Axes**: Three orthogonal directions (X, Y, Z)
- **Orientation**: How axes are oriented (right-handed convention)

## Common Frames in Robotics

### World Frame (Global Frame)
- **Symbol**: `{W}` or `{world}`
- **Purpose**: Fixed reference for entire environment
- **Characteristics**: 
  - Immutable (doesn't move)
  - Often aligned with gravity (Z up or down)
  - Used for global planning

### Robot Base Frame
- **Symbol**: `{B}` or `{base}`
- **Purpose**: Attached to robot's base
- **Characteristics**:
  - Moves with robot
  - Origin typically at robot center or mounting point
  - X often forward, Y left, Z up

### Sensor Frames
- **Camera Frame**: `{C}` - At camera optical center
- **LiDAR Frame**: `{L}` - At LiDAR origin
- **IMU Frame**: `{I}` - At IMU center
- **Purpose**: Where sensor data is measured

### End-Effector Frame
- **Symbol**: `{E}` or `{ee}`
- **Purpose**: At robot's tool/gripper
- **Characteristics**: Moves with end-effector

### Object Frames
- **Symbol**: `{O}` or `{obj}`
- **Purpose**: Attached to objects in environment
- **Characteristics**: Move with objects

## Transformations

A **transform** describes the relationship between two frames:
- **Translation**: Position offset
- **Rotation**: Orientation difference

### Transform Notation

**T_A^B**: Transform from frame A to frame B
- Reads as: "Transform TO B FROM A"
- Represents: Where frame A is relative to frame B

### Homogeneous Transforms

A transform combines translation and rotation:

```
T = [R  t]   where R is 3x3 rotation matrix
    [0  1]         t is 3x1 translation vector
```

**Properties**:
- 4x4 matrix
- Invertible: T_B^A = (T_A^B)^(-1)
- Composable: T_A^C = T_B^C * T_A^B

## Representing Rotations

### Rotation Matrix
- **3x3 orthogonal matrix**
- **Properties**: R^T * R = I, det(R) = 1
- **Pros**: Direct, no singularities
- **Cons**: 9 parameters (redundant)

### Euler Angles
- **Roll, Pitch, Yaw (RPY)**
- **Pros**: Intuitive, compact (3 parameters)
- **Cons**: Gimbal lock, order-dependent

### Quaternions
- **4 parameters**: (w, x, y, z) where w² + x² + y² + z² = 1
- **Pros**: No singularities, efficient
- **Cons**: Less intuitive, double cover (q and -q represent same rotation)

### Axis-Angle
- **Axis**: Unit vector
- **Angle**: Rotation amount
- **Pros**: Intuitive for small rotations
- **Cons**: Singularity at 180°

## Transform Operations

### Applying a Transform

**Point transformation**:
```
p_B = T_A^B * p_A
```
Point p in frame A → point in frame B

**Pose transformation**:
```
T_C^B = T_A^B * T_C^A
```
Compose transforms: A→B then C→A gives C→B

### Inverse Transform

```
T_B^A = (T_A^B)^(-1)
```

For homogeneous transforms:
```
T^(-1) = [R^T  -R^T*t]
         [0    1     ]
```

## Transform Trees

Robots have a **tree structure** of frames:

```
World
  └── Robot Base
       ├── Camera
       ├── LiDAR
       ├── IMU
       └── End-Effector
            └── Tool
```

**Rules**:
- Each frame has one parent
- Transforms chain: T_world^tool = T_world^base * T_base^ee * T_ee^tool
- Tree structure prevents cycles

## Common Operations

### 1. Sensor Fusion

**Problem**: Multiple sensors in different frames

**Solution**: Transform all to common frame
```
point_camera → T_camera^base → point_base
point_lidar → T_lidar^base → point_base
→ Fuse in base frame
```

### 2. Planning in Different Frames

**World Frame**: Global path planning
**Robot Frame**: Local obstacle avoidance
**End-Effector Frame**: Manipulation tasks

Transform between as needed:
```
path_world → T_world^robot → path_robot
```

### 3. Control Commands

**Planning**: Commands in world frame
**Control**: Needs robot frame
**Actuators**: Need joint/actuator frames

Transform chain:
```
command_world → T_world^robot → command_robot → joint_space
```

## Calibration

### Why Calibration Matters

**Uncalibrated transforms cause**:
- Sensor misalignment
- Poor sensor fusion
- Navigation errors
- Manipulation failures

### Calibration Methods

**Hand-Eye Calibration**:
- Calibrate camera relative to robot
- Uses known patterns/objects
- Solves: AX = XB problem

**Multi-Sensor Calibration**:
- Calibrate all sensors to common frame
- Uses overlapping fields of view
- Optimization-based

**Kinematic Calibration**:
- Calibrate robot joint transforms
- Uses measured poses
- Improves accuracy

## Implementation Tips

### 1. Use a Transform Library

**ROS2**: `tf2` (Transform Library 2)
- Maintains transform tree
- Handles time synchronization
- Efficient lookups

**Python**: `scipy.spatial.transform`, `transforms3d`
**C++**: Eigen, `tf2` in ROS2

### 2. Consistent Conventions

- **Right-handed coordinate system**
- **Standard axis conventions** (e.g., REP-103 for ROS)
- **Document frame definitions**

### 3. Handle Time

**Problem**: Frames move over time

**Solution**: 
- Store transforms with timestamps
- Interpolate for query time
- Use latest transform if interpolation not needed

### 4. Validate Transforms

- Check rotation matrix properties (orthogonal, det=1)
- Verify quaternion normalization
- Test inverse: T * T^(-1) = I
- Validate transform chains

## Common Pitfalls

1. **Frame Confusion**: Mixing up "from" and "to"
2. **Wrong Order**: T_A^C ≠ T_B^C * T_A^B (order matters!)
3. **Time Stamps**: Using stale transforms
4. **Units**: Mixing meters and millimeters
5. **Conventions**: Inconsistent axis definitions

## Next Steps

- Read about [Common Mistakes](./common_mistakes.md) to avoid errors
- Learn about [Sensors](../04_sensors/) and their frame conventions


