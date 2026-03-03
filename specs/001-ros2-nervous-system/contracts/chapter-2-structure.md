# Chapter 2 Structure Contract: Python Agent Integration

**Chapter**: 2
**Title**: "Python Agent Integration: Bridging AI with ROS 2"
**User Story**: US2 (Implement Python Agent Control)
**Priority**: P2
**Prerequisites**: Chapter 1 completed
**Status**: Draft

## Chapter Specification

### Learning Objectives

By the end of this chapter, learners will be able to:

1. **Design** a Python agent that publishes to ROS 2 Topics
2. **Implement** subscription to robot state topics for feedback
3. **Handle** connection errors and ROS 2 initialization failures
4. **Create** a complete agent controlling a simulated humanoid robot
5. **Debug** common issues in ROS 2 Python integration

### Content Structure

**Target Word Count**: 900-1100 words

#### Section 1: From Concepts to Control (150-200 words)
- Review of Chapter 1 concepts (Nodes, Topics)
- Introduction: AI agents as robot controllers
- The humanoid robot control scenario
- Prerequisites check: Can you run a basic ROS 2 node?

#### Section 2: Designing the Agent (200-250 words)
- Agent architecture: Publisher + Subscriber pattern
- Control flow: Decision → Command → Actuation
- Topic design for humanoid control
  - `/humanoid/command/joint_angles` (agent → robot)
  - `/humanoid/state/joint_angles` (robot → agent)
  - `/humanoid/status` (robot health)
- Message types: sensor_msgs/JointState

#### Section 3: Implementing the Publisher (200-250 words)
- Creating a command publisher node
- Joint state message construction
- Timer-based command generation
- Code example: `humanoid_controller.py` (part 1)
- Why we publish, not directly control motors

#### Section 4: Implementing Feedback (200-250 words)
- Subscribing to robot state
- Callback design for state updates
- Closed-loop control concept
- Code example: `humanoid_controller.py` (part 2)
- Reading joint positions and verifying commands

#### Section 5: Error Handling & Robustness (150-200 words)
- Handling ROS 2 initialization failures
- Detecting disconnection from robot/simulation
- Graceful degradation strategies
- Code example: error handling patterns
- Timeout implementation

#### Section 6: Running in Simulation (100-150 words)
- Setting up Gazebo with humanoid robot
- Launching the simulation
- Running the agent
- Verification: Robot moves as expected

#### Section 7: Common Pitfalls (100-150 words)
- Agent starts before simulation is ready
- Topic name mismatches
- Message type mismatches
- Not spinning the node

#### Section 8: Summary (100-150 words)
- Key takeaways
- From simple control to complex behaviors
- Connection to Chapter 3 (defining the robot)

### Code Examples

**Example 1: `humanoid_controller.py`** (80-100 lines)
```python
# Complete agent controlling humanoid robot arm
# Features:
# - Publishes joint angle commands
# - Subscribes to robot state feedback
# - Handles connection errors
# - Implements graceful shutdown
#
# Topics:
# - Publish: /humanoid/command/joint_angles (sensor_msgs/JointState)
# - Subscribe: /humanoid/state/joint_angles (sensor_msgs/JointState)
#
# Usage: python humanoid_controller.py
```

**Example 2: `state_subscriber.py`** (30-40 lines)
```python
# Standalone subscriber for monitoring robot state
# Demonstrates: subscription-only pattern
# Topic: /humanoid/state/joint_angles
# Usage: ros2 run my_package state_subscriber
```

**Example 3: `error_handling.py`** (40-50 lines)
```python
# Demonstrates error handling patterns
# Features:
# - Try-except for rclpy.init()
# - Timeout waiting for publishers
# - Graceful shutdown on SIGINT
```

### Troubleshooting Tips

1. **"Agent publishes but robot doesn't move"**
   - Cause: Simulation not running or topic mismatch
   - Solution: Check `ros2 topic list` and `ros2 topic echo`

2. **"rclpy.init() fails with RcwROSException"**
   - Cause: ROS 2 environment not sourced or already initialized
   - Solution: Source setup.bash or check for existing node

3. **"Node exits with 'context was destroyed' error"**
   - Cause: Shutdown not handled properly
   - Solution: Use try-finally with `node.destroy_node()`

4. **"No messages received on subscription"**
   - Cause: Publisher not started or QoS mismatch
   - Solution: Check publisher status, verify QoS settings

5. **"Agent crashes after random time"**
   - Cause: Unhandled exception in callback
   - Solution: Wrap callback code in try-except

### References

1. **ROS 2 Tutorials - Writing a Simple Publisher/Subscriber**
   - URL: https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html
   - Sections: Publisher setup, Subscriber setup

2. **sensor_msgs/JointState Documentation**
   - URL: http://docs.ros.org/en/api/sensor_msgs/html/msg/JointState.html
   - Sections: Message fields, usage examples

3. **Gazebo ROS 2 Integration**
   - URL: https://gazebosim.org/docs/fortrose/ros2_integration
   - Sections: Spawning robots, plugin configuration

### Validation Criteria

- [ ] Word count between 900-1100
- [ ] All 3 code examples run successfully in ROS 2 Humble + Gazebo
- [ ] humanoid_controller.py controls simulated robot
- [ ] Error handling demonstrated for common failures
- [ ] All 5 troubleshooting tips present
- [ ] Learning objectives are measurable
- [ ] All references accessible
- [ ] Humanoid robot scenario (no other robot types)

### Acceptance Tests

1. **Agent Execution Test**: Learner runs humanoid_controller.py and robot moves
2. **Feedback Test**: Agent receives and displays robot state
3. **Error Handling Test**: Agent handles simulation not running gracefully
4. **Code Modification Test**: Learner modifies command to wave robot arm
5. **Independent Test**: Can run and explain without reference (US2 requirement)

---

**Contract Version**: 1.0
**Last Updated**: 2026-03-03
**Status**: Ready for content creation
