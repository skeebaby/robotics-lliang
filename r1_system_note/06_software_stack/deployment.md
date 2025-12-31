# Deployment

Deploying robot software to real hardware involves considerations beyond development, including real-time constraints, hardware integration, safety, and reliability.

## Deployment Challenges

### Real-time Requirements

**Problem**: Real systems have timing constraints

**Solutions**:
- **RTOS**: Real-time operating system
- **Priority scheduling**: Critical tasks first
- **Resource reservation**: Guarantee resources
- **Deterministic execution**: Predictable timing

### Hardware Integration

**Problem**: Software must interface with hardware

**Solutions**:
- **Drivers**: Hardware-specific code
- **Abstraction layers**: Hide hardware details
- **Standard interfaces**: USB, Ethernet, CAN, etc.

### Reliability

**Problem**: Systems must work reliably

**Solutions**:
- **Error handling**: Graceful failures
- **Monitoring**: Health checks
- **Recovery**: Automatic recovery
- **Redundancy**: Backup systems

### Safety

**Problem**: Robots can cause harm

**Solutions**:
- **Safety limits**: Hard constraints
- **Emergency stops**: Immediate shutdown
- **Watchdogs**: Detect failures
- **Validation**: Extensive testing

## Deployment Architecture

### On-Robot Computing

**Compute on robot**:
- **Pros**: Low latency, no network needed
- **Cons**: Limited compute, power constraints
- **Use**: Real-time control, basic perception

### Edge Computing

**Compute near robot**:
- **Pros**: More compute, still low latency
- **Cons**: Additional hardware
- **Use**: Advanced perception, planning

### Cloud Computing

**Compute in cloud**:
- **Pros**: Unlimited compute, scalable
- **Cons**: Network latency, connectivity
- **Use**: Training, complex planning, data processing

### Hybrid

**Combine approaches**:
- **Real-time on robot**: Control, safety
- **Edge for perception**: Object detection
- **Cloud for planning**: Complex decisions

## Real-time Systems

### RTOS Options

**FreeRTOS**:
- Free, open-source
- Small footprint
- Good for embedded

**RT-Linux**:
- Linux with real-time patches
- Full Linux compatibility
- Good for complex systems

**QNX**:
- Commercial RTOS
- Very reliable
- Used in safety-critical

**ROS2 with RT**:
- ROS2 real-time support
- Deterministic execution
- Good for robotics

### Real-time Considerations

**Deterministic Execution**:
- Avoid dynamic allocation
- Fixed-size buffers
- Predictable algorithms

**Priority Scheduling**:
- Control: Highest priority
- Perception: Medium priority
- Logging: Lowest priority

**Resource Management**:
- CPU affinity: Pin to cores
- Memory locking: Prevent swapping
- I/O scheduling: Prioritize critical I/O

## Hardware Integration

### Sensor Integration

**Drivers**:
- Vendor-provided drivers
- ROS2 drivers
- Custom drivers

**Interfaces**:
- **USB**: Cameras, IMUs
- **Ethernet**: LiDAR, cameras
- **Serial**: Simple sensors
- **I2C/SPI**: Embedded sensors

**Calibration**:
- Intrinsic: Sensor parameters
- Extrinsic: Sensor poses
- Temporal: Time synchronization

### Actuator Integration

**Motor Controllers**:
- PWM control
- CAN bus
- Serial commands

**Safety**:
- Current limits
- Position limits
- Emergency stops

**Feedback**:
- Encoders
- Current sensors
- Position feedback

## Software Deployment

### Build Systems

**Colcon** (ROS2):
- Build ROS2 packages
- Dependency management
- Install targets

**CMake**:
- General C++ builds
- Cross-platform
- Flexible

**Python**:
- pip for packages
- Virtual environments
- Requirements files

### Packaging

**Debian Packages**:
- System integration
- Dependency management
- Easy installation

**Docker**:
- Containerization
- Isolation
- Reproducibility

**Snap**:
- Self-contained
- Easy updates
- Security

### Installation

**Methods**:
1. **Direct install**: Copy files
2. **Package manager**: apt, pip, etc.
3. **Container**: Docker, Snap
4. **OTA updates**: Over-the-air

## Configuration Management

### Parameters

**ROS2 Parameters**:
- Node configuration
- Launch-time or runtime
- YAML files

**Configuration Files**:
- YAML, JSON, XML
- Version controlled
- Environment-specific

### Calibration

**Sensor Calibration**:
- Store calibration data
- Load at startup
- Update when needed

**System Calibration**:
- Robot-specific parameters
- Tuned for hardware
- Documented

## Monitoring and Logging

### Health Monitoring

**System Health**:
- CPU, memory usage
- Disk space
- Network status

**Robot Health**:
- Sensor status
- Actuator status
- Battery level

**Application Health**:
- Node status
- Topic rates
- Error rates

### Logging

**ROS2 Logging**:
- Built-in logging
- Levels: DEBUG, INFO, WARN, ERROR
- Configurable

**System Logging**:
- syslog
- journald
- Custom logs

**Data Logging**:
- Bag files (ROS2)
- Custom formats
- Database storage

### Diagnostics

**ROS2 Diagnostics**:
- Diagnostic messages
- Health status
- Performance metrics

**Tools**:
- `ros2 run diagnostic_aggregator`
- Custom diagnostic nodes
- Monitoring dashboards

## Safety Systems

### Emergency Stops

**Hardware E-Stop**:
- Physical button
- Hardware interrupt
- Immediate shutdown

**Software E-Stop**:
- Software command
- Graceful shutdown
- State saving

### Watchdogs

**Purpose**: Detect system failures

**Types**:
- **Hardware watchdog**: Resets on timeout
- **Software watchdog**: Monitors processes
- **Application watchdog**: Monitors robot state

### Safety Limits

**Types**:
- **Position limits**: Joint/workspace limits
- **Velocity limits**: Maximum speeds
- **Acceleration limits**: Maximum accelerations
- **Current limits**: Motor current limits

**Implementation**:
- Hardware limits (motor controllers)
- Software limits (control code)
- Both (defense in depth)

## Testing Before Deployment

### Unit Tests

**Test components**:
- Individual functions
- Classes
- Modules

**Tools**:
- pytest (Python)
- gtest (C++)
- ROS2 test framework

### Integration Tests

**Test system**:
- Multiple components
- Full pipeline
- End-to-end

**Methods**:
- Simulation
- Hardware-in-the-loop
- Real hardware

### Validation Tests

**Validate behavior**:
- Functional requirements
- Performance requirements
- Safety requirements

**Methods**:
- Test scenarios
- Stress tests
- Failure mode tests

## Deployment Strategies

### Phased Rollout

**Gradual deployment**:
1. **Pilot**: Single robot
2. **Limited**: Small group
3. **Full**: All robots

**Benefits**:
- Catch issues early
- Learn and adapt
- Reduce risk

### Blue-Green Deployment

**Two environments**:
- **Blue**: Current production
- **Green**: New version

**Process**:
1. Deploy to green
2. Test green
3. Switch to green
4. Keep blue as backup

### Canary Deployment

**Gradual rollout**:
1. Deploy to small subset
2. Monitor performance
3. Gradually expand
4. Roll back if issues

## Maintenance

### Updates

**Types**:
- **Bug fixes**: Critical fixes
- **Features**: New functionality
- **Security**: Security patches

**Methods**:
- **Manual**: SSH, direct access
- **OTA**: Over-the-air updates
- **Scheduled**: Maintenance windows

### Monitoring

**Continuous monitoring**:
- System metrics
- Robot performance
- Error rates
- User feedback

### Debugging

**Remote debugging**:
- SSH access
- Remote logging
- Telemetry
- Video streaming

## Best Practices

### 1. Start Simple

**Begin with minimal deployment**:
- Basic functionality
- Add complexity gradually
- Validate at each step

### 2. Test Thoroughly

**Test before deployment**:
- Unit tests
- Integration tests
- Validation tests
- Stress tests

### 3. Monitor Continuously

**Monitor after deployment**:
- System health
- Robot performance
- Error rates
- User feedback

### 4. Plan for Failures

**Design for reliability**:
- Error handling
- Graceful degradation
- Recovery mechanisms
- Fallback modes

### 5. Document Everything

**Document**:
- Configuration
- Calibration
- Known issues
- Procedures

### 6. Version Control

**Track changes**:
- Code versions
- Configuration versions
- Calibration versions
- Deployment versions

## Common Pitfalls

### 1. Ignoring Real-time

**Problem**: Not considering timing

**Solution**: Use RTOS, prioritize tasks

### 2. Insufficient Testing

**Problem**: Not testing enough

**Solution**: Comprehensive test suite

### 3. Poor Error Handling

**Problem**: Crashes on errors

**Solution**: Robust error handling

### 4. No Monitoring

**Problem**: Don't know what's happening

**Solution**: Comprehensive monitoring

### 5. Configuration Drift

**Problem**: Configurations diverge

**Solution**: Version control, automation

## Next Steps

- Review [ROS2 Mental Model](./ros2_mental_model.md) for deployment
- Understand [Simulation](./simulation.md) for testing
- Learn about [System Architecture](../02_system_architecture/) for integration


