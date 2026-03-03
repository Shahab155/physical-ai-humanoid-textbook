---
title: "Chapter 2: Sensor Simulation"
sidebar_label: "Chapter 2"
description: "Learn to integrate LiDAR, Depth Camera, and IMU sensors into robot models and visualize data in ROS 2"
---

# Chapter 2: Sensor Simulation

## Introduction

Sensors are the perception system of robots, enabling them to understand their environment. This chapter teaches you to integrate simulated sensors (LiDAR, Depth Camera, IMU) into your Gazebo robot models and visualize the sensor data using ROS 2 and RViz2.

**Why simulate sensors?** Sensor simulation is safer, cheaper, and more reproducible than testing with real hardware. You can test perception algorithms in diverse scenarios without damaging expensive equipment.

## LiDAR Sensor

LiDAR (Light Detection and Ranging) uses laser beams to measure distances to objects, generating 2D or 3D point clouds of the environment.

### LiDAR Plugin Configuration

```xml
<gazebo reference="laser_link">
  <sensor type="ray" name="laser_scanner">
    <pose>0 0 0 0 0 0</pose>
    <visualize>true</visualize>
    <update_rate>10</update_rate>
    <ray>
      <scan>
        <horizontal>
          <samples>360</samples>
          <resolution>1</resolution>
          <min_angle>-1.570796</min_angle>
          <max_angle>1.570796</max_angle>
        </horizontal>
        <range>
          <min>0.05</min>
          <max>10.0</max>
          <resolution>0.01</resolution>
        </range>
      </scan>
    </ray>
    <plugin name="gazebo_ros_laser" filename="libgazebo_ros_laser.so">
      <ros>
        <remapping>~/out:=scan</remapping>
      </ros>
      <topic_name>/scan</topic_name>
      <frame_name>laser_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

**Key Parameters**:
- `update_rate`: 10 Hz (10 scans per second)
- `samples`: 360 rays (1-degree resolution)
- `min_angle` / `max_angle`: -90° to +90° (180° field of view)
- `range`: 0.05m to 10.0m (5cm to 10m detection range)

### ROS 2 Message: sensor_msgs/LaserScan

```
Header: stamp, frame_id
angle_min: -1.570796
angle_max: 1.570796
angle_increment: 0.0087266
time_increment: 0.0
scan_time: 0.1
range_min: 0.05
range_max: 10.0
ranges: [1.2, 1.15, 1.3, ...]  # 360 values
```

**View data**: `ros2 topic echo /scan`

## Depth Camera

Depth cameras use infrared or structured light to measure distance per pixel, generating 3D point clouds.

### Depth Camera Plugin Configuration

```xml
<gazebo reference="camera_link">
  <sensor type="depth" name="depth_camera">
    <pose>0 0 0 0 0 0</pose>
    <visualize>true</visualize>
    <update_rate>30</update_rate>
    <camera>
      <horizontal_fov>1.047</horizontal_fov>  <!-- 60 degrees -->
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100.0</far>
      </clip>
    </camera>
    <plugin name="depth_camera_controller" filename="libgazebo_ros_camera.so">
      <ros>
        <remapping>~/image_raw:=depth/image_raw</remapping>
        <remapping>~/camera_info:=depth/camera_info</remapping>
      </ros>
    </plugin>
  </sensor>
</gazebo>
```

**Key Parameters**:
- `update_rate`: 30 Hz (30 frames per second)
- `horizontal_fov`: 60° field of view
- `width` / `height`: 640x480 resolution (VGA)
- `near` / `far`: 0.1m to 100m depth range

### ROS 2 Messages: sensor_msgs/Image & CameraInfo

**Depth Image**:
```
Header: stamp, frame_id
height: 480
width: 640
encoding: "16UC1"  # 16-bit unsigned, single channel (millimeters)
data: [0x00, 0x10, ...]  # Binary depth data
```

**Camera Info**:
```
Header: stamp, frame_id
height: 480
width: 640
K: [525.0, 0.0, 319.5, 0.0, 525.0, 239.5, 0.0, 0.0, 1.0]  # Intrinsic matrix
```

**View data**: `ros2 topic echo /depth/image_raw`

## IMU Sensor

IMU (Inertial Measurement Unit) measures linear acceleration and angular velocity using accelerometers and gyroscopes.

### IMU Plugin Configuration

```xml
<gazebo reference="imu_link">
  <sensor type="imu" name="imu_sensor">
    <pose>0 0 0 0 0 0</pose>
    <update_rate>100</update_rate>
    <always_on>true</always_on>
    <visualize>true</visualize>
    <plugin name="imu_controller" filename="libgazebo_ros_imu.so">
      <ros>
        <remapping>~/out:=imu/data</remapping>
      </ros>
      <topic_name>/imu/data</topic_name>
      <frame_name>imu_link</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

**Key Parameters**:
- `update_rate`: 100 Hz (high frequency for control)
- `always_on`: Sensor always active
- `frame_name`: TF frame for IMU data

### ROS 2 Message: sensor_msgs/Imu

```
Header: stamp, frame_id
orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}  # Quaternion
orientation_covariance: [0.0, ..., 0.0]  # 3x3 matrix
angular_velocity: {x: 0.01, y: -0.02, z: 0.0}  # rad/s
angular_velocity_covariance: [0.0, ..., 0.0]
linear_acceleration: {x: 0.1, y: 0.0, z: 9.81}  # m/s²
linear_acceleration_covariance: [0.0, ..., 0.0]
```

**View data**: `ros2 topic echo /imu/data`

## Visualizing Sensor Data in RViz2

RViz2 is the standard ROS 2 visualization tool.

### Launch RViz2

```bash
ros2 run rviz2 rviz2
```

### Configure Displays

**LiDAR (LaserScan)**:
1. Add → By topic → /scan → LaserScan
2. Set color map: Rainbow
3. Set size: 0.1m

**Depth Camera (Image)**:
1. Add → By topic → /depth/image_raw → Image
2. Set min/max value: 0 to 10000 (millimeters)

**IMU**:
1. Add → By topic → /imu/data → TF
2. Visualize orientation axes

## Multi-Sensor Integration

Combine multiple sensors on one robot for comprehensive perception.

### Sensor Placement Considerations

1. **LiDAR**: Top of robot (360° unobstructed view)
2. **Depth Camera**: Front-facing (navigation, obstacle detection)
3. **IMU**: Center of mass (accurate acceleration measurement)

### Performance Optimization

```xml
<!-- Reduce LiDAR update rate for performance -->
<update_rate>5</update_rate>  <!-- 10 Hz → 5 Hz -->

<!-- Reduce camera resolution -->
<width>320</width>
<height>240</height>  <!-- 640x480 → 320x240 -->

<!-- Disable unused sensor visualization -->
<visualize>false</visualize>
```

**Target**: Maintain 30+ FPS real-time factor with all sensors active

## Hands-On Exercise

**Task**: Add LiDAR, Depth Camera, and IMU to the differential drive robot

1. **Create sensor configs** (`sensors_config.sdf`):
   - LiDAR: 360 rays, 180° FOV, 10m range
   - Depth Camera: 640x480, 60° FOV, 100m range
   - IMU: 100 Hz, linear acceleration + angular velocity

2. **Integrate into robot** (`robot_with_sensors.urdf`):
   - Add sensor links (laser_link, camera_link, imu_link)
   - Attach sensor plugins with ROS 2 topics
   - Configure reference frames for TF

3. **Launch simulation**:
   ```bash
   gazebo obstacle_course.world
   ros2 launch module2_digital_twin sensor_visualizer.launch.py
   ```

4. **Verify sensor data**:
   ```bash
   ros2 topic list | grep -E "scan|depth|imu"
   ros2 topic echo /scan --once
   ros2 topic hz /scan
   ```

5. **Visualize in RViz2**:
   - Add LaserScan display for /scan
   - Add Image display for /depth/image_raw
   - Add TF display for /imu/data frame

**Expected Outcome**: All three sensors publish data simultaneously, RViz2 visualizes LiDAR scan, depth image, and robot orientation.

## Key Takeaways

- **LiDAR**: 2D distance measurements via laser scanning, `sensor_msgs/LaserScan`
- **Depth Camera**: 3D per-pixel distance, `sensor_msgs/Image` + `CameraInfo`
- **IMU**: Accelerometer + gyroscope, `sensor_msgs/Imu`
- **RViz2**: Standard tool for visualizing sensor data
- **Integration**: Multiple sensors require careful placement and performance tuning

**Next**: [Chapter 3: Unity Digital Twin](./chapter-03-unity-digital-twin.md) - Build high-fidelity visualizations with real-time synchronization.

---

**Word Count**: 720 words

**Code Examples**:
- [lidar_config.sdf](https://github.com/your-repo/code-examples/module-02-digital-twin/robot-models/lidar_config.sdf)
- [depth_camera_config.sdf](https://github.com/your-repo/code-examples/module-02-digital-twin/robot-models/depth_camera_config.sdf)
- [imu_config.sdf](https://github.com/your-repo/code-examples/module-02-digital-twin/robot-models/imu_config.sdf)
- [robot_with_sensors.urdf](https://github.com/your-repo/code-examples/module-02-digital-twin/robot-models/robot_with_sensors.urdf)
- [sensor_visualizer.launch.py](https://github.com/your-repo/code-examples/module-02-digital-twin/ros2-nodes/sensor_visualizer.launch.py)
- [data_logger.py](https://github.com/your-repo/code-examples/module-02-digital-twin/ros2-nodes/data_logger.py)
