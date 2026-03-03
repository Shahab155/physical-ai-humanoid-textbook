#!/usr/bin/env python3
"""
Humanoid Robot State Subscriber

This standalone subscriber monitors the state of a humanoid robot
and displays current joint positions.

Use Cases:
- Monitoring robot state during operation
- Logging joint positions for analysis
- Debugging robot behavior
- Verifying robot is functioning correctly

Learning Points:
- Creating a subscription-only node
- Processing JointState messages
- Extracting joint positions from messages
- Logging state information
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class StateSubscriber(Node):
    """
    Subscriber node that monitors humanoid robot joint states.

    This node subscribes to the robot's state topic and logs
    current joint positions as they're received.
    """

    def __init__(self):
        """Initialize the state subscriber node"""
        super().__init__('humanoid_state_subscriber')

        # Create subscription to robot state
        # Topic: /humanoid/state/joint_angles
        # Message type: sensor_msgs/JointState
        # Callback: self.state_callback
        # QoS: Queue size of 10
        self.subscription = self.create_subscription(
            JointState,
            '/humanoid/state/joint_angles',
            self.state_callback,
            10
        )

        # Store current state
        self.current_state = {}
        self.message_count = 0

        self.get_logger().info('State Subscriber started')
        self.get_logger().info('Listening to: /humanoid/state/joint_angles')
        self.get_logger().info('Waiting for state updates...')

    def state_callback(self, msg):
        """
        Callback function called when new robot state is received.

        This method processes incoming JointState messages and logs
        the current joint positions.

        Args:
            msg: JointState message containing robot state
        """
        # Increment message counter
        self.message_count += 1

        # Update current state
        self.current_state = dict(zip(msg.name, msg.position))

        # Log every state update
        self.get_logger().info(f'State update #{self.message_count}:')

        # Log each joint position
        for name, position in self.current_state.items():
            # Convert radians to degrees for readability
            position_deg = position * 180.0 / 3.14159

            # Determine joint type from name
            if 'pan' in name or 'yaw' in name:
                joint_type = 'Rotation'
            elif 'lift' in name or 'flex' in name or 'elbow' in name:
                joint_type = 'Flexion'
            else:
                joint_type = 'Position'

            self.get_logger().info(f'  {name:20s}: {position:7.3f} rad ({position_deg:6.1f}°) [{joint_type}]')

        # Optional: Check if positions are within safe limits
        self.check_safety_limits(msg)

    def check_safety_limits(self, msg):
        """
        Verify joint positions are within safe operating limits.

        This is a simple example - real robots would have more
        sophisticated safety checking.

        Args:
            msg: JointState message to check
        """
        safe = True

        # Example safety limits (in radians)
        safety_limits = {
            'left_shoulder_pan': (-1.57, 1.57),      # -90 to +90 degrees
            'left_shoulder_lift': (-1.0, 2.0),     # -57 to +114 degrees
            'left_elbow': (0.0, 2.5),              # 0 to +143 degrees
            'right_shoulder_pan': (-1.57, 1.57),
            'right_shoulder_lift': (-1.0, 2.0),
            'right_elbow': (0.0, 2.5),
        }

        for i, name in enumerate(msg.name):
            if name in safety_limits:
                min_limit, max_limit = safety_limits[name]
                position = msg.position[i]

                if position < min_limit or position > max_limit:
                    self.get_logger().warn(
                        f'  ⚠️  SAFETY WARNING: {name} at {position:.3f} rad '
                        f'(limit: {min_limit:.3f} to {max_limit:.3f})'
                    )
                    safe = False

        if safe and self.message_count % 10 == 0:
            # Every 10th message, confirm all is well
            self.get_logger().debug('  ✓ All joints within safe limits')


def main(args=None):
    """
    Main entry point for the state subscriber.

    Spins until interrupted, logging all state updates.
    """
    try:
        # Initialize ROS 2
        rclpy.init(args=args)
    except Exception as e:
        print(f"ERROR: ROS 2 initialization failed: {e}")
        print("Source ROS 2 with: source /opt/ros/humble/setup.bash")
        return 1

    # Create the subscriber node
    subscriber = StateSubscriber()

    try:
        # Spin the node (keep it alive and processing callbacks)
        rclpy.spin(subscriber)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        subscriber.get_logger().info('Keyboard interrupt, shutting down...')

    finally:
        # Clean up
        subscriber.get_logger().info(f'Total state updates received: {subscriber.message_count}')
        subscriber.destroy_node()
        rclpy.shutdown()
        subscriber.get_logger().info('Shutdown complete')

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
