# Research: Module 1 - The Robotic Nervous System (ROS 2)

**Feature**: 001-ros2-nervous-system
**Date**: 2026-03-03
**Phase**: Phase 0 - Outline & Research

## Overview

This document consolidates research findings for creating educational content on ROS 2 fundamentals for humanoid robot control. Research covers ROS 2 architecture, Python integration (rclpy), URDF modeling, and best practices for educational technical writing.

## Research Tasks

From Technical Context in plan.md, the following areas required research:

1. ROS 2 Humble architecture and core concepts (Nodes, Topics, Services)
2. rclpy best practices for educational content
3. URDF modeling for humanoid robots
4. Gazebo simulation integration
5. Official ROS 2 documentation sources for references
6. Educational content structure for intermediate learners

---

## Decision 1: ROS 2 Distribution and Version

**Decision**: ROS 2 Humble Hawksbill (LTS)

**Rationale**:
- Long Term Support until 2027
- Most stable and widely adopted ROS 2 distribution
- Runs on Ubuntu 22.04 LTS (most common OS for robotics)
- Extensive documentation and community support
- Aligns with assumption CR-005 in specification

**Alternatives Considered**:
- **ROS 2 Iron**: Not LTS, shorter support window
- **ROS 2 Jazzy**: Too new, less documentation available
- **ROS 2 Foxy**: Older LTS, approaching end of life

**Reference**: https://docs.ros.org/en/humble/

---

## Decision 2: Python Agent Library

**Decision**: rclpy (official ROS 2 Python client library)

**Rationale**:
- Officially maintained by Open Robotics
- Full support for ROS 2 features (Nodes, Topics, Services, Parameters)
- Python 3.8+ compatibility (matches spec requirement)
- Extensive documentation and examples
- Type hints available for better IDE support

**Alternatives Considered**:
- **rospy2**: Unofficial port, not maintained, deprecated
- **Custom wrappers**: Would require additional maintenance, not beginner-friendly

**Best Practices for Educational Content**:
- Use explicit context managers for node lifecycle
- Include proper exception handling for ROS 2 errors
- Demonstrate both synchronous (Services) and asynchronous (Topics) patterns
- Show type annotations for clarity

**Reference**: https://docs.ros.org/en/humble/p/rclpy/

---

## Decision 3: Humanoid Robot URDF Structure

**Decision**: Simplified humanoid with 5 joints per arm + torso

**Rationale**:
- Simple enough for beginners to understand
- Complex enough to demonstrate URDF concepts (joints, links, hierarchies)
- Matches requirement CR-014: complete URDF example for humanoid
- Can be extended by learners for more complex robots

**Structure**:
```
humanoid_root
  ├── torso (fixed joint)
  ├── head (revolute joint - pitch/yaw)
  ├── left_arm
  │   ├── shoulder (revolute - 3 DOF)
  │   ├── elbow (revolute - 1 DOF)
  │   └── wrist (revolute - 1 DOF)
  └── right_arm
      ├── shoulder (revolute - 3 DOF)
      ├── elbow (revolute - 1 DOF)
      └── wrist (revolute - 1 DOF)
```

**Alternatives Considered**:
- **Full humanoid with legs**: Too complex for introductory content
- **Single arm manipulator**: Not humanoid, violates spec constraint
- **Mobile humanoid base**: Adds mobility complexity beyond scope

**Best Practices**:
- Use joint limits for safety
- Include inertial properties for realistic simulation
- Add visual and collision meshes
- Use consistent coordinate frames (URDF standard)

**Reference**: http://wiki.ros.org/urdf/Tutorials

---

## Decision 4: Simulation Environment

**Decision**: Gazebo Fortress (compatible with ROS 2 Humble)

**Rationale**:
- Official simulation platform for ROS 2
- Pre-installed with ROS 2 Humble desktop-full
- Excellent URDF visualization
- Physics engine for realistic robot behavior
- Extensive documentation

**Alternatives Considered**:
- **Ignition Gazebo**: Newer, but less mature documentation
- **Webots**: Good for education but not standard in ROS 2 workflow
- **RViz only**: No physics, limits learning about robot dynamics

**Best Practices for Educational Content**:
- Provide launch files for easy simulation startup
- Include world files with simple environments
- Document plugin requirements
- Show how to visualize robot state in RViz

**Reference**: https://gazebosim.org/docs/fortress

---

## Decision 5: Code Example Structure

**Decision**: Progressive complexity with standalone examples

**Rationale**:
- Each example builds on previous concepts
- Standalone files allow easy testing and modification
- Matches requirement CR-002: learning objectives → concepts → examples
- Supports requirement SC-013: 30-minute setup time

**Example Progression**:
1. **Chapter 1**:
   - `hello_world_node.py`: Minimal ROS 2 node
   - `simple_talker.py`: Basic publisher
   - `simple_listener.py`: Basic subscriber
   - `simple_service.py`: Service server/client

2. **Chapter 2**:
   - `humanoid_controller.py`: Complete agent with Topics
   - `state_subscriber.py`: Robot state feedback
   - `error_handling.py`: Connection error examples

3. **Chapter 3**:
   - `simple_humanoid.urdf`: Complete URDF model
   - `check_urdf_example.sh`: Validation script

**Best Practices**:
- Each example < 100 lines (manageable for learners)
- Include shebang and usage comments
- Use type hints for parameters
- Add docstrings explaining ROS 2 concepts

---

## Decision 6: Reference Sources

**Decision**: Official documentation + peer-reviewed sources

**Primary Sources** (minimum 5 required per CR-021):

1. **ROS 2 Humble Documentation** - Official API and concepts
   - URL: https://docs.ros.org/en/humble/
   - Type: Official documentation
   - Sections: Concepts, Tutorials, API Reference

2. **rclpy Documentation** - Python client library
   - URL: https://docs.ros.org/en/humble/p/rclpy/
   - Type: Official documentation
   - Sections: Node creation, Publishers, Subscribers, Services

3. **URDF Tutorial** - Robot modeling guide
   - URL: http://wiki.ros.org/urdf/Tutorials
   - Type: Official documentation (ROS wiki)
   - Sections: Creating a URDF, Joint types, Links

4. **Gazebo Documentation** - Simulation platform
   - URL: https://gazebosim.org/docs/fortress
   - Type: Official documentation
   - Sections: URDF in Gazebo, Plugins, Physics

5. **"ROS 2: The Next Generation Robot Software Platform"** - Academic paper
   - Authors: Ioan A. Șucan, Sachin Chitta, et al.
   - Publication: IEEE ICRA 2019
   - Type: Peer-reviewed conference paper
   - Content: ROS 2 architecture and design decisions

**Alternative Sources** (if needed):
- **"Programming ROS 2 with Python"** - O'Reilly book (if available)
- **ROS 2 Design Paper** - https://design.ros2.org/
- **Quintic ROS 2 Tutorials** - Community tutorials (vetted)

---

## Decision 7: Educational Content Structure

**Decision**: Chapter template with consistent sections

**Rationale**:
- Meets requirement CR-002: objectives, concepts, examples, steps, summary
- Provides predictable structure for learners
- Facilitates word count management (2500-4000 total)
- Supports progressive complexity

**Chapter Template**:
```markdown
# Chapter N: [Title]

## Learning Objectives
- [Measurable outcomes]

## Prerequisites
- [Required knowledge from previous chapters]

## Concepts
- [Explanations with analogies]
- [Diagrams/visual aids]

## Code Examples
- [Complete, runnable code]
- [Step-by-step walkthrough]

## Implementation Steps
1. [Setup]
2. [Execution]
3. [Verification]

## Common Pitfalls
- [Troubleshooting tips]

## Summary
- [Key takeaways]

## References
- [Citations]
```

**Best Practices**:
- 800-1200 words per chapter (balanced distribution)
- 2-4 code examples per chapter
- 3-5 common pitfalls per chapter (requirement CR-028)
- Analogies to humanoid robots throughout (requirement CR-026)

---

## Decision 8: Cross-Platform Considerations

**Decision**: Primary focus on Ubuntu 22.04 with notes for macOS/WSL

**Rationale**:
- Ubuntu is standard ROS 2 platform (requirement assumption #4)
- Reduces complexity for primary audience
- Notes enable broader accessibility without complicating main content

**Platform Support**:
- **Primary**: Ubuntu 22.04 LTS (fully supported)
- **Secondary**: macOS (notes on Homebrew installation)
- **Tertiary**: WSL2 (notes on Windows Subsystem for Linux)

**Best Practices**:
- Test all examples on Ubuntu 22.04
- Document OS-specific commands in separate callouts
- Provide platform-specific installation links
- Note Gazebo limitations on non-Linux platforms

---

## Summary of Technical Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| ROS 2 Version | Humble Hawksbill LTS | Long-term support, stable |
| Python Library | rclpy | Official, well-documented |
| URDF Structure | Simplified humanoid (5 joints/arm) | Teachable complexity |
| Simulation | Gazebo Fortress | ROS 2 standard |
| Code Examples | Progressive, standalone | Learnable, testable |
| References | 5 official/peer-reviewed | Credible, accessible |
| Content Structure | Consistent chapter template | Predictable, manageable |
| Platform Focus | Ubuntu 22.04 primary | Standard ROS 2 platform |

## Unresolved Questions

**None** - All technical decisions resolved. Ready for Phase 1 design.

## Next Steps

1. Generate data-model.md (content entities and structure)
2. Create contracts/ (chapter structure specifications)
3. Write quickstart.md (content creation workflow)
4. Update agent context with ROS 2 domain knowledge
