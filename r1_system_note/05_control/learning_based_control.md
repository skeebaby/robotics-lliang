# Learning-Based Control

Learning-based control uses machine learning to improve robot performance by learning from data and experience, rather than relying solely on hand-designed controllers.

## What is Learning-Based Control?

Learning-based control uses:
- **Data**: Examples, demonstrations, experience
- **Machine Learning**: Neural networks, reinforcement learning
- **Adaptation**: Improves over time
- **Generalization**: Handles novel situations

**Characteristics**:
- Can handle complex systems
- Adapts to environment
- Requires training/data
- Less predictable than classical

## Types of Learning-Based Control

### 1. Imitation Learning
**Learn from demonstrations**

**Methods**:
- **Behavioral Cloning**: Supervised learning from expert
- **DAgger**: Interactive learning with expert
- **Inverse Reinforcement Learning**: Learn reward function

### 2. Reinforcement Learning
**Learn from trial and error**

**Methods**:
- **Policy Gradient**: Direct policy optimization
- **Value-Based**: Q-learning, DQN
- **Actor-Critic**: Combine policy and value

### 3. Model Learning
**Learn system dynamics**

**Methods**:
- **Neural ODEs**: Learn differential equations
- **Gaussian Processes**: Probabilistic models
- **Ensemble Methods**: Multiple models

### 4. Adaptive Control
**Online parameter adaptation**

**Methods**:
- **Model Reference Adaptive Control**: Adapt to match reference
- **Self-Tuning**: Estimate parameters online

## Imitation Learning

### Behavioral Cloning

**Process**:
1. Collect expert demonstrations
2. Train neural network: state → action
3. Deploy learned policy

**Architecture**:
```
State (s) → Neural Network → Action (a)
```

**Training**:
```
Loss = ||a_expert - a_predicted||²
```

**Pros**:
- Simple to implement
- Fast training (supervised)
- Leverages human expertise

**Cons**:
- Limited to demonstrated behaviors
- Distribution shift (train vs. test mismatch)
- No exploration

### DAgger (Dataset Aggregation)

**Process**:
1. Train initial policy from expert data
2. Run policy, collect states
3. Expert labels actions for collected states
4. Retrain on aggregated dataset
5. Repeat

**Benefits**:
- Handles distribution shift
- Improves over iterations
- Better generalization

**Challenges**:
- Requires expert during training
- Can be time-consuming

### Inverse Reinforcement Learning

**Goal**: Learn reward function from demonstrations

**Process**:
1. Expert demonstrates behavior
2. Infer reward function that explains behavior
3. Use reward for planning/control

**Benefits**:
- More general than behavioral cloning
- Can handle multiple objectives

## Reinforcement Learning

### Overview

**RL Framework**:
- **Agent**: Robot/controller
- **Environment**: World robot acts in
- **State**: Current situation
- **Action**: Control command
- **Reward**: Performance signal
- **Policy**: State → Action mapping

### Policy Gradient Methods

**REINFORCE**:
- Direct policy optimization
- Gradient ascent on expected reward
- **Pros**: Works for continuous actions
- **Cons**: High variance, slow

**PPO (Proximal Policy Optimization)**:
- Constrained policy updates
- More stable than REINFORCE
- **Pros**: Stable, good performance
- **Cons**: Requires tuning

**TRPO (Trust Region Policy Optimization)**:
- Constrained updates (trust region)
- **Pros**: Theoretically sound
- **Cons**: Computationally expensive

### Value-Based Methods

**Q-Learning**:
- Learn action-value function Q(s,a)
- **Pros**: Simple, well-understood
- **Cons**: Discrete actions only

**DQN (Deep Q-Network)**:
- Neural network for Q-function
- **Pros**: Handles high-dimensional states
- **Cons**: Discrete actions, sample inefficient

**DDPG (Deep Deterministic Policy Gradient)**:
- Continuous action extension
- **Pros**: Continuous actions, off-policy
- **Cons**: Requires tuning

### Actor-Critic Methods

**Combine policy and value**:
- **Actor**: Policy (what to do)
- **Critic**: Value function (how good)

**Benefits**:
- Lower variance than policy gradient
- More sample efficient
- Better for continuous control

**Examples**:
- A3C, A2C
- SAC (Soft Actor-Critic)
- TD3 (Twin Delayed DDPG)

## Model Learning

### Neural ODEs

**Learn dynamics**:
```
ẋ = f_θ(x, u)
where f_θ is neural network
```

**Training**:
- Collect state-action-next_state tuples
- Learn to predict next state
- Use for planning/control

**Benefits**:
- Continuous-time models
- Can use in MPC

### Gaussian Process Models

**Probabilistic dynamics**:
- Uncertainty estimates
- **Benefits**: Knows what it doesn't know
- **Use**: Safe exploration, robust control

### Ensemble Methods

**Multiple models**:
- Train several models
- Use ensemble for predictions
- **Benefits**: Robustness, uncertainty

## Hybrid Approaches

### Learning + Classical Control

**Example**: Learned feedforward + PID feedback
```
u = u_learned_feedforward + u_PID_feedback
```

**Benefits**:
- Combines strengths
- Learning handles complexity
- Classical provides stability

### Learning for High-Level, Classical for Low-Level

**Architecture**:
```
Learned Planner → Classical Controller → Actuators
```

**Benefits**:
- Learning for complex decisions
- Classical for reliable execution

## Training Considerations

### Simulation vs. Real World

**Simulation**:
- **Pros**: Fast, safe, unlimited data
- **Cons**: Sim-to-real gap
- **Use**: Initial training, pre-training

**Real World**:
- **Pros**: Realistic, no sim-to-real gap
- **Cons**: Slow, expensive, unsafe
- **Use**: Fine-tuning, final training

### Sim-to-Real Transfer

**Challenges**:
- Model mismatch
- Unmodeled dynamics
- Different sensor noise

**Solutions**:
- Domain randomization
- Robust training
- Adaptation methods

### Safety During Training

**Problem**: Exploration can be dangerous

**Solutions**:
- **Safe exploration**: Constrain actions
- **Simulation first**: Train in sim
- **Human supervision**: Monitor training
- **Safety constraints**: Hard limits

## Applications

### Manipulation
- **Task**: Pick and place, assembly
- **Methods**: Imitation learning, RL
- **Challenges**: Contact dynamics, precision

### Navigation
- **Task**: Path planning, obstacle avoidance
- **Methods**: RL, learned cost maps
- **Challenges**: Generalization, safety

### Locomotion
- **Task**: Walking, running
- **Methods**: RL, learned gaits
- **Challenges**: Stability, efficiency

### Driving
- **Task**: Autonomous driving
- **Methods**: Imitation learning, RL
- **Challenges**: Safety, generalization

## Challenges

### 1. Sample Efficiency
**Problem**: RL requires many samples

**Solutions**:
- Sim-to-real transfer
- Imitation learning (fewer samples)
- Better algorithms (more efficient)

### 2. Generalization
**Problem**: Works in training, fails in new situations

**Solutions**:
- Domain randomization
- Diverse training data
- Regularization

### 3. Safety
**Problem**: Exploration can cause damage

**Solutions**:
- Safe exploration methods
- Constrained RL
- Human oversight

### 4. Interpretability
**Problem**: Black box, hard to debug

**Solutions**:
- Interpretable architectures
- Visualization tools
- Hybrid approaches

### 5. Real-time Performance
**Problem**: Inference must be fast

**Solutions**:
- Efficient architectures
- Model compression
- Hardware acceleration

## Best Practices

1. **Start with Simulation**: Train in sim first
2. **Use Imitation Learning**: Faster than RL
3. **Combine with Classical**: Hybrid approaches
4. **Validate Thoroughly**: Test extensively
5. **Monitor Performance**: Log metrics
6. **Handle Failures**: Graceful degradation
7. **Document Training**: Hyperparameters, data

## Comparison with Classical Control

| Aspect | Classical | Learning-Based |
|--------|-----------|----------------|
| Design | Hand-designed | Data-driven |
| Complexity | Limited | Can handle complex |
| Predictability | High | Lower |
| Training | None | Required |
| Adaptation | Limited | Can adapt |
| Guarantees | Theoretical | Empirical |
| Real-time | Yes | Depends |

## When to Use Learning-Based Control

**Use when**:
- System too complex to model
- Need to adapt to environment
- Have training data/demos
- Classical methods insufficient

**Avoid when**:
- Simple system (classical sufficient)
- Safety critical (unless extensively validated)
- No training data available
- Real-time constraints very tight

## Next Steps

- Learn about [Classical Control](./classical_control.md) for comparison
- Understand [System Architecture](../02_system_architecture/perception_planning_control.md) integration
- Review [Software Stack](../06_software_stack/) for implementation


