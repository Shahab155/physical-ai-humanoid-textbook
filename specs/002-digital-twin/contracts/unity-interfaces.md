# Unity Interfaces: Module 2 - The Digital Twin

**Feature**: 002-digital-twin
**Date**: 2026-03-03
**Phase**: Phase 1 - Design & Contracts

## Overview

This document specifies the Unity C# interfaces and component structures used for ROS 2 integration and digital twin visualization in Module 2.

---

## Core Unity Components

### 1. ROSConnector Singleton

**Purpose**: Manages TCP connection to ROS 2 and handles message serialization.

**Script Location**: `Scripts/RosConnector.cs`

```csharp
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using Unity.Robotics.ROSTCPConnector.ROSGenerated;

public class RosConnector : MonoBehaviour
{
    public static RosConnector instance { get; private set; }

    [Header("Connection Settings")]
    public string rosIp = "127.0.0.1";
    public int rosPort = 10000;

    [Header("Connection Status")]
    public bool isConnected = false;

    void Awake()
    {
        // Singleton pattern
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

        // Register message subscriptions
        ROSConnection.instance.Subscribe<OdometryMsg>("/odom", OnOdometryReceived);
        ROSConnection.instance.Subscribe<JointStateMsg>("/joint_states", OnJointStatesReceived);
    }

    void OnOdometryReceived(OdometryMsg msg)
    {
        // Handle robot position/velocity update
        isConnected = true;
    }

    void OnJointStatesReceived(JointStateMsg sensor_msgs)
    {
        // Handle joint angle updates for humanoid
        isConnected = true;
    }
}
```

**Configuration**:
- Attach to **GameObject**: `RosConnector` (in every Unity scene)
- **Inspector Settings**:
  - ROS IP: `127.0.0.1` (for local ROS 2)
  - ROS Port: `10000` (default ROS-TCP-Endpoint)

---

### 2. RobotStateSync Component

**Purpose**: Synchronizes Unity GameObject transform with ROS 2 odometry data.

**Script Location**: `Scripts/RobotStateSync.cs`

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
        // Register subscriber
        ROSConnection.instance.Subscribe<OdometryMsg>("/odom", UpdateRobotState);
    }

    void UpdateRobotState(OdometryMsg msg)
    {
        // Convert ROS 2 coordinates (Right-Handed, Z-up) to Unity (Left-Handed, Y-up)
        targetPosition = Ros2Unity.ToVector3(msg.pose.pose.position);
        targetRotation = Ros2Unity.ToQuaternion(msg.pose.pose.orientation);
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

**Helper: Coordinate Conversion**

```csharp
public static class Ros2Unity
{
    // ROS 2 (Z-up) → Unity (Y-up)
    public static Vector3 ToVector3(Unity.Robotics.ROSTCPConnector.ROSGenerated.geometry_msgs.Point p)
    {
        return new Vector3((float)p.x, (float)p.z, (float)p.y);
    }

    public static Quaternion ToQuaternion(Unity.Robotics.ROSTCPConnector.ROSGenerated.geometry_msgs.Quaternion q)
    {
        return new Quaternion((float)-q.x, (float)-q.z, (float)-q.y, (float)q.w);
    }
}
```

**Configuration**:
- Attach to robot root GameObject (e.g., `HumanoidRobot`)
- **Robot Object**: Drag the humanoid robot GameObject here
- **Lerp Speed**: Adjust for smoothness (10-30 recommended)

---

### 3. HumanoidController Component

**Purpose**: Controls humanoid animation based on joint states from ROS 2.

**Script Location**: `Scripts/HumanoidController.cs`

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
        // Initialize joint array
        jointAngles = new float[jointNames.Length];

        // Subscribe to joint states
        ROSConnection.instance.Subscribe<sensor_msgs.JointStateMsg>(
            "/joint_states",
            OnJointStatesReceived
        );
    }

    void OnJointStatesReceived(sensor_msgs.JointStateMsg msg)
    {
        // Map ROS 2 joint positions to Unity humanoid
        for (int i = 0; i < jointNames.Length; i++)
        {
            int index = System.Array.IndexOf(msg.name, jointNames[i]);
            if (index >= 0)
            {
                jointAngles[i] = (float)msg.position[index];
            }
        }
    }

    void Update()
    {
        // Update animator parameters
        for (int i = 0; i < jointNames.Length; i++)
        {
            animator.SetFloat(jointNames[i], jointAngles[i]);
        }
    }
}
```

**Configuration**:
- Attach to humanoid robot GameObject
- **Animator**: Drag the Animator component (with Mecanim humanoid rig)
- **Joint Names**: Match ROS 2 joint state names to Unity humanoid bones

---

## Unity Scene Structure

### DigitalTwinScene Hierarchy

```
DigitalTwinScene
├── Lights
│   ├── Directional Light (sun)
│   └── Ambient Light
├── Floor (Plane)
├── HumanoidRobot
│   ├── Pelvis (root)
│   │   ├── Torso
│   │   │   ├── Chest
│   │   │   ├── Head
│   │   │   ├── LeftArm
│   │   │   │   ├── LeftUpperArm
│   │   │   │   └── LeftForeArm
│   │   │   └── RightArm
│   │   │       ├── RightUpperArm
│   │   │       └── RightForeArm
│   │   └── Legs...
│   ├── Animator (Component)
│   ├── HumanoidController (Script)
│   └── RobotStateSync (Script)
├── RosConnector (Script)
└── EventSystem (UI)
```

---

## Message Type Mappings

### ROS 2 → Unity C# Messages

**Odometry → Pose Update**

```csharp
// ROS 2: nav_msgs/Odometry
public class OdometryMsg
{
    public HeaderMsg header;
    public string child_frame_id;
    public PoseWithCovarianceMsg pose;
    public TwistWithCovarianceMsg twist;
}

// Unity: Unity.Robotics.ROSTCPConnector.ROSGenerated.nav_msgs.OdometryMsg
// Auto-generated by ROS-TCP-Connector
```

**JointState → Animator Parameters**

```csharp
// ROS 2: sensor_msgs/JointState
public class JointStateMsg
{
    public HeaderMsg header;
    public string[] name;        // Joint names
    public float[] position;     // Joint positions (rad)
    public float[] velocity;     // Joint velocities (rad/s)
    public float[] effort;       # Joint efforts (Nm)
}

// Unity: Map to Mecanim humanoid bones
```

---

## Prefab Specifications

### HumanoidRobot Prefab

**Components**:
1. **Transform**: Position (0, 0, 0), Rotation (0, 0, 0), Scale (1, 1, 1)
2. **Animator**: Controller = `HumanoidController`
3. **Capsule Collider**: Height = 1.7, Radius = 0.3 (for physics)
4. **Rigidbody**: Mass = 60, Use Gravity = true
5. **Scripts**:
   - `HumanoidController.cs`
   - `RobotStateSync.cs` (on root)

**Model Import Settings**:
- **Rig**: Humanoid (Mecanim)
- **Animation Type**: Humanoid
- **Avatar Created**: From model
- **Import Materials**: Yes (standard shader)

---

## Performance Requirements

### Frame Rate Targets

- **Unity Rendering**: 60 FPS minimum
- **Sync Update Rate**: 30 Hz (every ~33ms)
- **Network Latency**: <100ms for round-trip

### Optimization Guidelines

```csharp
// Use object pooling for frequent messages
public class MessagePool
{
    private Stack<OdometryMsg> pool = new Stack<OdometryMsg>();

    public OdometryMsg Get()
    {
        return pool.Count > 0 ? pool.Pop() : new OdometryMsg();
    }

    public void Return(OdometryMsg msg)
    {
        pool.Push(msg);
    }
}

// Batch joint updates
void Update()
{
    // Update all joints once per frame (not per message)
    animator.SetFloat("left_hip_yaw", jointAngles[0]);
    animator.SetFloat("left_hip_roll", jointAngles[1]);
    // ... etc
}
```

---

## Error Handling

### Connection Errors

```csharp
void OnConnectionError(string error)
{
    Debug.LogWarning($"ROS 2 Connection Error: {error}");
    // Attempt reconnection after 5 seconds
    Invoke(nameof(Reconnect), 5.0f);
}

void Reconnect()
{
    ROSConnection.instance.ConnectOnStart = true;
    ROSConnection.instance.RosIPAddress = rosIp;
    ROSConnection.instance.RosPort = rosPort;
}
```

### Message Validation

```csharp
bool ValidateOdometry(OdometryMsg msg)
{
    // Check for NaN in position
    if (float.IsNaN(msg.pose.pose.position.x)) return false;

    // Check for reasonable values (within 100m of origin)
    if (Mathf.Abs((float)msg.pose.pose.position.x) > 100.0f) return false;

    // Check quaternion is normalized
    float mag = Mathf.Sqrt(
        (float)(msg.pose.pose.orientation.x * msg.pose.pose.orientation.x) +
        (float)(msg.pose.pose.orientation.y * msg.pose.pose.orientation.y) +
        (float)(msg.pose.pose.orientation.z * msg.pose.pose.orientation.z) +
        (float)(msg.pose.pose.orientation.w * msg.pose.pose.orientation.w)
    );
    if (Mathf.Abs(mag - 1.0f) > 0.1f) return false;

    return true;
}
```

---

## Build Settings

### Platform-Specific Configuration

**Linux Build** (for Ubuntu compatibility):

1. **File** → **Build Settings** → **Linux**
2. **Architecture**: x86_64
3. **Backend**: Mono (IL2CP for release builds)
4. **API Compatibility Level**: .NET Standard 2.1

**Include in Build**:
- `RosConnector.cs`
- `RobotStateSync.cs`
- `HumanoidController.cs`
- ROS-TCP-Connector package
- Humanoid model FBX files
- Animator Controller

---

## Testing Interface

### Test Scene Setup

```csharp
// Editor-only test script
#if UNITY_EDITOR
[InitializeOnLoad]
public class Ros2ConnectionTest
{
    static Ros2ConnectionTest()
    {
        // Test connection on editor load
        EditorApplication.delayCall += () =>
        {
            Debug.Log("Testing ROS 2 connection...");
            ROSConnection.instance.ConnectOnStart = true;
            // Add test assertions here
        };
    }
}
#endif
```

### Runtime Validation

```csharp
void ValidateSetup()
{
    // Check RosConnector exists
    if (FindObjectOfType<RosConnector>() == null)
    {
        Debug.LogError("RosConnector not found in scene!");
    }

    // Check Animator exists on humanoid
    if (humanoidAnimator == null)
    {
        Debug.LogError("Animator reference missing!");
    }
}
```

---

## Summary

Unity integration requires three core scripts:

1. **RosConnector.cs**: Manages ROS 2 TCP connection
2. **RobotStateSync.cs**: Syncs robot position/rotation from `/odom`
3. **HumanoidController.cs**: Maps `/joint_states` to Mecanim animation

All scripts use ROS-TCP-Connector with standard message types. Scene hierarchy follows Mecanim humanoid rig conventions.
