# Classical Control

Classical control methods use mathematical models and well-established control theory to achieve desired robot behavior. These methods are deterministic, well-understood, and reliable.

## What is Classical Control?

Classical control uses:
- **Mathematical models** of the system
- **Control theory** (linear systems, frequency domain)
- **Deterministic algorithms** (no learning)
- **Proven stability** guarantees

**Characteristics**:
- Predictable behavior
- Real-time capable
- No training required
- Works with good models

## Control Objectives

### 1. Tracking
**Goal**: Follow a desired trajectory

**Example**: Robot arm following planned path

### 2. Regulation
**Goal**: Maintain desired setpoint

**Example**: Drone maintaining altitude

### 3. Stabilization
**Goal**: Keep system stable

**Example**: Inverted pendulum balancing

### 4. Disturbance Rejection
**Goal**: Maintain performance despite disturbances

**Example**: Robot maintaining speed despite wind

## PID Control

### Overview
**PID** (Proportional-Integral-Derivative) is the most common control method.

**Components**:
- **P (Proportional)**: React to current error
- **I (Integral)**: Eliminate steady-state error
- **D (Derivative)**: Dampen oscillations

### Control Law
```
u(t) = Kp * e(t) + Ki * ∫e(τ)dτ + Kd * de(t)/dt

where:
  e(t) = desired - actual (error)
  Kp, Ki, Kd = tuning parameters
```

### Tuning Methods

**Manual Tuning**:
1. Start with Kp only
2. Add Kd to reduce oscillations
3. Add Ki to eliminate steady-state error
4. Adjust until performance acceptable

**Ziegler-Nichols**:
- Systematic tuning method
- Based on system response
- Good starting point

**Auto-tuning**:
- Automatic parameter selection
- Based on system identification
- Requires experiments

### Pros and Cons

**Pros**:
- Simple to implement
- Works for many systems
- Well-understood
- Real-time capable

**Cons**:
- Limited for complex systems
- Requires tuning
- May not be optimal
- Doesn't handle constraints well

## State-Space Control

### Overview
Represents system as:
```
ẋ = Ax + Bu  (state equation)
y = Cx + Du  (output equation)
```

**Where**:
- x: State vector
- u: Control input
- y: Output
- A, B, C, D: System matrices

### LQR (Linear Quadratic Regulator)

**Goal**: Optimal control for linear systems

**Cost Function**:
```
J = ∫(x^T Q x + u^T R u) dt
```

**Solution**: 
```
u = -K * x
where K = LQR(A, B, Q, R)
```

**Pros**:
- Optimal (minimizes cost)
- Handles multiple inputs/outputs
- Well-established theory

**Cons**:
- Requires linear model
- Requires full state observation
- Tuning Q and R matrices

### LQG (Linear Quadratic Gaussian)

**Extension of LQR**:
- Handles measurement noise
- Uses Kalman filter for state estimation
- Optimal under Gaussian noise

## Model Predictive Control (MPC)

### Overview
**MPC** optimizes control over a prediction horizon.

**Process**:
1. Predict future states using model
2. Optimize control sequence
3. Apply first control action
4. Repeat at next time step

### Control Law
```
minimize: J = Σ(x_k^T Q x_k + u_k^T R u_k)
subject to: 
  x_{k+1} = f(x_k, u_k)  (dynamics)
  x_min ≤ x_k ≤ x_max    (state constraints)
  u_min ≤ u_k ≤ u_max    (input constraints)
```

### Advantages
- **Handles constraints** explicitly
- **Good performance** (optimization-based)
- **Works for non-linear** systems (non-linear MPC)
- **Predictive** (anticipates future)

### Disadvantages
- **Computationally expensive**
- **Requires model** (accuracy matters)
- **Real-time challenges** (optimization must finish)

### Applications
- Autonomous vehicles (path following)
- Robot manipulators (trajectory tracking)
- Drones (position control)

## Feedforward Control

### Overview
**Feedforward** uses model to predict required control.

**Control Law**:
```
u = u_feedforward + u_feedback

u_feedforward = model_inverse(desired_trajectory)
u_feedback = PID(error)  (or other feedback)
```

### Benefits
- **Reduces tracking error** (model compensates)
- **Faster response** (doesn't wait for error)
- **Less feedback needed** (model does work)

### Requirements
- **Good model** (accuracy critical)
- **Inverse model** (can be complex)

## Robust Control

### Overview
**Robust control** handles model uncertainty.

**Methods**:
- **H∞ Control**: Minimize worst-case error
- **μ-synthesis**: Handle structured uncertainty
- **Sliding Mode**: Robust to disturbances

### When to Use
- Model uncertainty significant
- Disturbances unknown
- Safety critical
- Performance must be guaranteed

## Adaptive Control

### Overview
**Adaptive control** adjusts parameters online.

**Types**:
- **Model Reference Adaptive Control (MRAC)**: Adjust to match reference model
- **Self-Tuning Regulators**: Estimate parameters, update controller

### When to Use
- System parameters change
- Unknown/uncertain parameters
- Need to adapt over time

## Control Architecture

### Hierarchical Control

**High-Level**:
- Path planning
- Task coordination
- Mode switching
- Frequency: 1-10 Hz

**Mid-Level**:
- Trajectory generation
- Coordination
- Frequency: 10-100 Hz

**Low-Level**:
- Actuator control
- Stability
- Frequency: 100-1000 Hz

### Example: Mobile Robot

```
Mission Planner (1 Hz)
  ↓
Path Planner (10 Hz)
  ↓
Trajectory Generator (50 Hz)
  ↓
Velocity Controller (100 Hz)
  ↓
Motor Controller (1000 Hz)
```

## Implementation Considerations

### Real-time Requirements
- **Low-level control**: Hard real-time (< 10ms)
- **High-level control**: Soft real-time (< 100ms)
- **Use RTOS** for critical loops

### Computational Resources
- **PID**: Very low (microseconds)
- **LQR**: Low (milliseconds)
- **MPC**: High (10-100ms, depends on horizon)

### Sensor Requirements
- **Full state**: LQR, MPC
- **Partial state**: Use observers (Kalman filter)
- **Delayed measurements**: Predict current state

## Tuning and Validation

### System Identification
**Purpose**: Build model from data

**Methods**:
- Step response
- Frequency response
- Parameter estimation

### Controller Design
1. **Model system**: Identify parameters
2. **Design controller**: Choose method, tune
3. **Simulate**: Test in simulation
4. **Validate**: Test on real system
5. **Iterate**: Refine as needed

### Performance Metrics
- **Rise time**: How fast to reach setpoint
- **Overshoot**: Maximum deviation
- **Settling time**: Time to reach steady-state
- **Steady-state error**: Final error
- **Disturbance rejection**: Response to disturbances

## Common Challenges

### 1. Model Uncertainty
**Problem**: Model doesn't match reality

**Solutions**:
- Robust control
- Adaptive control
- Online model learning

### 2. Non-linearity
**Problem**: System is non-linear

**Solutions**:
- Linearize around operating point
- Non-linear MPC
- Gain scheduling

### 3. Constraints
**Problem**: Actuator/safety limits

**Solutions**:
- MPC (handles constraints)
- Saturation limits
- Constraint-aware planning

### 4. Delays
**Problem**: Sensor/actuator delays

**Solutions**:
- Predict ahead
- Smith predictor
- Account in model

## Best Practices

1. **Start Simple**: PID before complex methods
2. **Understand System**: Good model → good control
3. **Validate**: Test in simulation first
4. **Monitor**: Log performance, detect issues
5. **Handle Failures**: Graceful degradation
6. **Document**: Tuning parameters, assumptions

## Next Steps

- Learn about [Learning-Based Control](./learning_based_control.md) for complex systems
- Review [Sensors](../04_sensors/) for control feedback
- Understand [System Architecture](../02_system_architecture/perception_planning_control.md) integration


