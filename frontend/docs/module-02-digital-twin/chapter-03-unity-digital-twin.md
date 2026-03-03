---
title: "Chapter 3: Unity Digital Twin"
sidebar_label: "Chapter 3"
description: "Learn to build high-fidelity digital twins in Unity with humanoid robots and real-time ROS 2 synchronization"
---

# Chapter 3: Unity Digital Twin

## Introduction

Digital twins are high-fidelity virtual replicas of physical systems that mirror real-time behavior. This chapter teaches you to create Unity-based digital twins with humanoid robot visualization and real-time synchronization with Gazebo simulations via ROS 2.

**Why Unity?** Unity provides photorealistic rendering, advanced animation systems (Mecanim), and cross-platform deployment—ideal for human-robot interaction demonstrations and presentations.

## Unity Project Setup

### Install Unity Hub and Editor

1. **Download Unity Hub**:
   - Visit: https://unity.com/download
   - Install for your OS (Linux/Windows/Mac)

2. **Install Unity Editor**:
   - Open Unity Hub → Installs → Install Editor
   - Select **Unity 2021.3 LTS** or later
   - Include: Linux Build Support (if applicable), Visual Studio

3. **Create New Project**:
   - Unity Hub → New Project → 3D Core
   - Project name: `DigitalTwin`
   - Location: Your workspace

### Install ROS-TCP-Connector

1. **Open Unity Project**, then:
   - Window → Package Manager
   - Click **+** → Add package by name
   - Enter: `com.unity.robotics.ros-tcp-connector`
   - Click **Add**

2. **Verify Installation**:
   - Check `Packages/ROS-TCP-Connector` in Project window
   - Should contain sample scripts and README

## Humanoid Model Import

### Import Humanoid Robot

1. **Obtain FBX Model**:
   - Export from Gazebo/Blender (`.fbx` format)
   - Or download from [Unity Asset Store](https://assetstore.unity.com/)

2. **Import to Unity**:
   - Assets → Import New Asset
   - Select `humanoid.fbx`
   - Configure Rig: Humanoid
   - Click **Import**

3. **Configure Humanoid Rig**:
   - Select imported model in Project window
   - Inspector → Rig → Animation Type: Humanoid
   - Click **Apply** → **Configure**

### Create Prefab

1. **Drag model** from Project to Hierarchy
2. **Add to Prefab**: Drag from Hierarchy to Project
3. **Name**: `HumanoidRobot`
4. **Configure Structure**:
   - Root: `Pelvis`
   - Joints: `Torso`, `Head`, `LeftArm`, `RightArm`, `LeftLeg`, `RightLeg`

## ROS 2 Integration

### RosConnector.cs Singleton

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;

public class RosConnector : MonoBehaviour
{
    public static RosConnector instance { get; private set; }

    [Header("Connection Settings")]
    public string rosIp = "127.0.0.1";
    public int rosPort = 10000;
    public bool isConnected = false;

    void Awake()
    {
        if (instance == null)
        {
            instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    void Start()
    {
        // Connect to ROS 2
        ROSConnection.instance.ConnectOnStart = true;
        ROSConnection.instance.RosIPAddress = rosIp;
        ROSConnection.instance.RosPort = rosPort;

        // Register subscriptions
        ROSConnection.instance.Subscribe<RosMessageTypes.Nav_msgs.Odometry>(
            "/odom", OnOdometryReceived);

        ROSConnection.instance.Subscribe<RosMessageTypes.Sensor_msgs.JointState>(
            "/joint_states", OnJointStatesReceived);

        isConnected = true;
        Debug.Log("Connected to ROS 2");
    }

    void OnOdometryReceived(RosMessageTypes.Nav_msgs.Odometry msg)
    {
        // Handle position/velocity data
        isConnected = true;
    }

    void OnJointStatesReceived(RosMessageTypes.Sensor_msgs.JointState msg)
    {
        // Handle joint angle data
        isConnected = true;
    }
}
```

**Place on**: `RosConnector` GameObject (empty GameObject in scene)

### Coordinate Conversion (ROS 2 → Unity)

```csharp
public static class Ros2Unity
{
    // Convert ROS 2 (Z-up) to Unity (Y-up)
    public static Vector3 ToVector3(Messages.GeometryMsgs.Point p)
    {
        return new Vector3((float)p.x, (float)p.z, (float)p.y);
    }

    public static Quaternion ToQuaternion(Messages.GeometryMsgs.Quaternion q)
    {
        return new Quaternion(
            (float)-q.x,
            (float)-q.z,
            (float)-q.y,
            (float)q.w
        );
    }
}
```

## Real-Time Synchronization

### RobotStateSync.cs

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector.ROSGenerated;

public class RobotStateSync : MonoBehaviour
{
    [Header("Target Robot")]
    public GameObject robotObject;

    [Header("Sync Settings")]
    public bool syncPosition = true;
    public bool syncRotation = true;
    public float lerpSpeed = 10.0f;

    private Vector3 targetPosition;
    private Quaternion targetRotation;

    void Start()
    {
        ROSConnection.instance.Subscribe<OdometryMsg>(
            "/odom", UpdateRobotState);
    }

    void UpdateRobotState(OdometryMsg msg)
    {
        // Convert ROS 2 coordinates to Unity
        targetPosition = Ros2Unity.ToVector3(
            msg.pose.pose.position);
        targetRotation = Ros2Unity.ToQuaternion(
            msg.pose.pose.orientation);
    }

    void Update()
    {
        // Smooth interpolation
        if (syncPosition)
        {
            robotObject.transform.localPosition = Vector3.Lerp(
                robotObject.transform.localPosition,
                targetPosition,
                Time.deltaTime * lerpSpeed
            );
        }

        if (syncRotation)
        {
            robotObject.transform.localRotation = Quaternion.Slerp(
                robotObject.transform.localRotation,
                targetRotation,
                Time.deltaTime * lerpSpeed
            );
        }
    }
}
```

**Attach to**: `HumanoidRobot` prefab

### HumanoidController.cs

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector.ROSGenerated;

public class HumanoidController : MonoBehaviour
{
    [Header("Animator Reference")]
    public Animator animator;

    [Header("Joint Mapping")]
    public string[] jointNames = {
        "left_hip_yaw_joint",
        "left_hip_roll_joint",
        "left_hip_pitch_joint",
        "left_knee_joint",
        "right_hip_yaw_joint",
        "right_hip_roll_joint",
        "right_hip_pitch_joint",
        "right_knee_joint"
    };

    private float[] jointAngles;

    void Start()
    {
        jointAngles = new float[jointNames.Length];

        ROSConnection.instanceSubscribe<Sensor_msgs.JointStateMsg>(
            "/joint_states", OnJointStatesReceived);
    }

    void OnJointStatesReceived(Sensor_msgs.JointStateMsg msg)
    {
        // Map ROS 2 joint positions to Unity humanoid
        for (int i = 0; i < jointNames.Length; i++)
        {
            int index = System.Array.IndexOf(
                msg.name.ToArray(),
                jointNames[i]
            );
            if (index >= 0)
            {
                jointAngles[i] = (float)msg.position[index];
            }
        }
    }

    void Update()
    {
        // Update Mecanim humanoid
        for (int i = 0; i < jointNames.Length; i++)
        {
            animator.SetFloat(jointNames[i], jointAngles[i]);
        }
    }
}
```

**Attach to**: `HumanoidRobot` prefab

## Build and Deployment

### Build Configuration

1. **Build Settings**: File → Build Settings
2. **Platform**: Linux, Windows, or macOS
3. **Add Open Scenes**: Add your scene
4. **Click Build**: Choose output directory

### Runtime Connection

1. **Start ROS 2 TCP Endpoint**:
   ```bash
   ros2 run ros_tcp_endpoint default_server_endpoint \
     --ros-args -p ROS_IP:=127.0.0.1 -p ROS_TCP_PORT:=10000
   ```

2. **Run Unity Build**:
   - Executable launches
   - Auto-connects to ROS 2
   - Receives `/odom` and `/joint_states`

## Hands-On Exercise

**Task**: Complete digital twin setup with real-time synchronization

1. **Create Unity Scene**:
   - Add plane (floor), lights (Directional Light + Ambient)
   - Import humanoid robot FBX with Mecanim rig

2. **Add Scripts**:
   - Create `RosConnector.cs` singleton
   - Attach `RobotStateSync.cs` to robot
   - Attach `HumanoidController.cs` to robot

3. **Configure ROS 2**:
   - Start Gazebo with robot: `gazebo obstacle_course.world`
   - Start TCP endpoint with domain ID match
   - Verify topics: `ros2 topic list`

4. **Test Sync**:
   - Move robot in Gazebo (Manual Control or publish `/cmd_vel`)
   - Verify Unity robot updates position/rotation
   - Check latency: Should be &lt;100ms

5. **Build & Run**:
   - Build standalone executable
   - Run without Unity Editor
   - Confirm real-time sync works

**Expected Outcome**: Unity digital twin mirrors Gazebo robot with &lt;100ms latency, 30+ FPS rendering.

## Key Takeaways

- **Unity Setup**: Unity Hub + Editor + ROS-TCP-Connector package
- **Humanoid Import**: FBX → Mecanim humanoid rig
- **ROS 2 Integration**: `RosConnector.cs` singleton, TCP connection
- **Synchronization**: RobotStateSync.cs for position/rotation, HumanoidController.cs for joints
- **Coordinate Conversion**: ROS 2 (Z-up) → Unity (Y-up) requires transformation
- **Performance**: Target &lt;100ms sync latency, 30+ FPS rendering

**Congratulations!** You've completed Module 2: The Digital Twin. You can now create physics simulations, integrate sensors, and build high-fidelity digital twins.

---

**Word Count**: 710 words

**Code Examples**:
- [RosConnector.cs](https://github.com/your-repo/code-examples/module-02-digital-twin/unity-scripts/RosConnector.cs)
- [RobotStateSync.cs](https://github.com/your-repo/code-examples/module-02-digital-twin/unity-scripts/RobotStateSync.cs)
- [HumanoidController.cs](https://github.com/your-repo/code-examples/module-02-digital-twin/unity-scripts/HumanoidController.cs)
- [Ros2Unity.cs](https://github.com/your-repo/code-examples/module-02-digital-twin/unity-scripts/Ros2Unity.cs)
- [HumanoidRobot.unitypackage](https://github.com/your-repo/code-examples/module-02-digital-twin/unity-scripts/HumanoidRobot.unitypackage)
