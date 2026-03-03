using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes;

/// <summary>
/// ROS 2 Connection Singleton
/// Manages TCP connection to ROS 2 and handles message subscriptions
/// Attach to a persistent GameObject in the scene
/// </summary>
public class RosConnector : MonoBehaviour
{
    public static RosConnector instance { get; private set; }

    [Header("Connection Settings")]
    [Tooltip("ROS 2 TCP server IP address (use 127.0.0.1 for local)")]
    public string rosIp = "127.0.0.1";

    [Tooltip("ROS 2 TCP server port (default: 10000)")]
    public int rosPort = 10000;

    [Header("Connection Status")]
    [Tooltip("Is currently connected to ROS 2")]
    public bool isConnected = false;

    [Tooltip("Connection status display (optional UI)")]
    public UnityEngine.UI.Text statusText;

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
        // Configure ROS 2 TCP connection
        ROSConnection.instance.ConnectOnStart = true;
        ROSConnection.instance.RosIPAddress = rosIp;
        ROSConnection.instance.RosPort = rosPort;

        // Register subscriptions for robot state data
        // Odometry: position and velocity
        ROSConnection.instance.Subscribe<Nav_Msgs.Odometry>(
            "/odom",
            OnOdometryReceived
        );

        // Joint states: humanoid joint angles
        ROSConnection.instance.Subscribe<Sensor_Msgs.JointState>(
            "/joint_states",
            OnJointStatesReceived
        );

        isConnected = true;
        Debug.Log("[RosConnector] Connected to ROS 2");
    }

    void Update()
    {
        // Update status display (if assigned)
        if (statusText != null)
        {
            statusText.text = isConnected ? "✓ Connected to ROS 2" : "✗ Disconnected";
            statusText.color = isConnected ? Color.green : Color.red;
        }
    }

    /// <summary>
    /// Callback for odometry messages (robot position/velocity)
    /// </summary>
    private void OnOdometryReceived(Nav_Msgs.Odometry msg)
    {
        isConnected = true;
        // Odometry data is handled by RobotStateSync component
    }

    /// <summary>
    /// Callback for joint state messages (humanoid joint angles)
    /// </summary>
    private void OnJointStatesReceived(Sensor_Msgs.JointState msg)
    {
        isConnected = true;
        // Joint states are handled by HumanoidController component
    }

    void OnApplicationQuit()
    {
        isConnected = false;
        Debug.Log("[RosConnector] Disconnected from ROS 2");
    }

    /// <summary>
    /// Manually reconnect to ROS 2 (call from UI button or on connection loss)
    /// </summary>
    public void Reconnect()
    {
        ROSConnection.instance.Connect();
        Debug.Log("[RosConnector] Reconnecting to ROS 2...");
    }

    /// <summary>
    /// Disconnect from ROS 2
    /// </summary>
    public void Disconnect()
    {
        ROSConnection.instance.Disconnect();
        isConnected = false;
        Debug.Log("[RosConnector] Disconnected from ROS 2");
    }
}