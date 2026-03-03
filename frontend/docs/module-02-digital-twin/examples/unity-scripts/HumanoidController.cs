using UnityEngine;
using Unity.Robotics.ROSTCPConnector.ROSGenerated;
using Sensor_Msgs = RosMessageTypes.Sensor_msgs;

/// <summary>
/// Humanoid Animation Controller
/// Maps ROS 2 joint states to Unity Mecanim humanoid animator
/// Attach to the humanoid robot GameObject
/// </summary>
public class HumanoidController : MonoBehaviour
{
    [Header("Animator Reference")]
    [Tooltip("Mecanim Animator component on humanoid robot")]
    public Animator animator;

    [Header("Joint Mapping")]
    [Tooltip("ROS 2 joint names to track (must match URDF)")]
    public string[] jointNames = {
        "left_hip_yaw_joint",
        "left_hip_roll_joint",
        "left_hip_pitch_joint",
        "left_knee_joint",
        "right_hip_yaw_joint",
        "right_hip_roll_joint",
        "right_hip_pitch_joint",
        "right_knee_joint",
        "torso_joint",
        "head_joint",
        "left_shoulder_pitch_joint",
        "left_elbow_joint",
        "right_shoulder_pitch_joint",
        "right_elbow_joint"
    };

    [Header("Animation Settings")]
    [Tooltip("Apply joint updates to Mecanim humanoid")]
    public bool updateAnimator = true;

    [Tooltip("Smooth joint transitions")]
    public bool smoothJoints = true;

    [Range(0.1f, 10.0f)]
    public float lerpSpeed = 5.0f;

    [Header("Debug")]
    public bool debugMode = false;

    // Current joint angles (from ROS 2)
    private float[] jointAngles;

    // Target joint angles (after smoothing)
    private float[] targetJointAngles;

    // Previous joint states for velocity calculation
    private float[] previousJointAngles;
    private bool[] jointInitialized;

    private int messageCount = 0;

    void Start()
    {
        if (animator == null)
        {
            Debug.LogError("[HumanoidController] Animator not assigned!");
            return;
        }

        // Initialize arrays
        int jointCount = jointNames.Length;
        jointAngles = new float[jointCount];
        targetJointAngles = new float[jointCount];
        previousJointAngles = new float[jointCount];
        jointInitialized = new bool[jointCount];

        // Subscribe to joint states topic
        ROSConnection.instance.Subscribe<Sensor_Msgs.JointState>(
            "/joint_states",
            OnJointStatesReceived
        );

        Debug.Log($"[HumanoidController] Tracking {jointCount} joints");
    }

    /// <summary>
    /// Callback for joint state messages from ROS 2
    /// </summary>
    void OnJointStatesReceived(Sensor_Msgs.JointState msg)
    {
        // Extract joint names and positions from ROS 2 message
        string[] nameArray = msg.name.ToArray();
        double[] positionArray = msg.position.ToArray();

        // Map to our joint tracking arrays
        for (int i = 0; i < jointNames.Length; i++)
        {
            int index = System.Array.IndexOf(nameArray, jointNames[i]);
            if (index >= 0 && index < positionArray.Length)
            {
                jointAngles[i] = (float)positionArray[index];
                jointInitialized[i] = true;
            }
        }

        messageCount++;
    }

    void Update()
    {
        if (!updateAnimator) return;

        // Update Mecanim humanoid
        for (int i = 0; i < jointNames.Length; i++)
        {
            // Skip uninitialized joints
            if (!jointInitialized[i]) continue;

            // Smooth joint transitions
            if (smoothJoints)
            {
                targetJointAngles[i] = Mathf.Lerp(
                    targetJointAngles[i],
                    jointAngles[i],
                    Time.deltaTime * lerpSpeed
                );
            }
            else
            {
                targetJointAngles[i] = jointAngles[i];
            }

            // Set Mecanim parameter
            // Note: Joint names must match Mecanim humanoid rig
            animator.SetFloat(jointNames[i], targetJointAngles[i]);
        }

        // Debug output
        if (debugMode && messageCount > 0 && messageCount % 60 == 0)
        {
            Debug.Log($"[HumanoidController] Joint message {messageCount}");
            for (int i = 0; i < Mathf.Min(5, jointNames.Length); i++)
            {
                Debug.Log($"  {jointNames[i]}: {jointAngles[i]:.3f} rad");
            }
        }
    }

    /// <summary>
    /// Get current joint angle for a specific joint
    /// </summary>
    public float GetJointAngle(string jointName)
    {
        int index = System.Array.IndexOf(jointNames, jointName);
        if (index >= 0)
        {
            return jointAngles[index];
        }
        Debug.LogWarning($"[HumanoidController] Joint '{jointName}' not found");
        return 0f;
    }

    /// <summary>
    /// Set joint angle manually (for testing or manual control)
    /// </summary>
    public void SetJointAngle(string jointName, float angle)
    {
        int index = System.Array.IndexOf(jointNames, jointName);
        if (index >= 0)
        {
            jointAngles[index] = angle;
            targetJointAngles[index] = angle;
            animator.SetFloat(jointName, angle);
        }
    }

    /// <summary>
    /// Reset all joints to zero position
    /// </summary>
    public void ResetJoints()
    {
        for (int i = 0; i < jointAngles.Length; i++)
        {
            jointAngles[i] = 0f;
            targetJointAngles[i] = 0f;
            previousJointAngles[i] = 0f;
            if (animator != null)
            {
                animator.SetFloat(jointNames[i], 0f);
            }
        }
        Debug.Log("[HumanoidController] All joints reset to zero");
    }
}