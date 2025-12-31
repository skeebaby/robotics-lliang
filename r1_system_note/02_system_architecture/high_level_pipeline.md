# High-Level Pipeline

The robot system pipeline describes the flow of information from sensors to actuators, enabling the robot to perceive, plan, and act in its environment.

## The Standard Pipeline

```
Sensors → Perception → Planning → Control → Actuators
   ↑                                        ↓
   └────────────────────────────────────────┘
              (Feedback Loop)
```

## Stage 1: Sensing

**Purpose**: Gather raw data about the environment and robot state

**Inputs**: 
- External environment (cameras, LiDAR, etc.)
- Internal state (joint positions, IMU, etc.)

**Outputs**: Raw sensor data streams

**Characteristics**:
- High frequency (often 10-100+ Hz)
- Raw, unprocessed data
- May include noise and artifacts

## Stage 2: Perception

**Purpose**: Extract meaningful information from sensor data

**Key Tasks**:
- **Localization**: Where am I? (position, orientation)
- **Mapping**: What does the environment look like? (obstacles, landmarks)
- **Object Detection**: What objects are present?
- **Tracking**: Where are objects moving?
- **Scene Understanding**: What is happening in the scene?

**Inputs**: Raw sensor data

**Outputs**: 
- Robot pose (position, orientation)
- Map of environment
- Detected objects with properties
- Semantic information

**Characteristics**:
- Computationally intensive
- May use AI/ML models
- Lower frequency than sensing (1-30 Hz typically)

## Stage 3: Planning

**Purpose**: Decide what actions to take to achieve goals

**Types of Planning**:

### Path Planning
- **Goal**: Find a collision-free path from current position to goal
- **Algorithms**: A*, RRT, Dijkstra
- **Output**: Sequence of waypoints

### Motion Planning
- **Goal**: Plan smooth trajectories considering dynamics
- **Considers**: Velocity, acceleration, constraints
- **Output**: Time-parameterized trajectory

### Task Planning
- **Goal**: Sequence of high-level actions
- **Example**: "Pick up object A, move to location B, place object A"
- **Output**: Action sequence

**Inputs**: 
- Current state (from perception)
- Goal specification
- Environment model

**Outputs**: 
- Planned trajectory or action sequence
- Predicted outcomes

**Characteristics**:
- Varies widely in frequency (0.1-10 Hz)
- Can be computationally expensive
- May require replanning when environment changes

## Stage 4: Control

**Purpose**: Execute planned actions by commanding actuators

**Types of Control**:

### Low-Level Control
- **Goal**: Follow desired trajectory precisely
- **Methods**: PID, LQR, MPC
- **Frequency**: High (100-1000 Hz)

### High-Level Control
- **Goal**: Execute planned actions
- **Coordinates**: Multiple subsystems
- **Frequency**: Medium (10-100 Hz)

**Inputs**: 
- Desired trajectory/actions (from planning)
- Current state (from sensors/perception)

**Outputs**: Actuator commands (motor torques, velocities, etc.)

**Characteristics**:
- Real-time critical
- High frequency
- Must be deterministic and reliable

## Stage 5: Actuation

**Purpose**: Execute physical actions in the world

**Types**:
- **Motion**: Wheels, legs, propellers
- **Manipulation**: Arms, grippers
- **Communication**: Speakers, displays

**Inputs**: Control commands

**Outputs**: Physical changes in the world

## Feedback Loops

### Inner Loop (Control)
- **Frequency**: Very high (100-1000 Hz)
- **Purpose**: Maintain stability, track trajectory
- **Example**: Motor controller adjusting torque based on encoder feedback

### Outer Loop (Perception-Planning)
- **Frequency**: Medium (1-30 Hz)
- **Purpose**: Adapt to environment changes
- **Example**: Replanning when obstacle detected

### Strategic Loop (Mission Planning)
- **Frequency**: Low (0.1-1 Hz)
- **Purpose**: High-level goal adjustment
- **Example**: Changing destination based on new information

## Data Flow Characteristics

### Latency Requirements
- **Control**: < 10ms (critical for stability)
- **Perception**: 50-200ms (acceptable for most applications)
- **Planning**: 100-1000ms (depends on complexity)

### Data Rates
- **Sensors**: Can be very high (e.g., LiDAR: millions of points/second)
- **Perception**: Reduced after processing
- **Planning**: Low bandwidth (waypoints, actions)
- **Control**: Moderate (actuator commands)

## Common Architectures

### Monolithic
- All stages in single process
- Simple but less flexible
- Good for simple systems

### Modular
- Each stage as separate module
- Better for complex systems
- Enables parallel development

### Distributed
- Stages on different computers
- Scalable
- Requires communication infrastructure (e.g., ROS2)

## Design Principles

1. **Separation of Concerns**: Each stage has clear responsibility
2. **Modularity**: Stages can be developed/tested independently
3. **Interfaces**: Well-defined data formats between stages
4. **Real-time Constraints**: Respect timing requirements
5. **Robustness**: Handle failures gracefully at each stage

## Next Steps

- Deep dive into [Perception, Planning, and Control](./perception_planning_control.md)
- Understand [Real-time vs AI Systems](./realtime_vs_ai.md) trade-offs


