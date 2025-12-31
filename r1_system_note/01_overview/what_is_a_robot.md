# What is a Robot?

## Definition

A **robot** is an autonomous or semi-autonomous machine capable of:
- **Sensing** its environment through sensors
- **Perceiving** and understanding the world around it
- **Planning** actions to achieve goals
- **Acting** on the physical world through actuators

## Key Components

### 1. Sensors
Robots gather information about their environment through sensors:
- **Exteroceptive sensors**: Measure the external environment (cameras, LiDAR, sonar)
- **Proprioceptive sensors**: Measure the robot's internal state (IMU, encoders, joint position sensors)

### 2. Actuators
Robots interact with the world through actuators:
- **Motors**: For movement (wheels, joints, propellers)
- **Grippers**: For manipulation
- **Speakers**: For communication

### 3. Computation
Robots require computational resources to:
- Process sensor data
- Make decisions
- Control actuators
- Run AI/ML models

### 4. Software Stack
The software enables:
- Sensor data processing
- Perception algorithms
- Planning and decision-making
- Control systems
- Communication between components

## Types of Robots

### Mobile Robots
- **Ground robots**: Wheeled, legged, or tracked
- **Aerial robots**: Drones, quadcopters
- **Marine robots**: Underwater vehicles

### Manipulator Robots
- **Arms**: Industrial robotic arms
- **Hands**: Dexterous manipulation

### Humanoid Robots
- Full-body robots designed to interact in human environments

## The Sense-Think-Act Loop

All robots operate on a fundamental loop:

```
Sense → Think → Act
  ↑                ↓
  └────────────────┘
```

1. **Sense**: Collect data from sensors
2. **Think**: Process data, make decisions, plan actions
3. **Act**: Execute actions through actuators
4. **Repeat**: The cycle continues, enabling continuous operation

## Why Robots Matter

Robots extend human capabilities by:
- Operating in dangerous environments
- Performing repetitive tasks with precision
- Working 24/7 without fatigue
- Processing information faster than humans
- Combining multiple sensor modalities

## Next Steps

- Learn about [Autonomy Levels](./autonomy_levels.md) to understand how independent robots can be
- Explore [System Architecture](../02_system_architecture/high_level_pipeline.md) to see how components work together

