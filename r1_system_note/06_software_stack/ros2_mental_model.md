# ROS2 Mental Model

Understanding ROS2's architecture and design philosophy is crucial for effectively building robot systems. This guide provides the mental model for thinking about ROS2.

## What is ROS2?

**ROS2** (Robot Operating System 2) is a middleware framework for robot software development.

**Key Concepts**:
- **Distributed**: Nodes run independently
- **Communication**: Nodes communicate via topics, services, actions
- **Modular**: Build systems from reusable components
- **Language Agnostic**: Python, C++, and more

## Core Concepts

### Nodes

**Definition**: A process that performs computation

**Characteristics**:
- Independent processes
- Can run on same or different machines
- Communicate via ROS2 mechanisms
- Single responsibility (ideally)

**Example Nodes**:
- `camera_driver`: Publishes images
- `object_detector`: Subscribes to images, publishes detections
- `planner`: Subscribes to detections, publishes path
- `controller`: Subscribes to path, publishes commands

### Topics

**Definition**: Named communication channel for streaming data

**Characteristics**:
- **One-to-many**: One publisher, many subscribers
- **Asynchronous**: Publisher doesn't wait for subscribers
- **Typed**: Each topic has a message type
- **Best-effort**: No delivery guarantees (by default)

**Example**:
```
camera_driver → /camera/image (Image msg)
object_detector subscribes to /camera/image
```

### Messages

**Definition**: Data structure sent over topics

**Characteristics**:
- **Typed**: Defined in `.msg` files
- **Structured**: Fields with types
- **Versioned**: Can evolve over time

**Example**:
```
# Image.msg
uint32 height
uint32 width
uint8[] data
```

### Services

**Definition**: Request-response communication

**Characteristics**:
- **Synchronous**: Client waits for response
- **One-to-one**: One client, one server
- **Blocking**: Client blocks until response

**Example**:
```
Client: "What is the robot's current pose?"
Server: "Pose is (x=5.2, y=3.1, theta=0.5)"
```

### Actions

**Definition**: Long-running tasks with feedback

**Characteristics**:
- **Asynchronous**: Non-blocking
- **Feedback**: Progress updates
- **Cancelable**: Can cancel mid-execution
- **Goal-Result-Feedback**: Three-part communication

**Example**:
```
Client: "Navigate to (10, 5)" (goal)
Server: "Moving... 50% complete" (feedback)
Server: "Arrived!" (result)
```

## Communication Patterns

### Pub-Sub (Topics)

**When to Use**:
- Streaming data (sensor data, commands)
- One-to-many communication
- Don't need response

**Example**:
```
Camera → Image Topic → [Detector, Visualizer, Recorder]
```

### Request-Response (Services)

**When to Use**:
- Need immediate response
- One-time queries
- Configuration changes

**Example**:
```
Client → "Get current pose" → Service → Response
```

### Action Pattern

**When to Use**:
- Long-running tasks
- Need progress updates
- May need to cancel

**Example**:
```
Client → "Navigate to goal" → Action Server
         ← "50% complete" (feedback)
         ← "Arrived" (result)
```

## Node Graph

### Concept

**Node Graph**: Visualization of all nodes and their connections

```
Node A (publisher) → Topic X → Node B (subscriber)
Node C (service server) ← Service Y ← Node D (client)
```

### Tools

**rqt_graph**: Visualize node graph
**ros2 node list**: List all nodes
**ros2 topic list**: List all topics

## Execution Model

### Single-Threaded Executor

**Default**: One thread per node

**Characteristics**:
- Simple
- Callbacks execute sequentially
- Blocking callbacks block everything

**Use When**:
- Simple nodes
- Callbacks are fast
- No blocking operations

### Multi-Threaded Executor

**Multiple threads**: Parallel callback execution

**Characteristics**:
- Callbacks can run in parallel
- Need synchronization for shared data
- More complex

**Use When**:
- Multiple callbacks
- Some callbacks are slow
- Need parallelism

### Composition

**Node Composition**: Multiple nodes in one process

**Benefits**:
- Lower latency (no inter-process communication)
- More efficient
- Easier deployment

**Trade-offs**:
- Less modular
- All nodes share process

## Lifecycle

### Node States

**Unconfigured** → **Inactive** → **Active** → **Finalized**

**State Transitions**:
- `configure`: Initialize
- `activate`: Start processing
- `deactivate`: Stop processing
- `cleanup`: Clean up resources
- `shutdown`: Terminate

### Lifecycle Nodes

**Purpose**: Controlled startup/shutdown

**Use When**:
- Need ordered initialization
- Complex resource management
- System-level coordination

## Parameter System

### Parameters

**Definition**: Configuration values for nodes

**Characteristics**:
- Can be set at launch
- Can be changed at runtime
- Typed (string, int, double, etc.)
- Can be declared in code

**Example**:
```python
# Declare parameter
self.declare_parameter('max_speed', 1.0)

# Get parameter
max_speed = self.get_parameter('max_speed').value
```

### Parameter Files

**YAML format**:
```yaml
node_name:
  ros__parameters:
    max_speed: 1.0
    enable_logging: true
```

## Launch System

### Launch Files

**Purpose**: Start multiple nodes, configure system

**Capabilities**:
- Start nodes
- Set parameters
- Remap topics
- Set environment variables
- Conditional execution

**Example**:
```python
# Launch file
Node(
    package='my_package',
    executable='my_node',
    parameters=[{'max_speed': 1.0}],
    remappings=[('/cmd_vel', '/robot/cmd_vel')]
)
```

## Time and Clocks

### ROS Time

**Types**:
- **Wall time**: Real-world time
- **Simulation time**: Time in simulation
- **System time**: System clock

### Clock Topics

**/clock**: Publishes current time (simulation)

**Use**: Synchronize nodes to simulation time

## TF2 (Transform Library)

### Purpose

**Maintain transform tree** between coordinate frames

### Concepts

**Transform Tree**: Hierarchical frames
**Broadcaster**: Publishes transforms
**Listener**: Queries transforms

### Example

```
world → base_link → camera_link
```

**Broadcast**:
```python
tf_broadcaster.sendTransform(
    translation=(x, y, z),
    rotation=quaternion,
    parent='base_link',
    child='camera_link'
)
```

**Lookup**:
```python
transform = tf_buffer.lookup_transform(
    'base_link', 'camera_link', time
)
```

## Common Patterns

### 1. Sensor → Processing → Control

```
sensor_node → raw_data_topic → 
processing_node → processed_data_topic → 
control_node → command_topic → actuator
```

### 2. Service for Configuration

```
config_client → config_service → config_server
(one-time setup)
```

### 3. Action for Long Tasks

```
navigation_client → navigate_action → 
navigation_server (with feedback)
```

### 4. Parameter for Tuning

```
Launch file → parameters → nodes
(runtime configuration)
```

## Best Practices

### 1. Single Responsibility

**Each node does one thing well**

**Bad**: One node does everything
**Good**: Separate nodes for sensing, processing, control

### 2. Use Appropriate Communication

**Topics**: Streaming data
**Services**: Request-response
**Actions**: Long tasks

### 3. Handle Timeouts

**Services/Actions**: Set timeouts
**Topics**: Check message age

### 4. Error Handling

**Robust**: Handle missing topics, failed services
**Graceful**: Degrade gracefully

### 5. Resource Management

**Lifecycle**: Use lifecycle nodes for complex systems
**Cleanup**: Properly clean up resources

## Mental Model Summary

**ROS2 as a Distributed System**:
- Nodes = Independent processes
- Topics = Message queues
- Services = RPC calls
- Actions = Async RPC with feedback

**Think of ROS2 as**:
- **Middleware**: Handles communication
- **Toolkit**: Provides common functionality
- **Ecosystem**: Reusable packages
- **Framework**: Structure for robot software

**Key Insights**:
1. **Decoupling**: Nodes don't know about each other directly
2. **Asynchronous**: Most communication is async
3. **Modular**: Build from components
4. **Distributed**: Can run across machines

## Next Steps

- Learn about [Simulation](./simulation.md) in ROS2
- Understand [Deployment](./deployment.md) strategies
- Review [System Architecture](../02_system_architecture/) for integration


