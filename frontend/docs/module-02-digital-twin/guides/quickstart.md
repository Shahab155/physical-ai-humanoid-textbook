# Quickstart Guide: Module 2 - The Digital Twin (Gazebo & Unity)

**Feature**: 002-digital-twin
**Date**: 2026-03-03
**Phase**: Phase 1 - Design & Contracts

## Overview

This guide provides step-by-step instructions to set up your development environment for Module 2. Estimated setup time: 30-45 minutes.

---

## Prerequisites

### Before You Begin

**Required Knowledge**:
- Basic Linux command-line operations
- Python 3 fundamentals
- ROS 2 basics (topics, nodes, launch files) from Module 1

**System Requirements**:
- **Operating System**: Ubuntu 20.04 LTS (Foxy) or Ubuntu 22.04 LTS (Humble)
- **RAM**: 8 GB minimum (16 GB recommended)
- **Storage**: 20 GB free space
- **CPU**: Quad-core processor or better
- **GPU**: Dedicated graphics card (NVIDIA/AMD) for Unity rendering

**Assumptions**:
- You have ROS 2 Foxy or Humble installed (from Module 1)
- You have a working ROS 2 workspace (`~/ros2_ws`)
- You have sudo/admin access on your system

---

## Step 1: Install Gazebo

### For ROS 2 Foxy (Ubuntu 20.04)

Gazebo 11 is installed automatically with ROS 2 Foxy desktop. Verify installation:

```bash
# Check Gazebo version
gazebo --version

# Expected output: Gazebo 11.x.x
# If not installed, run:
sudo apt update
sudo apt install ros-foxy-gazebo-ros-pkgs
```

### For ROS 2 Humble (Ubuntu 22.04)

```bash
# Install Gazebo Ignition (Citadel) or Gazebo 11 bridge
sudo apt update
sudo apt install ros-humble-gazebo-ros-pkgs
sudo apt install ros-humble-ros-gz

# Verify installation
gz sim --version   # For Ignition
gazebo --version   # For Gazebo 11 (if using ros_gz bridge)
```

### Verify Installation

```bash
# Launch empty Gazebo world
gazebo empty_world.world &

# Expected: Gazebo GUI opens with empty grid world
# Press Ctrl+C to close
```

**Troubleshooting**:
- If Gazebo doesn't launch, check graphics drivers: `glxinfo | grep OpenGL`
- For GPU issues, try `export LIBGL_ALWAYS_SOFTWARE=1` before launching

---

## Step 2: Install ROS 2 Gazebo Packages

### Install Simulation Packages

```bash
# Replace 'foxy' with 'humble' for Ubuntu 22.04
sudo apt install \
    ros-foxy-gazebo-ros2-control \
    ros-foxy-ros2-controllers \
    ros-foxy-gazebo-ros-pkgs \
    ros-foxy-xacro

# For sensor simulation
sudo apt install \
    ros-foxy-rgbd-launch \
    ros-foxy-depthimage-to-laserscan
```

### Source ROS 2 Environment

Add to your `~/.bashrc` (if not already there):

```bash
echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## Step 3: Create Module Workspace

### Create Directory Structure

```bash
# Create module workspace
mkdir -p ~/ros2_ws/src/module2_digital_twin
cd ~/ros2_ws/src/module2_digital_twin

# Create subdirectories for examples
mkdir -p worlds
mkdir -p models
mkdir -p launch
mkdir -p scripts
```

### Download Example Models

```bash
# Clone example robot models (optional)
cd ~/ros2_ws/src
git clone https://github.com/ros-simulation/gazebo_ros_pkgs.git -b foxy-devel

# Build workspace
cd ~/ros2_ws
colcon build --packages-select gazebo_ros_pkgs
source install/setup.bash
```

---

## Step 4: Test Gazebo + ROS 2 Integration

### Launch Test World

Create test launch file `~/ros2_ws/src/module2_digital_twin/launch/gazebo_test.launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    return LaunchDescription([
        # Launch Gazebo
        ExecuteProcess(
            cmd=['gazebo', 'empty_world.world', '-s', 'libgazebo_ros_factory.so'],
            output='screen'),
    ])
```

### Launch and Verify

```bash
# Launch Gazebo with ROS 2 integration
ros2 launch module2_digital_twin gazebo_test.launch.py

# In another terminal, check ROS 2 topics
ros2 topic list

# Expected output:
# /clock
# /parameter_events
# /rosout
```

**Troubleshooting**:
- If `/clock` topic is missing, Gazebo-ROS 2 bridge not loaded properly
- Check for errors: `ros2 launch <package> <launch_file> --show-args`

---

## Step 5: Install Unity Hub and Editor

### Download Unity Hub

1. Visit: https://unity.com/download
2. Download Unity Hub for Linux (or Windows/Mac)
3. Install downloaded package:

```bash
# For Ubuntu (deb package)
sudo dpkg -i unityhub_amd64.deb
sudo apt-get install -f  # Fix dependencies
```

### Install Unity Editor

1. Open Unity Hub
2. Go to **Installs** → **Install Editor**
3. Install **Unity 2021.3 LTS** or later (recommended: 2022.3 LTS)
4. Include modules: **Linux Build Support**, **Visual Studio**

### Verify Unity Installation

```bash
# Check Unity version from command line
/opt/unity/Editor/Unity -version

# Or open Unity Hub and verify installation in "Installs" tab
```

---

## Step 6: Install ROS-TCP-Connector

### Install in Unity Project

1. Create new Unity project: **File** → **New Project** → **3D Core**
2. Open **Window** → **Package Manager**
3. Click **+** → **Add package by name...**
4. Enter: `com.unity.robotics.ros-tcp-connector`
5. Click **Add**

### Alternatively, Install via Git URL

```
https://github.com/Unity-Technologies/Unity-Robotics-Hub.git?path=/main ROS-TCP-Connector
```

### Configure ROS 2 Connection

In Unity, create a script to configure ROS-TCP-Connector:

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;

public class Ros2Setup : MonoBehaviour
{
    void Start()
    {
        // Register ROS 2 connection (default: localhost, 10000)
        ROSConnection.instance.Register<RosMessageTypes>("/robot_state");
    }
}
```

---

## Step 7: Verify End-to-End Setup

### Test 1: Gazebo World Launch

```bash
# Launch Gazebo with example world
ros2 launch gazebo_ros gazebo.launch.py

# Expected: Gazebo GUI opens successfully
```

### Test 2: ROS 2 Topic Communication

```bash
# In one terminal, start a dummy publisher
ros2 topic pub /test std_msgs/String "data: 'Hello World'"

# In another terminal, echo the topic
ros2 topic echo /test

# Expected: See "Hello World" messages
```

### Test 3: Unity Build

```bash
# Open Unity Editor, create new 3D project
# Add a cube to scene: GameObject → 3D Object → Cube
# Press Play button in Editor

# Expected: Cube visible in Game view, no errors in Console
```

### Test 4: Unity-ROS 2 Connection (Optional)

```bash
# In ROS 2 terminal, start TCP endpoint
ros2 run ros_tcp_endpoint default_server_endpoint --ros-args -p ROS_IP:=127.0.0.1 -p ROS_TCP_PORT:=10000

# In Unity, add script with ROSConnection.instance.Connect()
# Press Play in Unity Editor

# Expected: Unity connects to ROS 2 (check Console for connection messages)
```

---

## Common Issues and Solutions

### Issue 1: Gazebo Won't Launch

**Symptoms**: `gazebo` command fails or window doesn't appear

**Solutions**:
```bash
# Check graphics drivers
glxinfo | grep "OpenGL renderer"

# Update graphics drivers (NVIDIA)
sudo ubuntu-drivers devices
sudo apt install nvidia-driver-535

# Try software rendering
export LIBGL_ALWAYS_SOFTWARE=1
gazebo empty_world.world
```

### Issue 2: ROS 2 Topics Not Visible

**Symptoms**: `ros2 topic list` doesn't show Gazebo topics

**Solutions**:
```bash
# Ensure Gazebo-ROS 2 bridge loaded
gazebo --verbose empty_world.world -s libgazebo_ros_factory.so

# Check if plugins exist
ls /opt/ros/foxy/lib/libgazebo_ros*.so

# Source workspace
source ~/ros2_ws/install/setup.bash
```

### Issue 3: Unity Build Fails

**Symptoms**: Build errors or missing dependencies

**Solutions**:
```bash
# Install Unity build dependencies
sudo apt install build-essential mono-devel

# In Unity Editor: Edit → Preferences → External Tools
# Set "External Script Editor" to your preferred IDE
```

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

---

## Next Steps

Once your environment is set up, proceed to:

1. **Chapter 1**: Create Gazebo worlds and configure physics
2. **Chapter 2**: Add sensor plugins to robot models
3. **Chapter 3**: Build Unity digital twin with ROS 2 synchronization

### Verification Checklist

- [ ] Gazebo launches with empty world
- [ ] ROS 2 topics appear when Gazebo is running
- [ ] Unity Editor opens and creates new project
- [ ] ROS-TCP-Connector package installs in Unity
- [ ] Test connection between Unity and ROS 2 works

### Resources for Help

- **Gazebo Forum**: https://answers.gazebosim.org/
- **ROS 2 Answers**: https://answers.ros.org/
- **Unity Robotics Hub**: https://github.com/Unity-Technologies/Unity-Robotics-Hub
- **Module 2 Code Examples**: `code-examples/module-02-digital-twin/`

---

## Environment Variables Reference

Add to `~/.bashrc` if needed:

```bash
# Gazebo model path (for custom models)
export GAZEBO_MODEL_PATH=~/ros2_ws/src/module2_digital_twin/models:$GAZEBO_MODEL_PATH

# Gazebo plugin path
export GAZEBO_PLUGIN_PATH=~/ros2_ws/install/lib:$GAZEBO_PLUGIN_PATH

# ROS 2 domain ID (if using multiple ROS 2 instances)
export ROS_DOMAIN_ID=0

# Unity ROS 2 endpoint
export ROS_IP=127.0.0.1
export ROS_TCP_PORT=10000
```

Reload shell: `source ~/.bashrc`
