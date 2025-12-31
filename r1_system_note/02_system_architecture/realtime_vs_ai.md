# Real-time vs AI Systems

Robot systems must balance real-time constraints with the computational demands of AI/ML algorithms. Understanding this tension is crucial for building effective robots.

## Real-time Systems

### Characteristics

**Hard Real-time**:
- **Definition**: Missing a deadline causes system failure
- **Example**: Motor control, safety systems
- **Requirements**: Guaranteed response time
- **Consequences**: Catastrophic if deadline missed

**Soft Real-time**:
- **Definition**: Missing deadline degrades performance but doesn't fail
- **Example**: Perception, planning
- **Requirements**: Usually meet deadlines
- **Consequences**: Reduced performance if deadline missed

### Real-time Requirements

1. **Deterministic Timing**: Predictable execution time
2. **Bounded Latency**: Maximum response time guaranteed
3. **Priority Scheduling**: Critical tasks run first
4. **Resource Management**: CPU, memory, I/O reserved

### Implementation Approaches

**RTOS (Real-Time Operating System)**:
- Preemptive scheduling
- Priority-based task management
- Predictable interrupt handling
- Examples: FreeRTOS, RT-Linux, QNX

**Real-time Frameworks**:
- ROS2 with real-time support
- Deterministic execution paths
- Minimal dynamic allocation
- Lock-free data structures

## AI/ML Systems

### Characteristics

**Non-deterministic**:
- Execution time varies
- Depends on input complexity
- Hard to predict worst-case

**Computationally Intensive**:
- Deep learning inference: 10-1000ms
- Training: Hours to days
- GPU acceleration often required

**Data-Driven**:
- Requires large datasets
- Performance improves with more data
- Generalization challenges

### AI in Robotics

**Perception**:
- Object detection (YOLO, Faster R-CNN)
- Semantic segmentation
- Depth estimation
- SLAM with learned features

**Planning**:
- Learned motion primitives
- Imitation learning
- Reinforcement learning policies
- End-to-end planning networks

**Control**:
- Learned controllers
- Adaptive control
- Model learning

## The Tension

### Challenge 1: Timing Uncertainty

**Problem**: AI inference time is unpredictable
- Simple input: 10ms
- Complex input: 500ms
- **Impact**: Can't guarantee real-time deadlines

**Solutions**:
- **Time budgets**: Set maximum inference time, timeout if exceeded
- **Simplified models**: Use smaller, faster models
- **Early exit**: Return partial results if time limit reached
- **Caching**: Reuse previous results when appropriate

### Challenge 2: Computational Resources

**Problem**: AI requires significant compute
- **Control loop**: Needs CPU for real-time tasks
- **AI inference**: Needs CPU/GPU for perception/planning
- **Conflict**: Competing for same resources

**Solutions**:
- **Dedicated hardware**: Separate processors for AI and control
- **Priority scheduling**: Control gets highest priority
- **Offloading**: Run AI on separate computer/cloud
- **Edge AI**: Optimized models for edge devices

### Challenge 3: Integration Complexity

**Problem**: Combining deterministic and non-deterministic components

**Solutions**:
- **Asynchronous processing**: AI runs in separate thread/process
- **Buffering**: Queue AI results, control reads latest
- **Fallback**: Classical methods when AI unavailable
- **Hybrid systems**: AI for high-level, classical for low-level

## Architecture Patterns

### Pattern 1: Separate Real-time and AI Layers

```
┌─────────────────┐
│   AI Layer      │  (Non-real-time)
│  Perception     │  Runs asynchronously
│  Planning       │  Updates when ready
└────────┬────────┘
         │ (latest results)
┌────────▼────────┐
│ Real-time Layer │  (Hard real-time)
│   Control       │  Always runs on time
│   Safety        │  Deterministic
└─────────────────┘
```

**Benefits**:
- Control always meets deadlines
- AI can take variable time
- Clear separation of concerns

**Challenges**:
- Stale data if AI slow
- Synchronization needed

### Pattern 2: Time-Budgeted AI

```
AI Task:
1. Start inference
2. Check elapsed time
3. If > budget: return best-so-far or fallback
4. Otherwise: return full result
```

**Benefits**:
- Guaranteed maximum latency
- Graceful degradation

**Challenges**:
- May return suboptimal results
- Requires early-exit mechanisms

### Pattern 3: Hybrid Classical + AI

```
┌──────────────┐
│ Classical    │  Fast, reliable baseline
│ (always on)  │
└──────┬───────┘
       │
┌──────▼───────┐
│ AI           │  Enhances when available
│ (when ready) │  Improves performance
└──────────────┘
```

**Benefits**:
- Always functional (classical)
- Better when AI available
- Robust to AI failures

**Challenges**:
- More complex integration
- Need to merge outputs

## Practical Guidelines

### When to Use Real-time

**Use hard real-time for**:
- Motor control
- Safety systems
- Stability-critical control
- Actuator commands

**Use soft real-time for**:
- Perception updates
- Planning
- High-level control

### When to Use AI

**Use AI for**:
- Complex perception (object recognition, scene understanding)
- Learning from experience
- Handling novel situations
- Improving over time

**Avoid AI for**:
- Safety-critical control (unless extensively validated)
- Ultra-low latency requirements (<10ms)
- Deterministic requirements

### Best Practices

1. **Layer Architecture**: 
   - Real-time at bottom (control, safety)
   - AI at top (perception, planning)

2. **Time Budgets**: 
   - Set maximum time for AI tasks
   - Have fallback if exceeded

3. **Resource Isolation**: 
   - Separate CPUs/cores for real-time and AI
   - Use CPU affinity/pinning

4. **Monitoring**: 
   - Track AI inference times
   - Alert if consistently slow
   - Log for analysis

5. **Testing**: 
   - Test with worst-case AI latency
   - Verify real-time guarantees hold
   - Stress test system

## Example: Autonomous Vehicle

**Real-time (Hard)**:
- Brake control: <10ms
- Steering control: <20ms
- Collision avoidance: <50ms

**AI (Soft Real-time)**:
- Object detection: 50-200ms acceptable
- Path planning: 100-500ms acceptable
- Semantic understanding: 200-1000ms acceptable

**Architecture**:
- Dedicated ECU for brake/steering (real-time)
- GPU computer for perception (AI)
- Communication via CAN bus or Ethernet

## Next Steps

- Learn about [Coordinate Frames](../03_coordinate_frames/frames_and_transforms.md) for proper sensor fusion
- Explore [Sensors](../04_sensors/) that feed both real-time and AI systems


