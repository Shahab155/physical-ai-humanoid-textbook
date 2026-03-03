---
title: "Chapter 1: Gazebo Physics Simulation"
sidebar_label: "Chapter 1"
description: "Learn to create Gazebo simulation environments with realistic physics, collisions, and robot spawning"
---

# Chapter 1: Gazebo Physics Simulation

## Introduction

Gazebo is a powerful 3D robotics simulator that enables you to test robot behaviors in realistic physical environments before deploying to real hardware. This chapter teaches you to create simulation environments with accurate physics, collision detection, and robot interaction.

**Why simulate first?** Simulation saves time, reduces hardware wear, and enables safe testing of dangerous scenarios. Real-world deployment becomes faster and more reliable when algorithms are validated in simulation.

## Physics Engine Configuration

Gazebo uses the Open Dynamics Engine (ODE) by default, providing realistic physics simulation including:

- **Gravity**: Earth's gravitational acceleration (9.8066 m/s²)
- **Collision Detection**: Accurate contact between objects
- **Friction**: Static and dynamic friction coefficients
- **Solver Parameters**: Time step size, update rate, real-time factor

### Basic Physics Configuration

```xml
<physics type='ode' default='true'>
  <max_step_size>0.001</max_step_size>
  <real_time_factor>1.0</real_time_factor>
  <real_time_update_rate>1000</real_time_update_rate>
  <gravity>0.0 0.0 -9.8066</gravity>
</physics>
```

**Key Parameters**:
- `max_step_size`: Time between physics updates (0.001s = 1kHz)
- `real_time_factor`: 1.0 = real-time, 2.0 = 2x speed
- `gravity`: Earth's gravity vector (x, y, z in m/s²)

## Creating World Files

World files (`.world`) define your simulation environment using SDF (Simulation Description Format) XML.

### World File Structure

```xml
<?xml version='1.0'?>
<sdf version='1.6'>
  <world name='my_world'>
    <physics>...</physics>
    <scene>
      <ambient>0.4 0.4 0.4 1</ambient>
      <background>0.7 0.7 0.7 1</background>
    </scene>
    <model name='table'>...</model>
    <model name='robot'>...</model>
  </world>
</sdf>
```

**Components**:
- `<physics>`: Engine settings (gravity, solver)
- `<scene>`: Visual appearance (lighting, background)
- `<model>`: Physical objects (robots, obstacles, furniture)

### Example: Empty World

```xml
<?xml version='1.0'?>
<sdf version='1.6'>
  <world name='empty_world'>
    <physics type='ode' default='true'>
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <gravity>0.0 0.0 -9.8066</gravity>
    </physics>
    <scene>
      <ambient>0.4 0.4 0.4 1</ambient>
      <background>0.7 0.7 0.7 1</background>
      <shadows>true</shadows>
    </scene>
  </world>
</sdf>
```

**Launch**: `gazebo empty_world.world`

## Collision Detection

Gazebo automatically detects collisions between models based on their physical properties.

### Material Properties

```xml
<surface>
  <friction>
    <ode>
      <mu>0.8</mu>        <!-- Static friction -->
      <mu2>0.6</mu2>       <!-- Dynamic friction -->
    </ode>
  </friction>
  <contact>
    <ode>
      <kp>1000000.0</kp>   <!-- Contact stiffness -->
      <kd>1.0</kd>         <!-- Contact damping -->
      <min_depth>0.001</min_depth>
    </ode>
  </contact>
</surface>
```

**Friction Values**:
- `mu`: Static friction (force to start moving)
- `mu2`: Dynamic friction (force to keep moving)
- Higher values = more friction (rubber: 0.9, ice: 0.1)

## Robot Spawning

Spawn robots into your simulation using URDF (Unified Robot Description Format) or SDF models.

### Differential Drive Robot (URDF)

```xml
<?xml version='1.0'?>
<robot name='diff_drive_robot'>
  <base_link name='base_link'>
    <inertial>
      <mass value="5.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0"
               iyy="0.1" iyz="0.0"
               izz="0.1"/>
    </inertial>
    <visual>
      <geometry><cylinder radius="0.2" length="0.1"/></geometry>
    </visual>
    <collision>
      <geometry><cylinder radius="0.2" length="0.1"/></geometry>
    </collision>
  </base_link>

  <wheel name="wheel_left">
    <parent base_link="base_link"/>
    <joint type="revolute">
      <axis xyz="0 0 1"/>
      <limit lower="-1.0" upper="1.0"/>
    </joint>
  </wheel>

  <wheel name="wheel_right">
    <parent base_link="base_link"/>
    <joint type="revolute">
      <axis xyz="0 0 1"/>
      <limit lower="-1.0" upper="1.0"/>
    </joint>
  </wheel>
</robot>
```

**Spawn**: `ros2 service call /spawn_entity gazebo_msgs/Spawn "{name: 'robot', xml: '$(cat robot.urdf)'}"`

## Hands-On Exercise

**Task**: Create a simulation environment with obstacles and a robot

1. **Create a world file** (`my_world.world`):
   - Set gravity to Earth's standard
   - Add a ground plane
   - Add 3 box obstacles at different positions

2. **Create a robot model** (`my_robot.urdf`):
   - Define a chassis (box, 5kg)
   - Add 2 wheels with revolute joints
   - Include inertial properties

3. **Launch simulation**:
   ```bash
   gazebo my_world.world
   ros2 run my_robot spawn_robot.launch.py
   ```

4. **Verify physics**:
   - Push the robot (Gazebo GUI → Manual Control)
   - Confirm collisions with obstacles
   - Check realistic movement (no floating/sliding)

**Expected Outcome**: Robot moves realistically, stops at obstacles, gravity pulls objects downward.

## Key Takeaways

- **Physics Engine**: ODE provides realistic gravity, collisions, friction
- **World Files**: SDF XML defines simulation environment
- **URDF Models**: Describe robot links, joints, inertial properties
- **Collision Detection**: Automatic based on geometry and material properties
- **Spawning**: ROS 2 services dynamically insert robots into simulation

**Next**: [Chapter 2: Sensor Simulation](./chapter-02-sensor-simulation.md) - Add LiDAR, Depth Camera, and IMU sensors to your robot.

---

**Word Count**: 680 words

**Code Examples**:
- [basic_world.world](https://github.com/your-repo/code-examples/module-02-digital-twin/gazebo-worlds/basic_world.world)
- [obstacle_course.world](https://github.com/your-repo/code-examples/module-02-digital-twin/gazebo-worlds/obstacle_course.world)
- [diff_drive_robot.urdf](https://github.com/your-repo/code-examples/module-02-digital-twin/robot-models/diff_drive_robot.urdf)
- [spawn_robot.launch.py](https://github.com/your-repo/code-examples/module-02-digital-twin/ros2-nodes/spawn_robot.launch.py)
