using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using Unity.Robotics.ROSTCPConnector.ROSGenerated;
using RosMessageTypes.Nav_Msgs;
using Messages.Geometry;

/// <summary>
/// Robot State Synchronization
/// Syncs Unity GameObject transform from ROS 2 /odom messages
/// Attach to the root GameObject of the humanoid robot
/// </summary>
public class RobotStateSync : MonoBehaviour
{
    [Header("Target Robot")]
    [Tooltip("Root GameObject of the humanoid robot")]
    public GameObject robotObject;

    [Header("Sync Settings")]
    [Tooltip("Sync robot position (x, y, z)")]
    public bool syncPosition = true;

    [Tooltip("Sync robot orientation (quaternion)")]
    public bool syncRotation = true;

    [Tooltip("Interpolation speed for smooth updates")]
    [Range(1.0f, 50.0f)]
    public float lerpSpeed = 20.0f;

    [Header("Debug")]
    [Tooltip("Show synchronization stats in console")]
    public bool debugMode = false;

    private Vector3 targetPosition = Vector3.zero;
    private Quaternion targetRotation = Quaternion.identity;
    private Vector3 currentPosition = Vector3.zero;
    private Quaternion currentRotation = Quaternion.identity;

    private int messageCount = 0;
    private float lastUpdateTime = 0f;

    void Start()
    {
        if (robotObject == null)
        {
            Debug.LogError("[RobotStateSync] robotObject not assigned!");
            return;
        }

        // Initialize from current transform
        currentPosition = robotObject.transform.localPosition;
        currentRotation = robotObject.transform.localRotation;

        // Subscribe to odometry topic
        ROSConnection.instance.Subscribe<OdometryMsg>(
            "/odom",
            UpdateRobotState
        );

        Debug.Log("[RobotStateSync] Subscribed to /odom topic");
    }

    /// <summary>
    /// Callback for odometry messages
    /// </summary>
    void UpdateRobotState(OdometryMsg msg)
    {
        // Convert ROS 2 coordinates (Z-up, Right-Handed) to Unity (Y-up, Left-Handed)
        // Position: (x, y, z) in ROS 2 → (x, z, y) in Unity
        // Quaternion: requires axis inversions for handedness change
        targetPosition = ConvertPosition(msg.pose.pose.position);
        targetRotation = ConvertQuaternion(msg.pose.pose.orientation);

        messageCount++;
        lastUpdateTime = Time.realtimeSinceStartup;
    }

    void Update()
    {
        if (robotObject == null) return;

        // Smooth interpolation to target position/rotation
        if (syncPosition)
        {
            currentPosition = Vector3.Lerp(
                currentPosition,
                targetPosition,
                Time.deltaTime * lerpSpeed
            );
            robotObject.transform.localPosition = currentPosition;
        }

        if (syncRotation)
        {
            currentRotation = Quaternion.Slerp(
                currentRotation,
                targetRotation,
                Time.deltaTime * lerpSpeed
            );
            robotObject.transform.localRotation = currentRotation;
        }

        // Debug output
        if (debugMode && messageCount > 0 && messageCount % 60 == 0)
        {
            Debug.Log($"[RobotStateSync] Messages: {messageCount}, " +
                     $"Pos: {currentPosition}, " +
                     $"Rot: {currentRotation.eulerAngles}");
        }
    }

    /// <summary>
    /// Convert ROS 2 Point to Unity Vector3
    /// ROS 2: Z-up, Unity: Y-up
    /// </summary>
    private Vector3 ConvertPosition(Point point)
    {
        return new Vector3(
            (float)point.x,
            (float)point.z,  // ROS 2 Z → Unity Y
            (float)point.y   // ROS 2 Y → Unity Z
        );
    }

    /// <summary>
    /// Convert ROS 2 Quaternion to Unity Quaternion
    /// ROS 2: Right-Handed, Unity: Left-Handed (inverts X and Z)
    /// </summary>
    private Quaternion ConvertQuaternion(Messages.GeometryMsgs.Quaternion q)
    {
        return new Quaternion(
            (float)-q.x,  // Invert X
            (float)-q.z,  // Invert Z (→ Y)
            (float)-q.y,  // Invert Y (→ Z)
            (float)q.w
        );
    }

    /// <summary>
    /// Reset robot to origin (for testing)
    /// </summary>
    public void ResetPosition()
    {
        targetPosition = Vector3.zero;
        targetRotation = Quaternion.identity;
        currentPosition = Vector3.zero;
        currentRotation = Quaternion.identity;
        robotObject.transform.localPosition = currentPosition;
        robotObject.transform.localRotation = currentRotation;
    }
}