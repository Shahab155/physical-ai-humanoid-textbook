using UnityEngine;
using Messages.Geometry;

/// <summary>
/// ROS 2 to Unity Coordinate Conversion Helper
/// Handles coordinate system transformations between ROS 2 (Z-up, Right-Handed) and Unity (Y-up, Left-Handed)
/// </summary>
public static class Ros2Unity
{
    /// <summary>
    /// Convert ROS 2 Point to Unity Vector3
    /// ROS 2 Coordinate System: Z-up, Right-Handed
    /// Unity Coordinate System: Y-up, Left-Handed
    ///
    /// Axis Mapping:
    /// - ROS 2 +X → Unity +X (same)
    /// - ROS 2 +Y → Unity +Z (swap)
    /// - ROS 2 +Z → Unity +Y (swap)
    /// </summary>
    /// <param name="point">ROS 2 Point message</param>
    /// <returns>Unity Vector3</returns>
    public static Vector3 ToVector3(Point point)
    {
        if (point == null)
        {
            Debug.LogWarning("[Ros2Unity] Null point, returning zero vector");
            return Vector3.zero;
        }

        return new Vector3(
            (float)point.x,
            (float)point.z,  // ROS 2 Z → Unity Y (up)
            (float)point.y   // ROS 2 Y → Unity Z (forward)
        );
    }

    /// <summary>
    /// Convert ROS 2 Point to Unity Vector3 (float coordinates)
    /// </summary>
    public static Vector3 ToVector3(double x, double y, double z)
    {
        return new Vector3(
            (float)x,
            (float)z,  // Z → Y
            (float)y   // Y → Z
        );
    }

    /// <summary>
    /// Convert Unity Vector3 to ROS 2 Point (inverse transformation)
    /// </summary>
    public static Point ToRosPoint(Vector3 unityVector)
    {
        Point point = new Point();
        point.x = unityVector.x;
        point.y = unityVector.z;  // Unity Z → ROS 2 Y
        point.z = unityVector.y;  // Unity Y → ROS 2 Z
        return point;
    }

    /// <summary>
    /// Convert ROS 2 Quaternion to Unity Quaternion
    /// ROS 2: Right-Handed coordinate system
    /// Unity: Left-Handed coordinate system (inverts X and Z axes)
    ///
    /// Quaternion Conversion: q_unity = (-q_x, -q_z, -q_y, q_w)
    /// This flips the handedness of the coordinate system
    /// </summary>
    /// <param name="q">ROS 2 Quaternion message</param>
    /// <returns>Unity Quaternion</returns>
    public static Quaternion ToQuaternion(Messages.GeometryMsgs.Quaternion q)
    {
        if (q == null)
        {
            Debug.LogWarning("[Ros2Unity] Null quaternion, returning identity");
            return Quaternion.identity;
        }

        return new Quaternion(
            (float)-q.x,  // Invert X
            (float)-q.z,  // Invert Z (→ Y)
            (float)-q.y,  // Invert Y (→ Z)
            (float)q.w
        );
    }

    /// <summary>
    /// Convert ROS 2 Quaternion to Unity Quaternion (float components)
    /// </summary>
    public static Quaternion ToQuaternion(double x, double y, double z, double w)
    {
        return new Quaternion(
            (float)-x,
            (float)-z,
            (float)-y,
            (float)w
        );
    }

    /// <summary>
    /// Convert Unity Quaternion to ROS 2 Quaternion (inverse transformation)
    /// </summary>
    public static Messages.GeometryMsgs.Quaternion ToRosQuaternion(Quaternion unityQuat)
    {
        Messages.GeometryMsgs.Quaternion q = new Messages.GeometryMsgs.Quaternion();
        q.x = -unityQuat.x;  // Invert back
        q.z = -unityQuat.y;  // Unity Y → ROS 2 Z
        q.y = -unityQuat.z;  // Unity Z → ROS 2 Y
        q.w = unityQuat.w;
        return q;
    }

    /// <summary>
    /// Convert ROS 2 Pose to Unity Transform
    /// </summary>
    public static Transform ToTransform(Pose pose)
    {
        Transform t = new Transform();
        t.position = ToVector3(pose.position);
        t.rotation = ToQuaternion(pose.orientation);
        return t;
    }

    /// <summary>
    /// Create a look-at rotation from a position and target
    /// Useful for cameras or directed sensors
    /// </summary>
    public static Quaternion LookRotation(Vector3 position, Vector3 target, Vector3 up)
    {
        Vector3 forward = (target - position).normalized;
        Quaternion rotation = Quaternion.LookRotation(forward, up);
        return rotation;
    }

    /// <summary>
    /// Debug print coordinate conversion info
    /// </summary>
    public static void DebugConversion(string label, Point rosPoint, Quaternion rosQuat)
    {
        Vector3 unityPos = ToVector3(rosPoint);
        Quaternion unityRot = ToQuaternion(rosQuat);

        Debug.Log($"[Ros2Unity] {label}:");
        Debug.Log($"  ROS 2 Position: ({rosPoint.x:F3}, {rosPoint.y:F3}, {rosPoint.z:F3})");
        Debug.Log($"  Unity Position: {unityPos}");
        Debug.Log($"  ROS 2 Quaternion: ({rosQuat.x:F3}, {rosQuat.y:F3}, {rosQuat.z:F3}, {rosQuat.w:F3})");
        Debug.Log($"  Unity Quaternion: {unityRot.eulerAngles}");
    }
}