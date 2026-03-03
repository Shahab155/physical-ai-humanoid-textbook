# ROS 2 Message Contracts: Module 2 - The Digital Twin

**Feature**: 002-digital-twin
**Date**: 2026-03-03
**Phase**: Phase 1 - Design & Contracts

## Overview

This document specifies the ROS 2 message types and topic conventions used in Module 2 for sensor simulation and robot state communication. All messages use standard ROS 2 `sensor_msgs` and geometry message types.

---

## Standard Message Types

### 1. sensor_msgs/LaserScan

**Purpose**: LiDAR sensor data representing distance measurements in a 2D plane.

**Topic**: `/scan`

**Message Definition**:

```
# Standard ROS 2 LaserScan message
std_msgs/Header header

# Angular configuration
float32 angle_min            # Start angle of scan [rad]
float32 angle_max            # End angle of scan [rad]
float32 angle_increment      # Angular distance between measurements [rad]

# Range configuration
float32 time_increment       # Time between measurements [seconds]
float32 scan_time            # Time between scans [seconds]
float32 range_min            # Minimum measurable range [m]
float32 range_max            # Maximum measurable range [m]

# Data arrays
float32[] ranges             # Range data [m] (length = number of samples)
float32[] intensities        # Intensity data [device-specific]
```

**Example Values**:

```yaml
angle_min: -1.5707963        # -90 degrees
angle_max: 1.5707963         # +90 degrees
angle_increment: 0.0174533   # ~1 degree
range_min: 0.05              # 5 cm minimum
range_max: 10.0              # 10 m maximum
ranges: [1.2, 1.15, 1.3, ...]  # Sample distances
```

**QoS Profile**: `sensor_data` (best effort)

---

### 2. sensor_msgs/Image

**Purpose**: Depth camera image data representing distance per pixel.

**Topic**: `/depth/image_raw`

**Message Definition**:

```
# Standard ROS 2 Image message
std_msgs/Header header

# Image configuration
uint32 height                 # Image height in pixels
uint32 width                  # Image width in pixels

# Encoding
string encoding               # Image encoding (e.g., "16UC1" for depth)
uint8 is_bigendian            # Byte order (0 = little endian)
uint32 step                   # Full row length in bytes

# Data
uint8[] data                  # Image matrix [height x step bytes]
```

**Depth-Specific Encoding**:

- **16UC1**: 16-bit unsigned integer, single channel (millimeters)
- **32FC1**: 32-bit float, single channel (meters)

**Example Configuration**:

```yaml
height: 480
width: 640
encoding: "16UC1"
is_bigendian: 0
step: 1280                    # 640 pixels * 2 bytes/pixel
data: [0x00, 0x10, ...]       # Binary depth data
```

**QoS Profile**: `sensor_data` (best effort)

---

### 3. sensor_msgs/CameraInfo

**Purpose**: Camera intrinsic parameters for image interpretation.

**Topic**: `/depth/camera_info`

**Message Definition**:

```
std_msgs/Header header

uint32 height                 # Image height
uint32 width                  # Image width

string distortion_model       # "plumb_bob", "rational_polynomial"
float64[] D                   # Distortion coefficients [5]

float64[9] K                 # Intrinsic matrix [3x3 row-major]
float64[9] R                 # Rectification matrix [3x3]
float64[12] P                # Projection matrix [3x4 row-major]

uint32 binning_x              # Binning horizontal
uint32 binning_y              # Binning vertical

sensor_msgs/RegionOfInterest roi
```

**Typical K Matrix (Intrinsics)**:

```
K = [fx  0  cx]
    [ 0  fy cy]
    [ 0  0   1]

Where:
fx, fy = focal length (pixels)
cx, cy = principal point (image center)
```

**Example Values**:

```yaml
K: [525.0, 0.0, 319.5, 0.0, 525.0, 239.5, 0.0, 0.0, 1.0]
```

---

### 4. sensor_msgs/Imu

**Purpose**: IMU sensor data providing orientation, angular velocity, and linear acceleration.

**Topic**: `/imu/data`

**Message Definition**:

```
std_msgs/Header header

# Orientation (quaternion)
geometry_msgs/Quaternion orientation
float64[9] orientation_covariance     # Covariance matrix [3x3]

# Angular velocity
geometry_msgs/Vector3 angular_velocity
float64[9] angular_velocity_covariance

# Linear acceleration
geometry_msgs/Vector3 linear_acceleration
float64[9] linear_acceleration_covariance
```

**Quaternion (x, y, z, w)**:

```
# Represents rotation from body to world frame
# For perfect alignment: [0, 0, 0, 1]
```

**Covariance Matrix**:

```
# Row-major 3x3 matrix (use 0 for unknown)
# Diagonal elements: [var_x, var_y, var_z]
```

**Example Values**:

```yaml
orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
angular_velocity: {x: 0.01, y: -0.02, z: 0.0}
linear_acceleration: {x: 0.1, y: 0.0, z: 9.81}
```

**QoS Profile**: `sensor_data` (best effort)

---

### 5. geometry_msgs/Twist

**Purpose**: Robot velocity commands (linear + angular).

**Topic**: `/cmd_vel`

**Message Definition**:

```
# Linear velocity [m/s]
geometry_msgs/Vector3 linear

# Angular velocity [rad/s]
geometry_msgs/Vector3 angular
```

**Example (Differential Drive)**:

```yaml
linear: {x: 0.5, y: 0.0, z: 0.0}    # Move forward at 0.5 m/s
angular: {x: 0.0, y: 0.0, z: 0.2}   # Rotate at 0.2 rad/s
```

**QoS Profile**: `system_default` (reliable)

---

### 6. nav_msgs/Odometry

**Purpose**: Robot pose and velocity estimates (for digital twin sync).

**Topic**: `/odom` or `/robot_state`

**Message Definition**:

```
std_msgs/Header header
string child_frame_id         # TF frame of robot base

# Pose (position + orientation)
geometry_msgs/PoseWithCovariance pose

# Velocity (linear + angular)
geometry_msgs/TwistWithCovariance twist
```

**Example**:

```yaml
pose:
  pose:
    position: {x: 1.5, y: 2.0, z: 0.0}
    orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}
twist:
  twist:
    linear: {x: 0.3, y: 0.0, z: 0.0}
    angular: {x: 0.0, y: 0.0, z: 0.1}
```

---

## Topic Naming Conventions

### Standard ROS 2 Topics

| Topic | Message Type | Publisher | Subscriber |
|-------|--------------|-----------|------------|
| `/scan` | sensor_msgs/LaserScan | Gazebo LiDAR plugin | Processing nodes, RViz2 |
| `/depth/image_raw` | sensor_msgs/Image | Gazebo camera plugin | Visualization, processing |
| `/depth/camera_info` | sensor_msgs/CameraInfo | Gazebo camera plugin | Image processing nodes |
| `/imu/data` | sensor_msgs/Imu | Gazebo IMU plugin | State estimation |
| `/cmd_vel` | geometry_msgs/Twist | Autonomy stack | Gazebo robot plugin |
| `/odom` | nav_msgs/Odometry | Gazebo diff drive plugin | Localization, Unity |
| `/clock` | rosgraph_msgs/Clock | Gazebo (simulation time) | All nodes |
| `/tf` | tf2_msgs/TFMessage | Robot state publisher | All nodes |
| `/joint_states` | sensor_msgs/JointState | Gazebo joint state publisher | Unity, visualization |

### Namespaced Topics (Multi-Robot)

For multiple robots, namespace topics:

```
/robot1/scan
/robot1/cmd_vel
/robot2/scan
/robot2/cmd_vel
```

---

## QoS Profiles

### sensor_data (Best Effort)

Used for high-frequency sensor data where occasional packet loss is acceptable:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

sensor_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE
)
```

**Applied to**: `/scan`, `/depth/image_raw`, `/imu/data`

### system_default (Reliable)

Used for critical commands and configuration:

```python
default_qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.VOLATILE
)
```

**Applied to**: `/cmd_vel`, `/odom`, `/joint_states`

---

## Service Definitions

### 1. Spawn Entity (Gazebo)

**Service**: `/spawn_entity`

**Type**: `gazebo_msgs/Spawn`

**Request**:

```
string name                     # Entity name
string xml                      # URDF/SDF string
string robot_namespace          # ROS 2 namespace
string initial_pose             # Initial pose (optional)
string reference_frame          # Reference frame
```

**Response**:

```
bool success                    # True if spawned
string status_message           # Error message if failed
```

---

## Frame IDs (TF)

### Standard Frame Tree

```
world (fixed)
 └── odom (fixed)
     └── base_link (moving robot base)
         ├── camera_link
         ├── imu_link
         ├── lidar_link
         └── wheel_left_link
         └── wheel_right_link
```

### Frame ID Naming

| Frame | Description | Parent |
|-------|-------------|--------|
| `world` | Global fixed frame | - |
| `odom` | Odometry frame | world |
| `base_link` | Robot base | odom |
| `camera_link` | Camera optical | base_link |
| `imu_link` | IMU sensor | base_link |
| `laser_link` | LiDAR sensor | base_link |

---

## Unity-ROS 2 Message Mapping

### C# Message Structures

**Equivalent C# classes for ROS 2 messages**:

```csharp
public class Vector3
{
    public float x, y, z;
}

public class Quaternion
{
    public float x, y, z, w;
}

public class Pose
{
    public Vector3 position;
    public Quaternion orientation;
}

public class RobotState
{
    public string robot_name;
    public Pose pose;
    public Dictionary<string, float> joint_positions;
    public uint32 timestamp_sec;
    public uint32 timestamp_nsec;
}
```

---

## Validation Rules

### Message Validation

1. **Header timestamps must be monotonically increasing**
2. **Frame IDs must match TF tree**
3. **Covariance matrices must be positive semi-definite**
4. **Image dimensions must match data array length**
5. **LiDAR ranges must be within [range_min, range_max] or set to NaN**

### Topic Validation

```bash
# Check topic exists
ros2 topic list | grep /scan

# Verify message type
ros2 topic info /scan

# Check message content
ros2 topic echo /scan --once
```

---

## Summary

Module 2 uses standard ROS 2 message types exclusively:

- **Sensors**: `sensor_msgs/LaserScan`, `sensor_msgs/Image`, `sensor_msgs/Imu`
- **Actuation**: `geometry_msgs/Twist` (cmd_vel)
- **State**: `nav_msgs/Odometry`, `sensor_msgs/JointState`
- **TF**: `tf2_msgs/TFMessage` for transforms

All messages follow ROS 2 conventions with standard topic names and QoS profiles.
