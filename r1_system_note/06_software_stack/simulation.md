# Simulation

Simulation is essential for robot development, allowing testing, debugging, and training without physical hardware.

## Why Simulate?

### Benefits

1. **Safety**: Test dangerous scenarios safely
2. **Cost**: Avoid hardware damage
3. **Speed**: Faster than real-time possible
4. **Reproducibility**: Repeat exact scenarios
5. **Debugging**: Easier to inspect and debug
6. **Training**: Generate unlimited data for ML
7. **Early Development**: Start before hardware ready

### Limitations

1. **Reality Gap**: Simulation ≠ reality
2. **Model Accuracy**: Models are approximations
3. **Missing Effects**: Unmodeled phenomena
4. **Computational Cost**: Can be expensive

## Simulation Types

### Physics Simulation

**Purpose**: Simulate physical dynamics

**Engines**:
- **Gazebo**: Popular, ROS-integrated
- **PyBullet**: Python-based, ML-friendly
- **MuJoCo**: Fast, accurate
- **Isaac Sim**: NVIDIA, GPU-accelerated

**Simulates**:
- Rigid body dynamics
- Collisions
- Friction
- Gravity
- Joints and constraints

### Sensor Simulation

**Purpose**: Simulate sensor outputs

**Types**:
- **Camera**: Rendered images
- **LiDAR**: Ray-casting
- **IMU**: Physics-based
- **GPS**: Position-based

**Challenges**:
- Realistic noise
- Realistic artifacts
- Computational cost

### Environment Simulation

**Purpose**: Simulate world/obstacles

**Types**:
- **Static**: Buildings, terrain
- **Dynamic**: Moving objects, people
- **Weather**: Rain, fog, lighting

## Gazebo (Classic)

### Overview

**Gazebo**: 3D physics simulator

**Features**:
- Physics engine (ODE, Bullet)
- Sensor simulation
- ROS integration
- GUI and headless modes

### Key Concepts

**World**: Environment description
**Model**: Robot or object
**Plugin**: Custom behavior
**Link**: Rigid body
**Joint**: Connection between links

### Workflow

1. **Create World**: Define environment
2. **Add Models**: Add robot, objects
3. **Configure Sensors**: Add cameras, LiDAR, etc.
4. **Launch**: Start simulation
5. **Control**: Send commands via ROS

### Limitations

- Being phased out (Gazebo Classic)
- Moving to Ignition/Gazebo

## Ignition Gazebo / Gazebo

### Overview

**New Gazebo**: Rewritten, modern

**Features**:
- Component-based architecture
- Better performance
- ROS2 integration
- Plugin system

### Key Improvements

- **Performance**: Faster, more efficient
- **Modularity**: Component-based
- **ROS2**: Native ROS2 support
- **Cloud**: Cloud simulation support

## PyBullet

### Overview

**PyBullet**: Python physics engine

**Features**:
- Python API
- Good for ML/RL
- Fast
- Free and open-source

### Use Cases

- Reinforcement learning
- Rapid prototyping
- Research
- Training data generation

### Example

```python
import pybullet as p

# Connect to physics server
p.connect(p.GUI)

# Load robot
robot = p.loadURDF("robot.urdf")

# Step simulation
p.stepSimulation()
```

## MuJoCo

### Overview

**MuJoCo**: Fast, accurate physics

**Features**:
- Very fast
- Accurate contact
- Good for control
- Now open-source

### Use Cases

- Control research
- Fast simulation
- High-fidelity dynamics

## Isaac Sim

### Overview

**Isaac Sim**: NVIDIA's simulator

**Features**:
- GPU-accelerated
- Photorealistic rendering
- ROS2 integration
- Large-scale simulation

### Use Cases

- Computer vision
- Large-scale testing
- Photorealistic rendering
- ML training

## Simulation Fidelity

### Levels of Fidelity

**Low Fidelity**:
- Simple dynamics
- Basic sensors
- Fast
- **Use**: Algorithm development, testing

**Medium Fidelity**:
- Realistic dynamics
- Good sensors
- Moderate speed
- **Use**: Most development, validation

**High Fidelity**:
- Very realistic
- Accurate sensors
- Slower
- **Use**: Final validation, sim-to-real

### Choosing Fidelity

**Consider**:
- **Purpose**: What are you testing?
- **Speed**: How fast needed?
- **Accuracy**: How realistic needed?
- **Resources**: Computational budget

## Sensor Simulation

### Camera Simulation

**Methods**:
- **Rendering**: Render 3D scene to image
- **Ray-tracing**: Physically-based
- **Rasterization**: Faster, less accurate

**Outputs**:
- RGB images
- Depth images
- Segmentation masks

**Challenges**:
- Realistic lighting
- Realistic materials
- Realistic noise

### LiDAR Simulation

**Methods**:
- **Ray-casting**: Cast rays, measure distance
- **Point sampling**: Sample from geometry

**Outputs**:
- Point clouds
- Intensity values

**Challenges**:
- Realistic noise
- Realistic artifacts
- Computational cost

### IMU Simulation

**Methods**:
- **Physics-based**: From simulated motion
- **Noise models**: Add realistic noise

**Outputs**:
- Acceleration
- Angular velocity
- (Magnetometer)

**Challenges**:
- Realistic bias
- Realistic noise
- Temperature effects

## Sim-to-Real Transfer

### The Problem

**Sim-to-Real Gap**: Simulation ≠ reality

**Causes**:
- Model inaccuracies
- Unmodeled effects
- Sensor differences
- Actuator differences

### Solutions

#### 1. Domain Randomization

**Idea**: Vary simulation parameters

**Randomize**:
- Physics parameters (friction, mass)
- Visual appearance (textures, lighting)
- Sensor noise
- Environment

**Benefits**:
- More robust policies
- Better generalization

#### 2. System Identification

**Idea**: Calibrate simulation to match reality

**Process**:
1. Collect real robot data
2. Identify parameters
3. Update simulation model

#### 3. Progressive Training

**Idea**: Start in sim, fine-tune in real

**Process**:
1. Train in simulation
2. Transfer to real robot
3. Fine-tune with real data

#### 4. Robust Control

**Idea**: Design controllers robust to uncertainty

**Methods**:
- Robust control theory
- Adaptive control
- Learning-based with robustness

## Testing in Simulation

### Unit Testing

**Test individual components**:
- Controllers
- Planners
- Perception algorithms

**Benefits**:
- Fast iteration
- Isolated testing
- Reproducible

### Integration Testing

**Test system together**:
- Full pipeline
- Multiple components
- End-to-end

**Benefits**:
- Find integration issues
- Test interactions

### Scenario Testing

**Test specific scenarios**:
- Edge cases
- Failure modes
- Stress tests

**Benefits**:
- Comprehensive coverage
- Find bugs early

## Best Practices

### 1. Start Simple

**Begin with simple simulation**:
- Basic dynamics
- Simple sensors
- Add complexity gradually

### 2. Validate Models

**Compare simulation to reality**:
- System identification
- Validation experiments
- Parameter tuning

### 3. Use Appropriate Fidelity

**Match fidelity to purpose**:
- Low for algorithm development
- Medium for most work
- High for final validation

### 4. Handle Sim-to-Real Gap

**Plan for transfer**:
- Domain randomization
- Robust methods
- Validation in real

### 5. Reproducibility

**Make simulations reproducible**:
- Fixed random seeds
- Version control
- Document parameters

### 6. Performance

**Optimize when needed**:
- Profile simulation
- Reduce fidelity where possible
- Use faster engines

## Common Workflows

### Development Workflow

1. **Develop in simulation**
2. **Test in simulation**
3. **Validate in simulation**
4. **Transfer to real**
5. **Fine-tune**

### Training Workflow

1. **Generate data in simulation**
2. **Train model**
3. **Validate in simulation**
4. **Transfer to real**
5. **Fine-tune with real data**

### Testing Workflow

1. **Define test scenarios**
2. **Run in simulation**
3. **Analyze results**
4. **Fix issues**
5. **Re-test**

## Tools and Resources

### Visualization

- **RViz2**: ROS2 visualization
- **Gazebo GUI**: 3D visualization
- **Plotting**: Matplotlib, etc.

### Analysis

- **Bag files**: Record and replay
- **Logging**: ROS2 logging
- **Metrics**: Performance analysis

### Frameworks

- **ROS2**: Integration
- **gazebo_ros**: ROS-Gazebo bridge
- **ign_ros**: Ignition-ROS bridge

## Next Steps

- Learn about [Deployment](./deployment.md) to real robots
- Review [ROS2 Mental Model](./ros2_mental_model.md) for integration
- Understand [Control Systems](../05_control/) for simulation testing


