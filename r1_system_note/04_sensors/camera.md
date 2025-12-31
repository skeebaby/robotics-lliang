# Camera Sensors

Cameras are one of the most common sensors in robotics, providing rich visual information about the environment.

## Types of Cameras

### RGB Cameras
- **Output**: Color images (Red, Green, Blue channels)
- **Use Cases**: Object recognition, scene understanding, visual odometry
- **Pros**: Rich information, human-interpretable
- **Cons**: No depth information, sensitive to lighting

### Depth Cameras
- **RGB-D**: Combines RGB and depth
- **Stereo**: Two cameras for depth estimation
- **Structured Light**: Projects pattern, measures distortion
- **Time-of-Flight (ToF)**: Measures light travel time
- **Use Cases**: 3D mapping, obstacle avoidance, manipulation
- **Pros**: Provides depth information
- **Cons**: Limited range, sensitive to surfaces

### Monocular vs Stereo
- **Monocular**: Single camera, cheaper, lighter
- **Stereo**: Two cameras, provides depth, more complex

## Camera Parameters

### Intrinsic Parameters

**Focal Length** (fx, fy):
- Distance from image plane to camera center
- Measured in pixels
- Affects field of view

**Principal Point** (cx, cy):
- Optical center in image coordinates
- Usually near image center

**Distortion Coefficients**:
- Radial distortion: Barrel/pincushion
- Tangential distortion: Lens misalignment

**Camera Matrix (K)**:
```
K = [fx  0  cx]
    [0  fy  cy]
    [0   0   1]
```

### Extrinsic Parameters

**Pose**: Position and orientation relative to robot
- Translation: Camera position
- Rotation: Camera orientation
- Expressed as transform: T_base^camera

## Image Processing Pipeline

### 1. Image Acquisition
```
Light → Lens → Sensor → ADC → Digital Image
```

### 2. Preprocessing
- **Debayering**: Convert raw sensor data to RGB
- **White Balance**: Adjust color temperature
- **Exposure Control**: Adjust brightness
- **Noise Reduction**: Filter sensor noise

### 3. Calibration
- **Intrinsic Calibration**: Determine camera matrix
- **Extrinsic Calibration**: Determine camera pose
- **Distortion Correction**: Undistort images

### 4. Feature Extraction
- **Classical**: SIFT, SURF, ORB, FAST
- **Deep Learning**: Learned features from CNNs
- **Purpose**: Find distinctive points/regions

### 5. Processing
- **Object Detection**: Find objects in image
- **Segmentation**: Separate objects/regions
- **Tracking**: Follow objects over time
- **SLAM**: Build map from images

## Common Applications

### Visual Odometry
**Goal**: Estimate robot motion from images

**Methods**:
- **Feature-based**: Track features between frames
- **Direct**: Use pixel intensities directly
- **Deep Learning**: Learned odometry networks

**Challenges**:
- Scale ambiguity (monocular)
- Drift accumulation
- Lighting changes

### Object Detection
**Goal**: Find and classify objects

**Methods**:
- **Classical**: HOG, Haar cascades
- **Deep Learning**: YOLO, Faster R-CNN, SSD
- **3D Detection**: Combine with depth

### Visual SLAM
**Goal**: Build map while localizing

**Methods**:
- **ORB-SLAM**: Feature-based
- **Direct SLAM**: Dense methods
- **Semantic SLAM**: Include object labels

## Camera Models

### Pinhole Camera Model

**Projection**:
```
[u]   [fx  0  cx] [X]
[v] = [0  fy  cy] [Y]  (in camera frame)
[1]   [0   0   1] [Z]
```

**Inverse (Unprojection)**:
- Requires depth information
- Or use stereo/multiple views

### Distortion Models

**Radial Distortion**:
```
x_distorted = x * (1 + k1*r² + k2*r⁴ + k3*r⁶)
y_distorted = y * (1 + k1*r² + k2*r⁴ + k3*r⁶)
```

**Tangential Distortion**:
```
x_distorted = x + 2*p1*x*y + p2*(r² + 2*x²)
y_distorted = y + p1*(r² + 2*y²) + 2*p2*x*y
```

## Calibration

### Intrinsic Calibration

**Method**: Use known pattern (checkerboard)

**Process**:
1. Capture images of checkerboard from multiple angles
2. Detect corners in each image
3. Solve for camera matrix and distortion
4. Validate with reprojection error

**Tools**:
- OpenCV: `cv2.calibrateCamera()`
- ROS: `camera_calibration` package

### Extrinsic Calibration

**Hand-Eye Calibration**:
- Calibrate camera relative to robot
- Uses known object/pattern
- Solves: AX = XB problem

**Multi-Camera Calibration**:
- Calibrate multiple cameras
- Uses overlapping views
- Optimization-based

## Performance Considerations

### Frame Rate
- **Standard**: 30 FPS
- **High-speed**: 60-240 FPS
- **Trade-off**: Higher rate = more data, more processing

### Resolution
- **Low**: 640x480 (VGA)
- **Medium**: 1280x720 (HD)
- **High**: 1920x1080 (Full HD) or higher
- **Trade-off**: Higher resolution = more detail, more data

### Field of View
- **Narrow**: Telephoto, detailed but limited area
- **Wide**: Fisheye, large area but distorted
- **Standard**: 50-70 degrees horizontal

## Challenges

### Lighting
- **Too bright**: Overexposed, loss of detail
- **Too dark**: Underexposed, noise
- **Variable**: Shadows, reflections
- **Solutions**: Auto-exposure, HDR, multiple exposures

### Motion Blur
- **Cause**: Camera/object motion during exposure
- **Impact**: Blurry images, lost features
- **Solutions**: Shorter exposure, image stabilization

### Occlusion
- **Problem**: Objects hidden behind others
- **Impact**: Incomplete information
- **Solutions**: Multiple viewpoints, active vision

### Scale Ambiguity (Monocular)
- **Problem**: Can't determine absolute scale
- **Impact**: Scale drift in SLAM
- **Solutions**: Stereo, depth camera, known objects

## Integration with Robot System

### Data Flow
```
Camera → Image Capture → Preprocessing → 
Perception → Planning → Control
```

### Coordinate Frames
- **Camera Frame**: At optical center
- **Image Frame**: 2D pixel coordinates
- **Transform**: T_base^camera (extrinsic calibration)

### Synchronization
- **Multiple Cameras**: Synchronize triggers
- **Other Sensors**: Timestamp alignment
- **ROS2**: Use message timestamps

## Best Practices

1. **Calibrate Regularly**: Cameras drift over time
2. **Handle Failures**: Camera can fail, have fallbacks
3. **Optimize Processing**: Images are large, optimize pipelines
4. **Consider Lighting**: Design for expected conditions
5. **Multiple Views**: Use multiple cameras for robustness
6. **Validate Outputs**: Check image quality, detect failures

## Next Steps

- Learn about [LiDAR](./lidar.md) for 3D sensing
- Understand [IMU](./imu.md) for motion sensing
- Review [Coordinate Frames](../03_coordinate_frames/frames_and_transforms.md) for camera integration


