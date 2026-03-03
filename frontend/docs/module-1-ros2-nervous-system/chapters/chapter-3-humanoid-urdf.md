# Chapter 3: Humanoid Robot URDF - Modeling the Physical Body

> **Learning Objectives**: By the end of this chapter, you will be able to:
> - Explain the purpose and structure of URDF files
> - Create a URDF defining links and joints for a humanoid robot
> - Validate URDF files using the check_urdf tool
> - Visualize robot models in RViz or Gazebo
> - Interpret joint hierarchies and coordinate frames

## Prerequisites

- Completion of Chapter 1 (ROS 2 Fundamentals)
- Completion of Chapter 2 (Python Agent Integration)
- Understanding of coordinate frames and transformations
- Basic knowledge of XML structure

## Why Robot Modeling Matters

In Chapter 2, you controlled a humanoid robot's joints. Now we'll define what the robot **is**—its shape, joints, and physical properties.

**URDF (Unified Robot Description Format)** is XML that describes a robot's structure for ROS 2. It defines:
- What body parts exist (links)
- How they connect (joints)
- How they can move (joint types and limits)

Without URDF, simulators don't know what to render, and controllers don't know what to control.

## URDF Fundamentals

URDF uses two core elements:

### 1. Links (Body Parts)

A **link** is a rigid body part. Each link has:

```xml
<link name="left_upper_arm">
  <visual>
    <geometry><cylinder length="0.3" radius="0.05"/></geometry>
  </visual>
  <inertial>
    <mass value="1.5"/>
    <inertia ixx="0.01" ixy="0.0" ixz="0.0"
             iyy="0.01" iyz="0.0" izz="0.01"/>
  </inertial>
</link>
```

- **visual**: How it looks (for rendering)
- **collision**: Physical shape for physics
- **inertial**: Mass properties for dynamics

### 2. Joints (Connections)

A **joint** connects two links and defines their movement:

```xml
<joint name="left_elbow" type="revolute">
  <parent link="left_upper_arm"/>
  <child link="left_forearm"/>
  <origin xyz="0.0 0.0 -0.15" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-2.5" upper="2.5" effort="50.0" velocity="1.0"/>
</joint>
```

**Joint Types**:
- **revolute**: Rotates around one axis (elbow, shoulder)
- **prismatic**: Slides along one axis (piston)
- **fixed**: No movement (rigid attachment)
- **continuous**: Rotates infinitely (wheel)

### Coordinate Frames

URDF builds a **tree structure** of links and joints:

```
torso (root)
  ├── left_shoulder → left_elbow
  └── right_shoulder → right_elbow
```

Moving the torso moves everything attached to it.

## Designing a Simple Humanoid

Our humanoid has:
- **Torso**: Central body (root link)
- **Head**: Attached to torso
- **Arms**: Left and right with shoulder and elbow joints

**Physical Properties**:
- **Mass**: Torso ~10kg, arms ~1.5kg each
- **Dimensions**: Human-like proportions
- **Joint Limits**: Human-like ranges (elbow: 0-150°)

A full humanoid has 30+ joints. Our 7-joint model demonstrates URDF concepts without overwhelming complexity.

## Building the URDF Step-by-Step

### Step 1: Root Link

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <link name="torso">
    <visual>
      <geometry><box size="0.3 0.2 0.5"/></geometry>
    </visual>
    <inertial>
      <mass value="10.0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0"
               iyy="0.1" iyz="0.0" izz="0.1"/>
    </inertial>
  </link>
</robot>
```

### Step 2: Add Arm Links and Joints

Define the upper arm link and connect it to torso:

```xml
<link name="left_upper_arm">
  <visual>
    <geometry><cylinder length="0.3" radius="0.05"/></geometry>
  </visual>
  <inertial><mass value="1.5"/>
    <inertia ixx="0.01" ixy="0.0" ixz="0.0"
             iyy="0.01" iyz="0.0" izz="0.01"/>
  </inertial>
</link>

<joint name="left_shoulder" type="revolute">
  <parent link="torso"/>
  <child link="left_upper_arm"/>
  <origin xyz="0.18 0.0 0.4" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.57" upper="1.57" effort="50.0" velocity="1.0"/>
</joint>
```

Add forearm and elbow joint similarly. Repeat for right arm.

## Validating and Visualizing

### Validation with check_urdf

ROS 2 provides a tool to verify URDF syntax:

```bash
check_urdf simple_humanoid.urdf
```

**Expected output**:
```
robot name is: simple_humanoid
---------- Successfully Parsed XML ---------------
root link: torso
has 2 children: left_shoulder, right_shoulder
```

If there's an error (missing tag, invalid value), check_urdf will report the line number.

### Visualizing in RViz

```bash
ros2 run rviz2 rviz2
```

1. Add "RobotModel" display
2. Set "Robot Description" to your URDF file path
3. Robot appears as 3D model

### Loading in Gazebo

```bash
ros2 launch gazebo_ros gazebo.launch.py
```

In another terminal:
```bash
ros2 run gazebo_ros spawn_entity.py -entity simple_humanoid -file simple_humanoid.urdf
```

Gazebo loads the robot with physics, allowing you to interact with it.

## Extending the Model

Once your basic humanoid works, consider enhancements:

**Add Collision Geometry**:
```xml
<collision>
  <geometry><cylinder length="0.3" radius="0.05"/></geometry>
</collision>
```
Collision shapes can be simpler than visual (faster physics).

**Add Materials**:
```xml
<material name="blue"><color rgba="0.0 0.0 1.0 1.0"/></material>
```

**Add Sensors**: Cameras, IMUs, or LIDAR using `<sensor>` tags (see Gazebo documentation).

## Common Pitfalls

### 1. Missing Inertial Properties

**Cause**: Links without `<inertial>` tags

**Symptom**: Robot explodes or floats in Gazebo

**Solution**: Always include mass and inertia properties. Use simplified inertia tensors (diagonal values) if not calculating exact values.

### 2. Joint Hierarchy Cycles

**Cause**: Creating loops in joint connections (e.g., A→B→A)

**Symptom**: check_urdf error: "graph is not a tree"

**Solution**: URDF requires tree structure (no loops). For complex structures, use multiple links with fixed joints.

### 3. Wrong Origin Frames

**Cause**: Misunderstanding parent vs child coordinate frames

**Symptom**: Robot parts appear in wrong positions

**Solution**: The origin is the **child's frame relative to parent**. Use RViz visualization to debug positions.

### 4. Invalid Joint Limits

**Cause**: lower > upper or nonsensical limits

**Symptom**: Joints can't move or crash controllers

**Solution**: Use realistic limits based on human anatomy. Test with small motions first.

### 5. Malformed XML

**Cause**: Unclosed tags, invalid characters, wrong attribute names

**Symptom**: Parser errors at line X

**Solution**: Use XML validator or text editor with syntax highlighting. Run check_urdf frequently during development.

## Summary

You learned to define humanoid robot structure using URDF:

**Key Takeaways**:
- **Links**: Rigid body parts with visual, collision, and inertial properties
- **Joints**: Define how links connect and move (revolute, prismatic, fixed)
- **Hierarchy**: Tree structure—root connects to children, grandchildren, etc.
- **Validation**: check_urdf catches syntax errors before simulation
- **Visualization**: RViz/Gazebo verify geometry and joint movements

**Complete Journey**:
- Chapter 1: ROS 2 **concepts**
- Chapter 2: **Control** joints
- Chapter 3: **Define** the robot

You can now create and control custom robots in ROS 2.

## References

- [URDF Tutorial](http://wiki.ros.org/urdf/Tutorials) - Complete guide with examples
- [URDF XML Specification](http://wiki.ros.org/urdf/XML) - Official tag reference
- [Gazebo URDF Reference](https://gazebosim.org/docs/fortress/urdf) - Simulation-specific URDF extensions
