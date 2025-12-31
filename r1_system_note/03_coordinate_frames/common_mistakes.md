# Common Mistakes with Coordinate Frames

Even experienced roboticists make mistakes with coordinate frames. Here are the most common pitfalls and how to avoid them.

## Mistake 1: Confusing "From" and "To"

### The Error

**Wrong**:
```python
# Thinking: "I want to transform FROM world TO robot"
transform = get_transform("world", "robot")  # Actually: TO robot FROM world
point_robot = transform * point_world  # Wrong direction!
```

**Correct**:
```python
# T_world^robot transforms FROM world TO robot
transform = get_transform("world", "robot")  # T_world^robot
point_robot = transform * point_world  # Correct: world → robot
```

### How to Remember

- **T_A^B** means "TO B FROM A"
- Think: "Where is frame A relative to frame B?"
- The transform takes points IN frame A and gives points IN frame B

### Example

```python
# Robot is at (5, 0, 0) in world frame
T_world^robot = [1  0  0  -5]  # Robot 5m behind world origin
              [0  1  0   0]
              [0  0  1   0]
              [0  0  0   1]

# Point at (10, 0, 0) in world
point_world = [10, 0, 0, 1]

# Transform to robot frame
point_robot = T_world^robot * point_world = [5, 0, 0, 1]
# Point is 5m ahead of robot (correct!)
```

## Mistake 2: Wrong Transform Composition Order

### The Error

**Wrong**:
```python
# Want: T_A^C
T_A^C = T_A^B * T_B^C  # Wrong order!
```

**Correct**:
```python
# Chain: A → B → C
T_A^C = T_B^C * T_A^B  # Correct: apply B→C, then A→B
```

### How to Remember

- Read right to left: "First A→B, then B→C"
- Matrix multiplication: Rightmost transform applied first
- Visualize: Start at A, go through B, arrive at C

### Example

```python
# Robot base to end-effector
T_base^ee = get_transform("base", "end_effector")

# End-effector to tool
T_ee^tool = get_transform("end_effector", "tool")

# Base to tool (WRONG)
T_base^tool_wrong = T_base^ee * T_ee^tool  # Wrong!

# Base to tool (CORRECT)
T_base^tool = T_ee^tool * T_base^ee  # Correct order
```

## Mistake 3: Using Stale Transforms

### The Error

```python
# Get transform once
T_world^robot = get_transform("world", "robot")

# Use it later (robot has moved!)
point_robot = T_world^robot * point_world  # Using old transform!
```

### The Problem

- Robot moves continuously
- Transforms change over time
- Using old transform causes errors

### Solution

```python
# Always get latest transform
T_world^robot = get_latest_transform("world", "robot")
point_robot = T_world^robot * point_world

# Or use time-stamped lookup
target_time = rospy.Time.now()
T_world^robot = lookup_transform("world", "robot", target_time)
```

## Mistake 4: Mixing Units

### The Error

```python
# Transform in meters
T_camera^base = [1  0  0  0.5]  # 0.5 meters
                [0  1  0  0  ]
                [0  0  1  0  ]
                [0  0  0  1  ]

# Point in millimeters
point_camera = [1000, 0, 0, 1]  # 1000 mm = 1 m

# Result is wrong!
point_base = T_camera^base * point_camera  # Mixing units!
```

### Solution

**Standardize units**:
```python
# Convert everything to meters first
point_camera_m = point_camera_mm / 1000.0
point_base = T_camera^base * point_camera_m
```

**Or use consistent units throughout**:
- Choose: meters OR millimeters
- Document your choice
- Convert at boundaries (sensor interfaces, etc.)

## Mistake 5: Inconsistent Axis Conventions

### The Error

**Different parts of code use different conventions**:
- Some code: X forward, Y left, Z up
- Other code: X right, Y forward, Z up
- Result: Everything misaligned!

### Solution

**Establish conventions**:
- Document frame definitions
- Use standard conventions (e.g., REP-103 for ROS)
- Create frame definition document
- Validate transforms match conventions

**Example Convention**:
```
Robot Base Frame:
- X: Forward
- Y: Left
- Z: Up
- Right-handed
```

## Mistake 6: Forgetting Homogeneous Coordinates

### The Error

```python
# 3D point
point = [x, y, z]

# 4x4 transform
transform = [[R, t],
             [0, 1]]

# Wrong: dimensions don't match
result = transform * point  # Error!
```

### Solution

**Use homogeneous coordinates**:
```python
# 3D point as 4D homogeneous
point = [x, y, z, 1]  # Add 1 for translation

# Now it works
result = transform * point
result_3d = result[:3]  # Extract 3D part
```

## Mistake 7: Incorrect Rotation Representations

### The Error

**Mixing rotation representations**:
```python
# Quaternion
q = [w, x, y, z]

# Using as Euler angles
roll = q[0]  # Wrong! q[0] is w, not roll
```

### Solution

**Convert explicitly**:
```python
from scipy.spatial.transform import Rotation

# Quaternion to rotation matrix
R = Rotation.from_quat([x, y, z, w]).as_matrix()

# Rotation matrix to Euler
euler = Rotation.from_matrix(R).as_euler('xyz')
```

## Mistake 8: Not Handling Transform Failures

### The Error

```python
# Transform might not exist yet
T_world^robot = get_transform("world", "robot")
point_robot = T_world^robot * point_world  # Crashes if transform missing!
```

### Solution

**Handle errors gracefully**:
```python
try:
    T_world^robot = get_transform("world", "robot", timeout=1.0)
    point_robot = T_world^robot * point_world
except TransformException as e:
    # Use fallback or previous transform
    logger.warning(f"Transform unavailable: {e}")
    point_robot = use_last_known_transform(point_world)
```

## Mistake 9: Transform Tree Cycles

### The Error

**Creating circular dependencies**:
```
World → Robot → Camera → World  # Cycle!
```

### Solution

**Maintain tree structure**:
- Each frame has exactly one parent
- No cycles allowed
- Use transform library (e.g., tf2) that enforces this

## Mistake 10: Not Validating Transforms

### The Error

**Using invalid transforms**:
```python
# Rotation matrix not orthogonal
R = [[1, 0.1, 0],    # Not orthogonal!
     [0, 1, 0],
     [0, 0, 1]]

# Quaternion not normalized
q = [1.1, 0, 0, 0]  # ||q|| > 1!
```

### Solution

**Validate transforms**:
```python
def validate_rotation_matrix(R):
    assert np.allclose(R.T @ R, np.eye(3)), "Not orthogonal!"
    assert np.isclose(np.linalg.det(R), 1.0), "Not proper rotation!"

def validate_quaternion(q):
    norm = np.linalg.norm(q)
    assert np.isclose(norm, 1.0), f"Quaternion not normalized: {norm}"
```

## Debugging Tips

1. **Visualize**: Plot frames and transforms
2. **Test Inverses**: T * T^(-1) should be identity
3. **Check Units**: Verify consistent units
4. **Log Transforms**: Record transforms for debugging
5. **Use Tools**: ROS2 `tf2_echo`, `tf2_monitor` for debugging

## Best Practices

1. **Always specify frame names explicitly**
2. **Use transform libraries** (don't implement yourself)
3. **Document frame conventions**
4. **Validate transforms** before using
5. **Handle time** properly (latest vs. interpolated)
6. **Test transforms** with known examples
7. **Use consistent units** throughout
8. **Handle errors** gracefully

## Next Steps

- Review [Frames and Transforms](./frames_and_transforms.md) fundamentals
- Learn about [Sensors](../04_sensors/) and their frame conventions


