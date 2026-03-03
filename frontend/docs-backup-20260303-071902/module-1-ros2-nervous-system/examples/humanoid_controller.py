#!/usr/bin/env python3
"""
Humanoid Robot Controller - Complete Agent with Publisher and Subscriber

This agent demonstrates closed-loop control of a humanoid robot arm.
It publishes joint angle commands and subscribes to robot state for feedback.

Features:
- Publisher for joint commands (/humanoid/command/joint_angles)
- Subscriber for robot state (/humanoid/state/joint_angles)
- Wave motion pattern for left arm
- Connection health monitoring
- Graceful error handling

Learning Points:
- Combining publisher and subscriber in one node
- Using sensor_msgs/JointState for robot control
- Implementing closed-loop control with feedback
- Handling disconnections gracefully
"""

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import JointState
import math


class HumanoidController(Node):
    """
    Complete humanoid robot controller with command publishing
    and state subscription for closed-loop control.
    """

    def __init__(self):
        """Initialize the humanoid controller node"""
        super().__init__('humanoid_controller')

        # Initialize connection state
        self.robot_connected = False
        self.last_state_time = None

        # Create publisher for joint commands
        # Topic: /humanoid/command/joint_angles
        # Message: sensor_msgs/JointState
        # QoS: Queue size of 10
        self.command_publisher = self.create_publisher(
            JointState,
            '/humanoid/command/joint_angles',
            10
        )

        # Create subscriber for robot state feedback
        # Topic: /humanoid/state/joint_angles
        # Callback: self.state_callback
        # QoS: Queue size of 10
        self.state_subscriber = self.create_subscription(
            JointState,
            '/humanoid/state/joint_angles',
            self.state_callback,
            10
        )

        # Create timer for publishing commands (10 Hz = 0.1 second interval)
        self.command_timer = self.create_timer(0.1, self.publish_commands)

        # Create timer for monitoring connection health (1 Hz)
        self.watchdog_timer = self.create_timer(1.0, self.check_connection)

        # Wave motion parameters
        self.wave_phase = 0.0
        self.wave_amplitude_shoulder = 0.3  # Radians
        self.wave_amplitude_elbow = 0.5  # Radians

        # Joint names for left arm
        self.joint_names = [
            'left_shoulder_pan',    # Horizontal rotation
            'left_shoulder_lift',   # Vertical movement
            'left_elbow',           # Elbow flexion
        ]

        # Initial joint positions (neutral stance)
        self.neutral_positions = [0.0, 0.5, 1.2]

        # Current joint state (updated by subscriber)
        self.current_positions = {}

        self.get_logger().info('Humanoid Controller initialized')
        self.get_logger().info(f'Publishing to: /humanoid/command/joint_angles')
        self.get_logger().info(f'Subscribing to: /humanoid/state/joint_angles')
        self.get_logger().info('Waiting for robot state...')

    def publish_commands(self, timer=None):
        """
        Publish joint angle commands to the robot.

        This method is called every 0.1 seconds by the timer.
        It generates a wave motion pattern for the left arm.
        """
        # Only publish if robot is connected
        if not self.robot_connected:
            self.get_logger().warn('Not publishing: robot not connected')
            return

        # Create joint state message
        msg = JointState()

        # Set joint names
        msg.name = self.joint_names

        # Calculate wave motion using sine function
        # Wave phase increments each time this is called
        self.wave_phase += 0.2

        # Calculate joint positions for wave motion
        # Shoulder pan: stationary (0 radians)
        # Shoulder lift: wave up and down
        # Elbow: bend and unbend
        msg.position = [
            0.0,  # Shoulder pan - stationary
            0.5 + self.wave_amplitude_shoulder * math.sin(self.wave_phase),  # Shoulder lift
            1.2 + self.wave_amplitude_elbow * math.sin(self.wave_phase)  # Elbow
        ]

        # Initialize velocity and effort (optional, set to 0)
        msg.velocity = [0.0] * len(self.joint_names)
        msg.effort = [0.0] * len(self.joint_names)

        # Publish the command
        self.command_publisher.publish(msg)

        # Log command (throttled to avoid spam)
        if int(self.wave_phase * 10) % 5 == 0:  # Log every 5th iteration
            self.get_logger().info(
                f'Published: [{msg.position[0]:.2f}, '
                f'{msg.position[1]:.2f}, {msg.position[2]:.2f}]'
            )

    def state_callback(self, msg):
        """
        Callback function called when robot publishes state.

        Updates current joint positions and marks robot as connected.

        Args:
            msg: JointState message containing current joint positions
        """
        try:
            # Update last seen time
            self.last_state_time = self.get_clock().now()

            # Mark robot as connected
            if not self.robot_connected:
                self.robot_connected = True
                self.get_logger().info('✓ Robot connected!')

            # Extract and store current positions
            self.current_positions = dict(zip(msg.name, msg.position))

            # Log state (throttled)
            if 'left_elbow' in self.current_positions:
                elbow_pos = self.current_positions['left_elbow']
                if int(self.wave_phase * 10) % 10 == 0:  # Log every 10th iteration
                    self.get_logger().info(f'Robot elbow position: {elbow_pos:.3f} rad')

        except (IndexError, KeyError, AttributeError) as e:
            # Handle errors gracefully without crashing
            self.get_logger().error(f'Error in state_callback: {e}')

    def check_connection(self, timer=None):
        """
        Monitor connection health using watchdog timer.

        If no state received for 2 seconds, mark robot as disconnected.
        This handles cases where simulation crashes or robot goes offline.
        """
        if self.last_state_time is None:
            # Haven't received state yet
            self.get_logger().warn('Waiting for robot state...')
            return

        # Calculate time since last state update
        time_since_update = (
            self.get_clock().now() - self.last_state_time
        ).nanoseconds / 1e9  # Convert nanoseconds to seconds

        if time_since_update > 2.0:
            # No update for 2 seconds - robot likely disconnected
            if self.robot_connected:
                self.robot_connected = False
                self.get_logger().warn('⚠️  Robot connection lost!')
                self.get_logger().warn('Stopped publishing commands')
        elif time_since_update > 1.0:
            # Warning threshold
            self.get_logger().debug(f'State update delay: {time_since_update:.1f}s')


def main(args=None):
    """
    Main entry point for the humanoid controller.

    Handles ROS 2 initialization, creates node, spins until shutdown,
    and ensures clean shutdown.
    """
    try:
        # Initialize ROS 2 communications
        rclpy.init(args=args)
    except Exception as e:
        print(f"ERROR: ROS 2 initialization failed: {e}")
        print("Make sure you've sourced the ROS 2 setup:")
        print("  source /opt/ros/humble/setup.bash")
        return 1

    # Create the controller node
    controller = HumanoidController()

    # Create multi-threaded executor for better concurrent callback handling
    executor = MultiThreadedExecutor()

    try:
        # Spin the node (keep it alive and processing callbacks)
        # This will block until the node is shut down
        rclpy.spin(controller, executor=executor)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        controller.get_logger().info('Keyboard interrupt, shutting down...')

    finally:
        # Clean up resources
        controller.get_logger().info('Shutting down humanoid controller...')
        controller.destroy_node()
        rclpy.shutdown()
        controller.get_logger().info('Shutdown complete')

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
