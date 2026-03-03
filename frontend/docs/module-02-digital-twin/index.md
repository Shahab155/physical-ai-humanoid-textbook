---
title: "Module 2: The Digital Twin (Gazebo & Unity)"
sidebar_label: "Digital Twin"
sidebar_position: 2
description: "Learn physics simulation with Gazebo, sensor integration, and high-fidelity digital twin visualization with Unity"
---

# Module 2: The Digital Twin (Gazebo & Unity)

## Overview

This module introduces intermediate robotics students to physics simulation and digital twin visualization using Gazebo and Unity. You'll learn to create realistic simulation environments, integrate sensors (LiDAR, Depth Camera, IMU), and build high-fidelity digital twins with real-time ROS 2 synchronization.

## What You'll Learn

- **Gazebo Physics Simulation**: Create and configure simulation environments with realistic physics, gravity, and collision detection
- **Sensor Integration**: Add simulated sensors to robots, visualize data in ROS 2, and understand sensor message types
- **Unity Digital Twin**: Build high-fidelity visualizations with humanoid robots and real-time synchronization

## Prerequisites

Before starting this module, ensure you have:

- **ROS 2 Installation**: ROS 2 Humble (Ubuntu 22.04) or Foxy (Ubuntu 20.04) installed
- **Python Basics**: Familiarity with Python 3.8+ and command-line operations
- **Module 1 Completion**: Understanding of basic ROS 2 concepts (topics, nodes, launch files)
- **Hardware Access**: Computer with dedicated GPU for Unity rendering
- **Gazebo & Unity**: Will be installed during this module (see Quick Start)

## Module Structure

This module consists of three progressive chapters:

1. **[Gazebo Physics Simulation](./chapter-01-gazebo-physics.md)** - Set up simulation environments with realistic physics
2. **[Sensor Simulation](./chapter-02-sensor-simulation.md)** - Integrate LiDAR, Depth Camera, and IMU sensors
3. **[Unity Digital Twin](./chapter-03-unity-digital-twin.md)** - Build high-fidelity digital twins with real-time sync

## Learning Objectives

By the end of this module, you will be able to:

- ✅ Create Gazebo world files with custom physics settings (gravity, solver parameters)
- ✅ Spawn and control robot models in simulation with collision detection
- ✅ Integrate simulated sensors (LiDAR, Depth Camera, IMU) into robot models
- ✅ Visualize sensor data using RViz2 and understand ROS 2 message types
- ✅ Build Unity scenes with humanoid robot models
- ✅ Implement real-time synchronization between Gazebo and Unity (&lt;100ms latency)

## Quick Start

1. **Set up your environment** following the [Quick Start Guide](./quickstart.md)
2. **Troubleshoot issues** with the [Troubleshooting Guide](./troubleshooting.md)
3. **Reference ROS 2 messages** in [Message Reference](./ros2-messages.md)
4. **Reference Unity interfaces** in [Interface Reference](./unity-interfaces.md)

## Estimated Time

- **Chapter 1 (Gazebo Physics)**: 2-3 hours
- **Chapter 2 (Sensor Simulation)**: 3-4 hours
- **Chapter 3 (Unity Digital Twin)**: 4-5 hours
- **Total**: 9-12 hours

## Success Criteria

You'll successfully complete this module if you can:

- Create a functional Gazebo simulation environment within 30 minutes
- Integrate sensors and verify data streams on ROS 2 topics
- Build a Unity digital twin that syncs with Gazebo in real-time

Let's get started with [Chapter 1: Gazebo Physics Simulation](./chapter-01-gazebo-physics.md)!

---

## Module Summary

Congratulations on completing Module 2: The Digital Twin! You've mastered:

### Core Skills Acquired

1. **Physics Simulation** (Gazebo)
   - Created custom world files with SDF XML
   - Configured ODE physics engine parameters (gravity, solver, friction)
   - Spawned robots with URDF models and collision detection
   - Tested realistic robot-environment interactions

2. **Sensor Integration** (ROS 2)
   - Integrated LiDAR, Depth Camera, and IMU sensors into robot models
   - Configured sensor plugins with proper ROS 2 topic publishing
   - Visualized sensor data in RViz2 (LaserScan, Image, TF displays)
   - Logged sensor data for offline analysis

3. **Digital Twin Visualization** (Unity)
   - Set up Unity projects with ROS-TCP-Connector
   - Imported humanoid robot models with Mecanim rig
   - Implemented real-time synchronization (&lt;100ms latency)
   - Built high-fidelity visualizations with smooth animations

### What's Next?

You're now ready for advanced robotics topics:

- **Module 3: Navigation & Path Planning**: Apply your simulation skills to autonomous navigation
- **Module 4: Computer Vision**: Use your sensor data for object detection and tracking
- **Module 5: Human-Robot Interaction**: Extend your digital twin for interactive demonstrations

### Key References

- [Gazebo Documentation](http://gazebosim.org/tutorials)
- [ROS 2 Humble Docs](https://docs.ros.org/en/humble/)
- [ Unity Robotics](https://github.com/Unity-Technologies/ROS-TCP-Connector)

### Troubleshooting

Encountered issues? Review the [Troubleshooting Guide](./troubleshooting.md) or check the [Quick Start Guide](./quickstart.md).

---

**Next Module**: [Module 3: Navigation & Path Planning](../03-navigation/)
