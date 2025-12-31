# LiDAR Sensors

LiDAR (Light Detection and Ranging) provides precise 3D point cloud data by measuring distances using laser light.

## How LiDAR Works

### Basic Principle
1. **Emit**: Laser pulse sent out
2. **Reflect**: Light bounces off objects
3. **Receive**: Sensor detects reflected light
4. **Measure**: Time-of-flight determines distance
5. **Repeat**: Scan in multiple directions

### Distance Calculation
```
distance = (speed_of_light * time_of_flight) / 2
```

## Types of LiDAR

### Mechanical Spinning LiDAR
- **Mechanism**: Rotating mirror/prism
- **Coverage**: 360° horizontal, limited vertical
- **Examples**: Velodyne VLP-16, Ouster OS1
- **Pros**: Full 360° coverage, high resolution
- **Cons**: Moving parts, expensive, large

### Solid-State LiDAR
- **Mechanism**: No moving parts, electronic scanning
- **Coverage**: Limited field of view
- **Examples**: Ouster OS0, Innoviz
- **Pros**: More reliable, smaller, cheaper
- **Cons**: Limited FOV, newer technology

### Flash LiDAR
- **Mechanism**: Illuminates entire scene at once
- **Coverage**: Wide FOV, limited range
- **Pros**: No moving parts, fast
- **Cons**: Lower resolution, shorter range

## LiDAR Specifications

### Range
- **Short-range**: < 50m (indoor, close obstacles)
- **Medium-range**: 50-200m (urban driving)
- **Long-range**: > 200m (highway, long-range detection)

### Resolution
- **Angular Resolution**: Minimum angle between beams
- **Point Density**: Points per unit area
- **Higher Resolution**: More detail, more data

### Field of View
- **Horizontal**: Typically 360° for spinning LiDAR
- **Vertical**: 15-40° typically
- **Solid-state**: Limited FOV (e.g., 120° x 25°)

### Frame Rate
- **Standard**: 10-20 Hz
- **High-speed**: Up to 100 Hz
- **Trade-off**: Higher rate = more data

## Point Cloud Data

### Structure
Each point contains:
- **Position**: (x, y, z) in LiDAR frame
- **Intensity**: Reflectance strength
- **Timestamp**: When point was captured
- **Ring/Channel**: Which laser (for multi-beam)

### Point Cloud Format
```
Point Cloud:
  - Points: N x 3 (or N x 4 with intensity)
  - Organized: Height x Width (like image)
  - Unorganized: List of points
```

### Data Size
- **Typical**: 100K-1M points per scan
- **Size**: ~1-10 MB per scan (uncompressed)
- **Rate**: 10-20 scans/second
- **Bandwidth**: 10-200 MB/s

## Processing Point Clouds

### 1. Preprocessing
- **Noise Removal**: Filter outliers
- **Downsampling**: Reduce point count
- **Ground Removal**: Separate ground from objects
- **Coordinate Transform**: Convert to robot/base frame

### 2. Segmentation
- **Ground Segmentation**: Separate ground plane
- **Object Segmentation**: Cluster points into objects
- **Methods**: RANSAC, DBSCAN, region growing

### 3. Object Detection
- **Bounding Boxes**: 3D boxes around objects
- **Methods**: 
  - Classical: Clustering + fitting
  - Deep Learning: PointPillars, VoxelNet, SECOND
- **Output**: Objects with position, size, class

### 4. SLAM
- **LiDAR SLAM**: Build map from scans
- **Methods**: LOAM, LIO-SAM, LeGO-LOAM
- **Output**: Map + robot trajectory

## Common Applications

### Obstacle Detection
**Goal**: Find obstacles in path

**Process**:
1. Transform points to robot frame
2. Filter points in robot's path
3. Cluster into obstacles
4. Estimate obstacle properties

### Localization
**Goal**: Determine robot position

**Methods**:
- **Scan Matching**: Match current scan to map
- **ICP**: Iterative Closest Point
- **NDT**: Normal Distributions Transform

### Mapping
**Goal**: Build 3D map of environment

**Methods**:
- **Occupancy Grid**: 2D/3D grid
- **Point Cloud Map**: Collection of scans
- **Voxel Map**: 3D voxel grid

### Object Tracking
**Goal**: Track moving objects

**Process**:
1. Detect objects in each scan
2. Associate detections across time
3. Track with Kalman/Particle filter

## Coordinate Frames

### LiDAR Frame
- **Origin**: At LiDAR sensor center
- **Convention**: 
  - X: Forward
  - Y: Left
  - Z: Up
- **Transform**: T_base^lidar (calibrated)

### Point Cloud Transform
```
point_base = T_lidar^base * point_lidar
```

### Time Synchronization
- **Problem**: Points captured at different times
- **Solution**: 
  - Motion compensation (undistort for motion)
  - Timestamp each point
  - Transform to common time

## Calibration

### Intrinsic Calibration
- **Purpose**: Correct sensor errors
- **Methods**: Factory calibration, self-calibration
- **Parameters**: Beam angles, timing offsets

### Extrinsic Calibration
- **Purpose**: Determine LiDAR pose relative to robot
- **Methods**:
  - Known targets (checkerboard, spheres)
  - Optimization with other sensors
  - Hand-eye calibration

### Multi-LiDAR Calibration
- **Purpose**: Calibrate multiple LiDARs
- **Methods**: Overlapping scans, optimization

## Challenges

### Weather
- **Rain**: Scatters/absorbs laser
- **Fog**: Reduces range significantly
- **Snow**: Reflects unpredictably
- **Solutions**: Filtering, sensor fusion with cameras

### Sunlight
- **Problem**: Sunlight can saturate sensor
- **Impact**: Lost data, false detections
- **Solutions**: Filters, adaptive thresholds

### Reflective Surfaces
- **Problem**: Glass, mirrors reflect unpredictably
- **Impact**: False/missing detections
- **Solutions**: Sensor fusion, multiple viewpoints

### Computational Load
- **Problem**: Large point clouds, expensive processing
- **Impact**: Real-time constraints
- **Solutions**: 
  - Downsampling
  - Efficient algorithms
  - GPU acceleration

### Cost
- **Problem**: High-quality LiDAR is expensive
- **Impact**: Budget constraints
- **Solutions**: 
  - Lower-cost options (solid-state)
  - Use cameras + depth estimation

## Integration with Robot System

### Data Flow
```
LiDAR → Point Cloud → Preprocessing → 
Segmentation → Object Detection → Planning
```

### Synchronization
- **With Cameras**: Align timestamps
- **With IMU**: For motion compensation
- **With Odometry**: For localization

### Real-time Constraints
- **Processing**: Must complete before next scan
- **Latency**: < 100ms for obstacle avoidance
- **Optimization**: Efficient algorithms critical

## Best Practices

1. **Calibrate Extrinsics**: Accurate transforms critical
2. **Handle Motion**: Compensate for robot motion during scan
3. **Filter Noise**: Remove outliers and artifacts
4. **Optimize Processing**: Point clouds are large
5. **Fuse with Other Sensors**: LiDAR + cameras + IMU
6. **Handle Failures**: LiDAR can fail, have fallbacks
7. **Consider Weather**: Design for expected conditions

## Comparison with Cameras

| Aspect | LiDAR | Camera |
|--------|-------|--------|
| Depth | Direct measurement | Requires estimation |
| Range | 50-200m+ | Limited by resolution |
| Weather | Affected by rain/fog | Affected by lighting |
| Texture | No color/texture | Rich color/texture |
| Cost | Expensive | Cheap |
| Data Size | Large (point clouds) | Large (images) |
| Processing | Geometric | Appearance-based |

## Next Steps

- Learn about [Cameras](./camera.md) for complementary sensing
- Understand [IMU](./imu.md) for motion sensing
- Review [Coordinate Frames](../03_coordinate_frames/frames_and_transforms.md) for LiDAR integration


