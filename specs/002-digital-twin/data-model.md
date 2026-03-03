# Data Model: Module 2 - The Digital Twin (Gazebo & Unity)

**Feature**: 002-digital-twin
**Date**: 2026-03-03
**Phase**: Phase 1 - Design & Contracts

## Overview

This document defines the key entities involved in robotics simulation with Gazebo and Unity digital twin visualization. These entities represent the data structures and communication patterns used throughout the module.

---

## Core Entities

### 1. Gazebo World Entity

**Purpose**: Container for simulation environment including physics settings, models, and environment objects.

**Attributes**:
- `world_name`: string (e.g., "obstacle_course", "empty_room")
- `physics_engine`: string (default: "ode")
- `gravity`: vector3d (default: [0.0, 0.0, -9.8066] m/s²)
- `max_step_size`: float (default: 0.001 s)
- `real_time_update_rate`: int (default: 1000 Hz)
- `ambient_light`: rgba (e.g., [0.4, 0.4, 0.4, 1.0])
- `background_color`: rgba (e.g., [0.7, 0.7, 0.7, 1.0])

**Relationships**:
- Contains multiple `Model` entities (robots, obstacles, furniture)
- Has one `Physics` configuration entity

**File Format**: SDF XML (`.world` files)

**Example**:
```xml
<sdf version='1.6'>
  <world name='demo_world'>
    <physics type='ode' default='true'>
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>
    <model name='table'>...</model>
    <model name='robot'>...</model>
  </world>
</sdf>
```

---

### 2. Robot Model Entity

**Purpose**: Representation of robot physical properties, including links, joints, and sensor attachments.

**Attributes**:
- `robot_name`: string (e.g., "diff_drive_robot", "humanoid_t1")
- `model_format`: enum (URDF, SDF)
- `parent_link`: string (root link for kinematics)
- `pose`: vector6d (x, y, z, roll, pitch, yaw in meters/radians)

**Relationships**:
- Contains multiple `Link` entities (rigid bodies)
- Contains multiple `Joint` entities (connections between links)
- Has multiple `SensorPlugin` attachments

**File Formats**:
- URDF XML (`.urdf`) - ROS 2 standard
- SDF XML (`.sdf`) - Gazebo native

**Example Structure**:
```
robot (diff_drive_robot)
├── base_link (chassis)
│   ├── inertia (mass, center of mass)
│   └── collision (geometry)
├── wheel_left_joint (revolute)
├── wheel_right_joint (revolute)
├── caster_wheel_joint (continuous)
└── sensor_plugins
    ├── lidar_link
    ├── camera_link
    └── imu_link
```

---

### 3. Link Entity

**Purpose**: Rigid body component of a robot model with physical properties.

**Attributes**:
- `link_name`: string (e.g., "base_link", "wheel_left")
- `mass`: float (kilograms)
- `inertia`: matrix3x3 (moment of inertia tensor)
- `visual_geometry`: shape (box, cylinder, sphere, mesh)
- `collision_geometry`: shape (may differ from visual)
- `material`: rgba (color, shininess)

**Validation Rules**:
- Mass must be > 0
- Inertia matrix must be positive definite
- Collision and visual frames must align

---

### 4. Joint Entity

**Purpose**: Connection between two links defining relative motion constraints.

**Attributes**:
- `joint_name`: string
- `joint_type`: enum (revolute, prismatic, continuous, fixed, floating, planar)
- `parent_link`: string
- `child_link`: string
- `axis`: vector3d (rotation/translation axis)
- `limits`: {lower, upper, effort, velocity} (position/force bounds)
- `dynamics`: {damping, friction} (physical properties)

**Example**:
```xml
<joint name='wheel_left_joint' type='revolute'>
  <parent>base_link</parent>
  <child>wheel_left</child>
  <axis xyz='0 0 1'/>
  <limit lower='-1.0' upper='1.0' effort='10.0' velocity='10.0'/>
</joint>
```

---

### 5. Sensor Plugin Entity

**Purpose**: Component that generates simulated sensor data and publishes to ROS 2 topics.

**Attributes**:
- `sensor_name`: string (e.g., "laser_scanner", "depth_camera")
- `sensor_type`: enum (ray, camera, imu, contact)
- `plugin_name`: string (e.g., "libgazebo_ros_laser.so")
- `update_rate`: float (Hz, e.g., 10.0 for LiDAR)
- `topic_name`: string (ROS 2 publication target)
- `frame_id`: string (TF frame identifier)

**Relationships**:
- Attached to a `Link` entity
- Publishes to one or more `ROS 2 Topic` entities
- Has `SensorConfiguration` parameters

**Sensor-Specific Attributes**:

**LiDAR**:
- `scan_angle_min`: float (radians, e.g., -π/2)
- `scan_angle_max`: float (radians, e.g., π/2)
- `range_min`: float (meters, e.g., 0.05)
- `range_max`: float (meters, e.g., 10.0)
- `num_rays`: int (e.g., 360 samples)

**Depth Camera**:
- `image_width`: int (pixels, e.g., 640)
- `image_height`: int (pixels, e.g., 480)
- `horizontal_fov`: float (radians, e.g., 1.047)
- `near_clip`: float (meters, e.g., 0.1)
- `far_clip`: float (meters, e.g., 100.0)

**IMU**:
- `angular_velocity_noise`: float (stddev)
- `linear_acceleration_noise`: float (stddev)
- `orientation_reference_frame`: enum (world, local)

---

### 6. ROS 2 Topic Entity

**Purpose**: Communication channel for sensor data and robot state between Gazebo, Unity, and learner code.

**Attributes**:
- `topic_name`: string (e.g., "/scan", "/depth/image_raw", "/imu/data")
- `message_type`: string (e.g., "sensor_msgs/LaserScan")
- `qos_profile`: enum (sensor_data, system_default)
- `publisher_count`: int (number of active publishers)
- `subscriber_count`: int (number of active subscribers)

**Standard Topic Patterns**:
- `/scan` → sensor_msgs/LaserScan (LiDAR data)
- `/depth/image_raw` → sensor_msgs/Image (depth camera)
- `/depth/camera_info` → sensor_msgs/CameraInfo (intrinsics)
- `/imu/data` → sensor_msgs/Imu (IMU readings)
- `/clock` → rosgraph_msgs/Clock (simulation time)
- `/tf` → tf2_msgs/TFMessage (transforms)

**Data Flow**:
```
Gazebo Sensor Plugin → ROS 2 Topic → ROS 2 Node (C++/Python) → Processing/Visualization
```

---

### 7. Unity Scene Entity

**Purpose**: High-fidelity rendering environment with humanoid models and lighting.

**Attributes**:
- `scene_name`: string (e.g., "DigitalTwinScene")
- `render_pipeline`: enum (Built-in, URP, HDRP)
- `target_frame_rate`: int (default: 60)
- `quality_settings`: enum (Low, Medium, High, Ultra)

**Relationships**:
- Contains multiple `GameObject` entities
- Has `RosConnector` component for ROS 2 communication
- Has `Lighting` configuration (ambient, directional, point lights)

**GameObject Hierarchy**:
```
Scene
├── Lights
│   ├── Directional Light (sun)
│   └── Ambient Light
├── Floor
├── HumanoidRobot
│   ├── Pelvis
│   ├── Torso
│   ├── Head
│   ├── LeftArm (with joints)
│   ├── RightArm (with joints)
│   ├── LeftLeg (with joints)
│   └── RightLeg (with joints)
└── RosConnector
```

---

### 8. Digital Twin Sync Entity

**Purpose**: Real-time synchronized visualization mirroring the Gazebo simulation state.

**Attributes**:
- `sync_mode`: enum (position_only, position_rotation, full_state)
- `update_frequency`: float (Hz, e.g., 30.0)
- `interpolation`: enum (none, lerp, slerp)
- `tolerance_position`: float (meters, e.g., 0.001)
- `tolerance_rotation`: float (radians, e.g., 0.01)

**Relationships**:
- Subscribes to robot state `ROS 2 Topics`
- Updates Unity `GameObject` transforms
- Monitors synchronization latency

**Data Flow**:
```
Gazebo Robot State → ROS 2 Topic (/robot_state) → Unity RosConnector → GameObject Transform Update
```

**State Structure**:
```csharp
public class RobotState
{
    public string robot_name;           // e.g., "humanoid_t1"
    public Vector3 position;            // x, y, z in meters
    public Quaternion rotation;         // quaternion (w, x, y, z)
    public Dictionary<string, float> joint_angles;  // joint positions
    public RosMessageHeader header;     // timestamp, frame_id
}
```

---

## Data Flow Diagrams

### Sensor Data Flow

```
┌─────────────┐         ┌─────────────────┐         ┌──────────────┐
│  Gazebo     │ Publish │   ROS 2 Topics  │ Subscribe│   ROS 2 Node │
│  Sensor     │────────▶│  (sensor_msgs)  │─────────▶│  (Python/C++)│
│  Plugins    │         └─────────────────┘         └──────────────┘
└─────────────┘                                          │
                                                           │ Process/
                                                           │ Visualize
                                                           ▼
                                                    ┌──────────────┐
                                                    │   RViz2      │
                                                    │  (Display)   │
                                                    └──────────────┘
```

### Digital Twin Sync Flow

```
┌─────────────┐         ┌─────────────────┐         ┌─────────────┐
│  Gazebo     │ Publish │   ROS 2 TCP     │ Receive  │   Unity      │
│  Simulation │────────▶│   Connector     │─────────▶│   Scene      │
│  (Physics)  │         │  (localhost)    │          │  (Visual)    │
└─────────────┘         └─────────────────┘         └─────────────┘
     │                                                        │
     │ Robot State                                           │ Update
     │ (position, rotation, joints)                          │ Transforms
     ▼                                                        ▼
┌─────────────────┐                                 ┌─────────────┐
│  ROS 2 Topics   │                                 │ Humanoid    │
│ /robot_state    │                                 │ GameObject  │
│ /joint_states   │                                 └─────────────┘
└─────────────────┘
```

---

## State Transitions

### Robot Spawn Sequence

1. **Initial State**: World file loaded, no models
2. **Spawn Request**: ROS 2 service call to spawn robot SDF/URDF
3. **Model Parsing**: Gazebo parses robot description
4. **Physics Initialization**: Links and joints added to physics engine
5. **Plugin Loading**: Sensor plugins initialized, begin publishing
6. **Ready State**: Robot can receive commands, sensor data flowing

### Simulation Lifecycle

```
[START] → [LOAD WORLD] → [SPAWN ROBOTS] → [SIMULATE]
                                              ↓
                                        [PAUSE/RESUME]
                                              ↓
                                        [RESET POSE]
                                              ↓
                                        [STOP] → [CLEANUP]
```

---

## Validation Rules

### World File Validation
- XML must conform to SDF 1.6 schema
- All model references must resolve
- Physics parameters within realistic ranges

### Robot Model Validation
- URDF/SDF must be valid XML
- All joint links must exist
- No kinematic loops (except properly closed chains)
- Inertia matrices positive definite

### Sensor Plugin Validation
- Plugin library must exist in Gazebo plugin path
- Topic names must be valid ROS 2 identifiers
- Update rates > 0 Hz
- Sensor ranges physically plausible (e.g., LiDAR min < max)

### Unity Scene Validation
- All required prefabs present
- RosConnector configured with correct IP/port
- Humanoid rig valid for Mecanim animation system

---

## Summary

The data model for Module 2 encompasses physics simulation (Gazebo), sensor data streams (ROS 2 topics), and visualization (Unity). Key entities form a pipeline:

1. **Gazebo World** + **Robot Model** → Simulation environment
2. **Sensor Plugins** → Generate data
3. **ROS 2 Topics** → Transport data
4. **Unity Scene** + **Digital Twin Sync** → Visualize data

This architecture enables learners to progress from basic physics simulation to sophisticated digital twin visualization while maintaining clear separation of concerns and standard interfaces.
