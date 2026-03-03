---
title: "Troubleshooting"
sidebar_label: "Troubleshooting"
description: "Common errors and solutions for Gazebo, Unity, and ROS 2 setup"
---

# Troubleshooting Guide

This guide addresses common issues encountered during Module 2 setup and implementation.

## Gazebo Issues

### Issue 1: Gazebo Won't Launch

**Symptoms**: `gazebo` command fails or window doesn't appear

**Solutions**:
```bash
# Check graphics drivers
glxinfo | grep "OpenGL renderer"

# Update NVIDIA drivers (Ubuntu)
sudo ubuntu-drivers devices
sudo apt install nvidia-driver-535

# Try software rendering
export LIBGL_ALWAYS_SOFTWARE=1
gazebo empty_world.world
```

**If still failing**: Check Gazebo version compatibility with ROS 2 distribution

---

### Issue 2: ROS 2 Topics Not Visible

**Symptoms**: `ros2 topic list` doesn't show Gazebo topics

**Solutions**:
```bash
# Ensure Gazebo-ROS 2 bridge loaded
gazebo --verbose empty_world.world -s libgazebo_ros_factory.so

# Check if plugins exist
ls /opt/ros/$ROS_DISTRO/lib/libgazebo_ros*.so

# Source workspace
source ~/ros2_ws/install/setup.bash
```

**Expected topics**: `/clock`, `/scan`, `/depth/image_raw`, `/imu/data`, `/odom`

---

## Unity Issues

### Issue 3: Unity Build Fails

**Symptoms**: Build errors or missing dependencies

**Solutions**:
```bash
# Install Unity build dependencies
sudo apt install build-essential mono-devel

# In Unity Editor: Edit → Preferences → External Tools
# Set "External Script Editor" to your preferred IDE
```

---

### Issue 4: ROS-TCP-Connector Can't Connect

**Symptoms**: Unity shows connection timeout errors

**Solutions**:
```bash
# Check firewall
sudo ufw allow 10000/tcp

# Verify ROS 2 endpoint is running
ros2 run ros_tcp_endpoint default_server_endpoint --ros-args -p ROS_TCP_PORT:=10000

# Test connectivity
netstat -an | grep 10000

# Ensure Unity and ROS 2 use same IP (localhost for local testing)
```

**Debug**: Check Unity Console for connection error messages

---

## Sensor Issues

### Issue 5: LiDAR Data Not Publishing

**Symptoms**: `/scan` topic missing or empty

**Solutions**:
```bash
# Check plugin configuration in URDF/SDF
grep -A 10 "libgazebo_ros_laser" robot_model.urdf

# Verify topic name matches
ros2 topic list | grep scan

# Check Gazebo console for plugin load errors
```

**Common fixes**: Correct plugin library name, verify topic remapping

---

### Issue 6: Depth Camera Shows Black Image

**Symptoms**: `/depth/image_raw` publishes but all zeros

**Solutions**:
```bash
# Check clip distances (near/far)
# Should be: near_clip="0.1" far_clip="10.0"

# Verify camera is pointing at objects (not empty space)
# Check depth encoding (16UC1 or 32FC1)
```

---

## Performance Issues

### Issue 7: Simulation Runs Slowly

**Symptoms**: Gazebo FPS drops below 30, laggy visualization

**Solutions**:
```bash
# Reduce sensor update rates
# LiDAR: 10 Hz → 5 Hz
# Camera: 30 Hz → 15 Hz

# Disable shadows in Gazebo GUI
# Display → No shadows

# Reduce physics update rate if acceptable
<max_step_size>0.002</max_step_size>  # 0.001 → 0.002
```

---

### Issue 8: Unity Rendering < 30 FPS

**Symptoms**: Choppy animation, delayed response

**Solutions**:
- Lower Unity quality settings (Medium → Low)
- Reduce polygon count on humanoid model
- Disable real-time lighting (use baked lighting)
- Close other GPU-intensive applications
- Update graphics drivers

---

## Installation Issues

### Issue 9: Package Dependencies Conflicts

**Symptoms**: `apt install` fails with dependency errors

**Solutions**:
```bash
# Update package lists
sudo apt update
sudo apt upgrade

# Fix broken packages
sudo apt --fix-broken install

# Remove conflicting packages
sudo apt autoremove
```

---

### Issue 10: ROS 2 Environment Not Sourced

**Symptoms**: `ros2` command not found

**Solutions**:
```bash
# Add to ~/.bashrc
echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc

# Reload shell
source ~/.bashrc

# Verify
echo $ROS_DISTRO  # Should show "foxy" or "humble"
```

---

## Getting Help

If you encounter issues not covered here:

1. **Check logs**:
   - Gazebo: `~/.gazebo/`
   - ROS 2: `~/.ros/log/`
   - Unity: Console window

2. **Search forums**:
   - [Gazebo Answers](https://answers.gazebosim.org/)
   - [ROS 2 Answers](https://answers.ros.org/)
   - [Unity Forums](https://forum.unity.com/)

3. **Verify prerequisites**: Complete [Quick Start Guide](./quickstart.md) from scratch

4. **Clean reinstall**: Remove and reinstall Gazebo/Unity if issues persist
