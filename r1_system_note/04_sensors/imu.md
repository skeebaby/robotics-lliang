# IMU Sensors

IMU (Inertial Measurement Unit) measures the robot's motion and orientation using accelerometers and gyroscopes, and often includes magnetometers.

## What is an IMU?

An IMU typically contains:
- **Accelerometer**: Measures linear acceleration
- **Gyroscope**: Measures angular velocity
- **Magnetometer** (optional): Measures magnetic field (compass)

## IMU Components

### Accelerometer
**Measures**: Linear acceleration (including gravity)

**Axes**: 3-axis (X, Y, Z)

**Output**: Acceleration in m/s²

**Uses**:
- Detect motion
- Estimate orientation (gravity direction)
- Measure linear acceleration

**Limitations**:
- Can't distinguish gravity from acceleration
- Drift over time
- Noise and bias

### Gyroscope
**Measures**: Angular velocity

**Axes**: 3-axis (roll, pitch, yaw rates)

**Output**: Angular velocity in rad/s

**Uses**:
- Measure rotation rates
- Integrate to get orientation change
- Detect rotational motion

**Limitations**:
- Integration drift (bias accumulates)
- Scale factor errors
- Temperature sensitivity

### Magnetometer
**Measures**: Magnetic field strength and direction

**Axes**: 3-axis (X, Y, Z)

**Output**: Magnetic field in µT or normalized

**Uses**:
- Determine heading (compass)
- Correct gyroscope yaw drift
- Absolute orientation reference

**Limitations**:
- Affected by metal, electronics
- Local magnetic anomalies
- Not reliable indoors

## IMU Data

### Raw Measurements
```
Accelerometer: [ax, ay, az]  (m/s²)
Gyroscope:     [gx, gy, gz]  (rad/s)
Magnetometer:  [mx, my, mz]  (µT or normalized)
```

### Frequency
- **Standard**: 100-1000 Hz
- **High-rate**: Up to 8 kHz
- **Trade-off**: Higher rate = more data, better for fast motion

### Coordinate Frame
- **IMU Frame**: At sensor center
- **Convention**: 
  - X: Forward/Right
  - Y: Left/Forward
  - Z: Up
- **Transform**: T_base^imu (calibrated)

## Orientation Estimation

### Problem
IMU doesn't directly measure orientation, must estimate from:
- Accelerometer: Gravity direction (pitch, roll)
- Magnetometer: Magnetic north (yaw)
- Gyroscope: Integrate angular velocity

### Methods

#### Complementary Filter
**Simple fusion of accelerometer and gyroscope**:
```
orientation = α * (orientation + gyro * dt) + (1-α) * accel_orientation
```
- **α**: Tuning parameter (typically 0.98)
- **Pros**: Simple, fast
- **Cons**: Not optimal, requires tuning

#### Kalman Filter
**Optimal estimation under assumptions**:
- Models sensor noise
- Combines predictions with measurements
- **Pros**: Optimal (under assumptions), handles noise
- **Cons**: More complex, requires tuning

#### Madgwick/Mahony Filter
**Gradient descent-based**:
- Fuses accelerometer, gyroscope, magnetometer
- **Pros**: Good performance, moderate complexity
- **Cons**: Requires tuning

#### Extended Kalman Filter (EKF)
**For non-linear systems**:
- Used in sensor fusion (IMU + other sensors)
- **Pros**: Handles non-linearity, optimal
- **Cons**: Complex, computationally expensive

## Common Applications

### Attitude Estimation
**Goal**: Determine robot orientation (roll, pitch, yaw)

**Process**:
1. Read accelerometer (gravity direction)
2. Read magnetometer (heading)
3. Fuse with gyroscope (smooth, high-rate)
4. Output: Quaternion or Euler angles

### Dead Reckoning
**Goal**: Estimate position from IMU

**Process**:
1. Integrate acceleration (with gravity removal) → velocity
2. Integrate velocity → position
3. **Problem**: Drift accumulates quickly
4. **Solution**: Combine with other sensors (GPS, odometry)

### Motion Detection
**Goal**: Detect if robot is moving

**Methods**:
- Check if acceleration > threshold
- Check if angular velocity > threshold
- **Use**: Wake up other sensors, detect impacts

### Vibration Analysis
**Goal**: Monitor robot health

**Process**:
1. Analyze acceleration frequencies
2. Detect anomalies
3. **Use**: Fault detection, maintenance

## Sensor Fusion

### IMU + Odometry
**Purpose**: Improve odometry accuracy

**Benefits**:
- IMU provides orientation
- Odometry provides position
- Together: Better pose estimate

### IMU + GPS
**Purpose**: Navigation when GPS unavailable

**Benefits**:
- GPS: Absolute position (when available)
- IMU: High-rate motion (when GPS lost)
- Together: Continuous navigation

### IMU + Camera (Visual-Inertial)
**Purpose**: Robust SLAM/odometry

**Benefits**:
- Camera: Scale, visual features
- IMU: High-rate motion, scale
- Together: Robust to visual failures

### IMU + LiDAR
**Purpose**: Motion compensation for LiDAR

**Benefits**:
- LiDAR: 3D structure
- IMU: Motion during scan
- Together: Undistorted point clouds

## Calibration

### Accelerometer Calibration
**Purpose**: Remove bias and scale errors

**Method**:
1. Place IMU in known orientations
2. Measure outputs
3. Solve for bias and scale factors

**Parameters**:
- Bias: [bx, by, bz]
- Scale: [sx, sy, sz]
- Misalignment: 3x3 matrix

### Gyroscope Calibration
**Purpose**: Remove bias (critical for integration)

**Method**:
1. Keep IMU stationary
2. Measure outputs (should be zero)
3. Average = bias

**Parameters**:
- Bias: [bx, by, bz] (most critical)
- Scale: [sx, sy, sz]

### Magnetometer Calibration
**Purpose**: Remove hard/soft iron effects

**Method**:
1. Rotate IMU in all orientations
2. Fit ellipsoid to measurements
3. Transform to sphere

**Parameters**:
- Bias: [bx, by, bz]
- Scale: [sx, sy, sz]
- Misalignment: 3x3 matrix

### Extrinsic Calibration
**Purpose**: Determine IMU pose relative to robot

**Method**:
- Known motion (rotation/translation)
- Optimization with other sensors
- Hand-eye calibration

## Challenges

### Drift
**Problem**: Integration errors accumulate

**Gyroscope Drift**:
- Bias causes orientation drift
- **Impact**: Orientation error grows over time
- **Solution**: Fuse with accelerometer/magnetometer

**Accelerometer Drift**:
- Double integration → position drift
- **Impact**: Position error grows quadratically
- **Solution**: Reset with absolute measurements (GPS, landmarks)

### Noise
**Problem**: Sensor measurements are noisy

**Impact**: 
- Orientation jitter
- Position estimation errors

**Solutions**:
- Filtering (low-pass, Kalman)
- Averaging
- Higher quality sensors

### Bias
**Problem**: Sensors have constant offset

**Impact**:
- Systematic errors
- Drift in integration

**Solutions**:
- Calibration
- Online bias estimation
- Temperature compensation

### Temperature Sensitivity
**Problem**: Sensor properties change with temperature

**Impact**:
- Bias changes
- Scale factor changes

**Solutions**:
- Temperature compensation
- Calibration at multiple temperatures

### Magnetic Interference
**Problem**: Metal, electronics affect magnetometer

**Impact**:
- Incorrect heading
- Unreliable yaw

**Solutions**:
- Calibration
- Use gyroscope for short-term yaw
- Don't rely solely on magnetometer

## Integration with Robot System

### Data Flow
```
IMU → Raw Measurements → Filtering → 
Orientation Estimation → Sensor Fusion → State Estimation
```

### Real-time Requirements
- **Frequency**: 100-1000 Hz
- **Latency**: < 10ms (for control)
- **Deterministic**: Predictable timing

### Coordinate Frames
- **IMU Frame**: Sensor frame
- **Transform**: T_base^imu
- **Output**: Usually in base or world frame

## Best Practices

1. **Calibrate Regularly**: Bias changes over time
2. **Handle Temperature**: Compensate for temperature effects
3. **Fuse with Other Sensors**: Don't rely solely on IMU
4. **Filter Noise**: Use appropriate filters
5. **Handle Failures**: IMU can fail, have fallbacks
6. **Understand Limitations**: IMU drifts, use appropriately
7. **Synchronize**: Align timestamps with other sensors

## IMU Specifications

### Consumer Grade
- **Cost**: $10-100
- **Accuracy**: Moderate
- **Use**: Hobby projects, basic applications

### Industrial Grade
- **Cost**: $100-1000
- **Accuracy**: Good
- **Use**: Professional robots, drones

### Tactical Grade
- **Cost**: $1000-10000
- **Accuracy**: Very high
- **Use**: Navigation, precision applications

## Next Steps

- Learn about [Cameras](./camera.md) for visual sensing
- Understand [LiDAR](./lidar.md) for 3D sensing
- Review [Coordinate Frames](../03_coordinate_frames/frames_and_transforms.md) for IMU integration
- Explore [Control Systems](../05_control/) that use IMU data


