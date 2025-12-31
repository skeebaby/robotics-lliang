# Perception, Planning, and Control

These three components form the core intelligence of a robot system. Understanding their roles and interactions is crucial for building effective robots.

## Perception

**Goal**: Understand the world from sensor data

### Key Tasks

#### 1. Localization
**Question**: "Where am I?"

**Methods**:
- **Odometry**: Dead reckoning from wheel encoders/IMU
- **Visual Odometry**: Camera-based motion estimation
- **SLAM**: Simultaneous Localization and Mapping
- **GPS/GNSS**: Global positioning (when available)

**Output**: Robot pose (x, y, z, roll, pitch, yaw)

**Challenges**:
- Drift accumulation
- Sensor noise
- Dynamic environments

#### 2. Mapping
**Question**: "What does the environment look like?"

**Types of Maps**:
- **Occupancy Grid**: Grid cells marked as free/occupied
- **Point Cloud**: 3D points from LiDAR/cameras
- **Semantic Map**: Objects labeled with meaning
- **Topological Map**: Graph of places and connections

**Methods**:
- **LiDAR SLAM**: Build map from LiDAR scans
- **Visual SLAM**: Build map from camera images
- **RGB-D SLAM**: Combine color and depth

#### 3. Object Detection & Recognition
**Question**: "What objects are present?"

**Methods**:
- **Classical**: Feature detection (SIFT, ORB), template matching
- **Deep Learning**: YOLO, Faster R-CNN, SSD
- **3D Detection**: Point cloud segmentation, 3D bounding boxes

**Output**: 
- Object classes
- Bounding boxes/poses
- Confidence scores

#### 4. Tracking
**Question**: "Where are objects moving?"

**Methods**:
- **Kalman Filter**: Linear motion models
- **Particle Filter**: Non-linear, multi-modal tracking
- **Deep Learning**: End-to-end tracking networks

**Output**: Object trajectories over time

### Perception Pipeline Example

```
Raw Images → Preprocessing → Feature Extraction → 
Object Detection → Tracking → Semantic Understanding
```

## Planning

**Goal**: Decide what actions to take

### Hierarchical Planning

#### 1. Mission Planning (High-Level)
- **Timeframe**: Minutes to hours
- **Goal**: Overall mission objectives
- **Example**: "Deliver package from A to B via waypoint C"

#### 2. Path Planning (Mid-Level)
- **Timeframe**: Seconds to minutes
- **Goal**: Find collision-free path
- **Algorithms**:
  - **A***: Optimal path in discrete grid
  - **RRT/RRT***: Probabilistic sampling
  - **Dijkstra**: Shortest path
  - **PRM**: Pre-computed roadmap

**Output**: Sequence of waypoints

#### 3. Motion Planning (Low-Level)
- **Timeframe**: Milliseconds to seconds
- **Goal**: Smooth, feasible trajectory
- **Considers**:
  - Kinematic constraints
  - Dynamic constraints
  - Actuator limits

**Algorithms**:
- **Trajectory Optimization**: Direct optimization
- **Lattice Planner**: Pre-computed motion primitives
- **MPC**: Model Predictive Control

**Output**: Time-parameterized trajectory (positions, velocities, accelerations)

### Planning Challenges

1. **Combinatorial Explosion**: Too many possible paths
2. **Dynamic Environments**: Obstacles move
3. **Uncertainty**: Imperfect perception
4. **Computational Limits**: Real-time constraints

### Replanning Strategies

- **Reactive**: Replan when obstacle detected
- **Predictive**: Anticipate future obstacles
- **Incremental**: Update plan efficiently
- **Anytime**: Return best plan found so far

## Control

**Goal**: Execute planned actions accurately

### Control Hierarchy

#### 1. High-Level Control
- **Input**: Planned trajectory
- **Output**: Desired states for low-level control
- **Frequency**: 10-100 Hz
- **Tasks**: 
  - Coordinate multiple subsystems
  - Handle mode switching
  - Execute action sequences

#### 2. Low-Level Control
- **Input**: Desired state (position, velocity)
- **Output**: Actuator commands (torque, voltage)
- **Frequency**: 100-1000 Hz
- **Tasks**:
  - Track trajectory precisely
  - Maintain stability
  - Reject disturbances

### Control Methods

#### Classical Control

**PID Control**:
- Proportional: React to current error
- Integral: Eliminate steady-state error
- Derivative: Dampen oscillations
- **Pros**: Simple, robust, well-understood
- **Cons**: Limited for complex systems

**LQR (Linear Quadratic Regulator)**:
- Optimal control for linear systems
- Minimizes cost function
- **Pros**: Optimal, handles multiple inputs/outputs
- **Cons**: Requires linear model

**MPC (Model Predictive Control)**:
- Optimize over prediction horizon
- Handle constraints explicitly
- **Pros**: Handles constraints, good performance
- **Cons**: Computationally expensive

#### Learning-Based Control

**Reinforcement Learning**:
- Learn control policy from experience
- **Pros**: Can handle complex dynamics, adapt
- **Cons**: Requires training, safety concerns

**Imitation Learning**:
- Learn from expert demonstrations
- **Pros**: Faster than RL, leverages human knowledge
- **Cons**: Limited to demonstrated behaviors

### Control Challenges

1. **Model Uncertainty**: Real system differs from model
2. **Disturbances**: External forces, wind, etc.
3. **Actuator Limits**: Saturation, delays
4. **Stability**: System must remain stable
5. **Robustness**: Handle variations and failures

## Integration: How They Work Together

### Typical Flow

```
1. Perception: "I see an obstacle 5m ahead"
2. Planning: "I'll go around it to the left"
3. Control: "Turn wheels 15° left, maintain speed"
4. Actuation: Robot turns
5. Perception: "Obstacle cleared, continue forward"
```

### Timing Considerations

- **Perception**: Updates at 10-30 Hz (acceptable latency: 50-200ms)
- **Planning**: Updates at 1-10 Hz (acceptable latency: 100-1000ms)
- **Control**: Updates at 100-1000 Hz (critical: <10ms latency)

### Data Dependencies

```
Perception → Planning → Control
    ↓           ↓          ↓
  Sensors    Goals    Actuators
```

### Failure Modes

1. **Perception Failure**: 
   - Robot doesn't see obstacle
   - **Mitigation**: Multiple sensors, redundancy

2. **Planning Failure**:
   - No feasible path found
   - **Mitigation**: Fallback behaviors, replanning

3. **Control Failure**:
   - Can't track desired trajectory
   - **Mitigation**: Robust controllers, safety limits

## Design Best Practices

1. **Modularity**: Separate perception, planning, control
2. **Interfaces**: Well-defined data formats
3. **Robustness**: Handle failures gracefully
4. **Performance**: Meet timing requirements
5. **Testing**: Test each component independently and together

## Next Steps

- Learn about [Real-time vs AI Systems](./realtime_vs_ai.md) trade-offs
- Understand [Coordinate Frames](../03_coordinate_frames/frames_and_transforms.md) for proper integration


