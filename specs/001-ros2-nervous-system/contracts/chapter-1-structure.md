# Chapter 1 Structure Contract: ROS 2 Fundamentals

**Chapter**: 1
**Title**: "ROS 2 Fundamentals: The Robotic Nervous System"
**User Story**: US1 (Learn ROS 2 Fundamentals)
**Priority**: P1
**Status**: Draft

## Chapter Specification

### Learning Objectives

By the end of this chapter, learners will be able to:

1. **Define** ROS 2 Nodes, Topics, and Services in their own words
2. **Explain** the publish-subscribe communication pattern
3. **Distinguish** when to use Topics vs. Services for robot control
4. **Create** a basic ROS 2 Node using rclpy
5. **Analyze** how Nodes form the "nervous system" of a robot

### Content Structure

**Target Word Count**: 900-1100 words

#### Section 1: Introduction to ROS 2 (150-200 words)
- What is ROS 2 and why it matters for humanoid robots
- The "robotic nervous system" analogy
- Prerequisites: Python knowledge, basic AI concepts

#### Section 2: ROS 2 Architecture (250-300 words)
- Nodes: The computational units
- Topics: Asynchronous publish-subscribe communication
- Services: Synchronous request-response communication
- Diagram showing Node/Topic relationships
- Comparison to biological nervous systems

#### Section 3: The Publish-Subscribe Pattern (200-250 words)
- How publishers and subscribers communicate
- Decoupling benefits for robot control
- Example: humanoid robot joint control via topics
- Visual aid: Message flow diagram

#### Section 4: Introduction to rclpy (200-250 words)
- What is rclpy? (ROS Client Library for Python)
- Setting up a Python ROS 2 environment
- Basic node lifecycle: initialize → spin → shutdown
- Code example: minimal "Hello World" node

#### Section 5: Common Pitfalls (100-150 words)
- Forgetting to source the ROS 2 setup
- Node not spinning (no callback execution)
- Incorrect topic naming (namespaces)

#### Section 6: Summary (100-150 words)
- Key takeaways
- Connection to next chapter (Python agents)

### Code Examples

**Example 1: `hello_world_node.py`** (15-20 lines)
```python
# Minimal ROS 2 node that prints a greeting
# Demonstrates: rclpy initialization, node creation, spinning
```

**Example 2: `simple_talker.py`** (30-40 lines)
```python
# Publisher that sends messages on a topic
# Demonstrates: Publisher creation, message types, timer callbacks
# Topic: /humanoid/status
# Message: String
```

**Example 3: `simple_listener.py`** (25-35 lines)
```python
# Subscriber that receives messages
# Demonstrates: Subscriber creation, callback functions
# Topic: /humanoid/status
```

**Example 4: `simple_service.py`** (40-50 lines)
```python
# Service server and client example
# Demonstrates: Synchronous communication
# Service: /humanoid/get_state
```

### Troubleshooting Tips

1. **"Command not found: ros2"**
   - Cause: ROS 2 environment not sourced
   - Solution: `source /opt/ros/humble/setup.bash`

2. **"Node publishes but nothing receives"**
   - Cause: Subscriber not running or topic mismatch
   - Solution: Check topic names with `ros2 topic list`

3. **"ImportError: No module named 'rclpy'"**
   - Cause: Python environment not configured
   - Solution: Source workspace setup or install rclpy

4. **"Node exits immediately"**
   - Cause: Node not spinning (no callbacks executing)
   - Solution: Add `rclpy.spin(node)` or use `spin_once` in loop

### References

1. **ROS 2 Concepts**
   - URL: https://docs.ros.org/en/humble/Concepts/Basic.html
   - Sections: Nodes, Topics, Services

2. **rclpy Documentation**
   - URL: https://docs.ros.org/en/humble/p/rclpy/
   - Sections: Creating a node, Publishers, Subscribers

### Validation Criteria

- [ ] Word count between 900-1100
- [ ] All 4 code examples run successfully in ROS 2 Humble
- [ ] All code includes explanatory comments
- [ ] At least 1 diagram/visual aid included
- [ ] All 4 troubleshooting tips present
- [ ] Learning objectives are measurable
- [ ] All references accessible and properly formatted
- [ ] Humanoid robot examples only (no wheeled robots)

### Acceptance Tests

1. **Quiz Definition Test**: Learner can define Nodes, Topics, Services without reference
2. **Concept Explanation Test**: Learner explains publish-subscribe in own words
3. **Code Execution Test**: Learner runs hello_world_node.py successfully
4. **Distinction Test**: Learner identifies when to use Topic vs. Service

---

**Contract Version**: 1.0
**Last Updated**: 2026-03-03
**Status**: Ready for content creation
