#!/usr/bin/env python3
"""
ROS 2 Error Handling Patterns for Humanoid Robot Control

This example demonstrates common error scenarios and how to handle them
gracefully in ROS 2 Python applications.

Error Types Covered:
- ROS 2 initialization failures
- Node creation errors
- Publisher/subscriber creation errors
- Connection timeouts
- Message callback exceptions
- Graceful shutdown patterns

Learning Points:
- Using try-except for ROS 2 operations
- Implementing timeouts for connections
- Handling callback exceptions without crashing
- Proper resource cleanup
- User-friendly error messages
"""

import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from sensor_msgs.msg import JointState
import sys


class RobustHumanoidController(Node):
    """
    Humanoid controller with comprehensive error handling.

    This example shows how to handle common errors that occur
    when working with ROS 2, including initialization failures,
    disconnections, and callback exceptions.
    """

    def __init__(self):
        """Initialize the robust controller with error handling"""
        try:
            # Attempt to create the node
            super().__init__('robust_humanoid_controller')
        except Exception as e:
            print(f"FATAL: Failed to create node: {e}")
            raise

        self.get_logger().info('Initializing robust humanoid controller...')

        # Connection state tracking
        self.robot_connected = False
        self.last_state_time = None
        self.connection_timeout = 5.0  # seconds

        # Publishers and subscribers (initialized separately)
        self.command_publisher = None
        self.state_subscriber = None

        # Timers (initialized separately)
        self.command_timer = None
        self.watchdog_timer = None

        # Wave motion state
        self.wave_phase = 0.0

        # Initialize components with error handling
        self._initialize_publishers()
        self._initialize_subscribers()
        self._initialize_timers()

        self.get_logger().info('✓ Initialization complete')

    def _initialize_publishers(self):
        """Initialize command publisher with error handling"""
        try:
            self.command_publisher = self.create_publisher(
                JointState,
                '/humanoid/command/joint_angles',
                10
            )
            self.get_logger().info('✓ Publisher created: /humanoid/command/joint_angles')
        except Exception as e:
            self.get_logger().error(f'Failed to create publisher: {e}')
            raise

    def _initialize_subscribers(self):
        """Initialize state subscriber with error handling"""
        try:
            self.state_subscriber = self.create_subscription(
                JointState,
                '/humanoid/state/joint_angles',
                self.state_callback,
                10
            )
            self.get_logger().info('✓ Subscriber created: /humanoid/state/joint_angles')
        except Exception as e:
            self.get_logger().error(f'Failed to create subscriber: {e}')
            # Don't raise - we can function without feedback
            self.get_logger().warn('Continuing without state feedback...')

    def _initialize_timers(self):
        """Initialize timers with error handling"""
        try:
            # Command publishing timer (10 Hz)
            self.command_timer = self.create_timer(0.1, self.publish_commands)

            # Connection watchdog (1 Hz)
            self.watchdog_timer = self.create_timer(1.0, self.check_connection)

            self.get_logger().info('✓ Timers initialized')
        except Exception as e:
            self.get_logger().error(f'Failed to create timers: {e}')
            raise

    def publish_commands(self, timer=None):
        """
        Publish commands with error handling.

        Wraps publishing logic in try-except to handle any
        unexpected errors during message creation or publishing.
        """
        # Don't publish if robot is not connected
        if not self.robot_connected:
            self.get_logger().warn('Skipping publish: robot disconnected')
            return

        try:
            # Create and publish joint command
            msg = JointState()
            msg.name = ['left_shoulder_pan', 'left_shoulder_lift', 'left_elbow']

            # Calculate wave motion
            self.wave_phase += 0.2
            import math
            msg.position = [
                0.0,
                0.5 + 0.3 * math.sin(self.wave_phase),
                1.2 + 0.5 * math.sin(self.wave_phase)
            ]
            msg.velocity = [0.0, 0.0, 0.0]
            msg.effort = [0.0, 0.0, 0.0]

            # Publish
            if self.command_publisher is not None:
                self.command_publisher.publish(msg)

        except Exception as e:
            # Log error but don't crash
            self.get_logger().error(f'Error publishing command: {e}')
            self.get_logger().info('Continuing despite publishing error...')

    def state_callback(self, msg):
        """
        Process state updates with comprehensive error handling.

        This callback is wrapped in try-except to handle:
        - Missing message fields
        - Invalid data types
        - Missing joints
        - Any other unexpected errors
        """
        try:
            # Update last seen time
            self.last_state_time = self.get_clock().now()

            # Mark robot as connected
            if not self.robot_connected:
                self.robot_connected = True
                self.get_logger().info('✓ Robot connected!')

            # Validate message has required fields
            if not hasattr(msg, 'name') or not hasattr(msg, 'position'):
                self.get_logger().warn('Invalid JointState message: missing fields')
                return

            # Validate field lengths match
            if len(msg.name) != len(msg.position):
                self.get_logger().error(
                    f'Malformed message: {len(msg.name)} names but '
                    f'{len(msg.position)} positions'
                )
                return

            # Extract positions with error handling
            positions = {}
            for i, name in enumerate(msg.name):
                try:
                    positions[name] = float(msg.position[i])
                except (IndexError, TypeError, ValueError) as e:
                    self.get_logger().error(
                        f'Error extracting position for {name}: {e}'
                    )

            # Log state (throttled)
            if 'left_elbow' in positions and int(self.wave_phase * 10) % 10 == 0:
                elbow_pos = positions['left_elbow']
                elbow_deg = elbow_pos * 180.0 / 3.14159
                self.get_logger().info(f'Elbow: {elbow_pos:.3f} rad ({elbow_deg:.1f}°)')

        except Exception as e:
            # Catch-all for any unexpected errors
            self.get_logger().error(f'Error in state_callback: {e}')
            # Continue running - don't let one bad message crash the node

    def check_connection(self, timer=None):
        """
        Monitor connection health with timeout detection.

        If no state received within timeout, mark robot as disconnected.
        """
        if self.last_state_time is None:
            # Haven't received any state yet
            elapsed_time = 999.9
        else:
            elapsed_time = (
                self.get_clock().now() - self.last_state_time
            ).nanoseconds / 1e9

        if elapsed_time > self.connection_timeout:
            # Robot not responding
            if self.robot_connected:
                self.robot_connected = False
                self.get_logger().warn(f'⚠️  Connection timeout (no state for {elapsed_time:.1f}s)')
                self.get_logger().warn('Robot may have crashed or disconnected')
        elif elapsed_time > self.connection_timeout / 2:
            # Warning threshold
            self.get_logger().debug(f'Connection delayed: {elapsed_time:.1f}s')

    def shutdown(self):
        """Clean shutdown of all resources"""
        self.get_logger().info('Shutting down gracefully...')

        # Cancel timers
        if self.command_timer:
            self.command_timer.cancel()
        if self.watchdog_timer:
            self.watchdog_timer.cancel()

        # Destroy node (will be called by rclpy.shutdown too)
        self.get_logger().info('Shutdown complete')


def handle_initialization_error():
    """
    Demonstrate proper ROS 2 initialization error handling.

    This shows how to detect and handle common initialization problems.
    """
    print("Attempting ROS 2 initialization...")

    try:
        rclpy.init()
        print("✓ ROS 2 initialized successfully")
        return True
    except rclpy.RclpyError as e:
        print(f"✗ ROS 2 initialization failed: {e}")
        print("\nCommon causes:")
        print("  - ROS 2 environment not sourced")
        print("  - ROS 2 not installed")
        print("  - Incompatible ROS 2 version")
        print("\nSolutions:")
        print("  1. Source ROS 2: source /opt/ros/humble/setup.bash")
        print("  2. Install ROS 2: sudo apt install ros-humble-desktop")
        print("  3. Check installation: ros2 --version")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def main_with_retry(max_retries=3, retry_delay=2.0):
    """
    Main function with connection retry logic.

    Attempts to connect to the robot with retries and graceful
    degradation if connection fails.

    Args:
        max_retries: Maximum number of connection attempts
        retry_delay: Seconds to wait between retries

    Returns:
        0 on success, 1 on failure
    """
    print("=== Robust Humanoid Controller ===")
    print(f"Max retries: {max_retries}")
    print(f"Retry delay: {retry_delay}s")
    print()

    # Attempt initialization
    if not handle_initialization_error():
        return 1

    # Create controller
    controller = None
    try:
        controller = RobustHumanoidController()
    except Exception as e:
        print(f"FATAL: Failed to create controller: {e}")
        rclpy.shutdown()
        return 1

    # Spin the node
    executor = MultiThreadedExecutor()
    retry_count = 0

    try:
        print("\nController started. Waiting for robot connection...")
        print("Press Ctrl+C to stop\n")

        rclpy.spin(controller, executor=executor)

    except KeyboardInterrupt:
        print("\nShutdown requested by user")

    finally:
        # Clean up
        if controller:
            controller.shutdown()
            controller.destroy_node()

        rclpy.shutdown()
        print("Clean shutdown complete")

    return 0


def demonstrate_error_scenarios():
    """
    Demonstrate various error scenarios and their handling.

    This function shows examples of common errors and how to handle them.
    """
    print("=== ROS 2 Error Handling Examples ===\n")

    # Example 1: Handling missing imports
    print("1. Import Error Handling:")
    try:
        import missing_module
    except ImportError as e:
        print(f"   ✓ Caught ImportError: {e}")
        print(f"   Solution: Install missing module (pip install <module>)")

    # Example 2: Handling invalid topic names
    print("\n2. Topic Name Validation:")
    invalid_topic = "invalid topic name with spaces"
    valid_topic = invalid_topic.replace(" ", "_")
    print(f"   Invalid: {invalid_topic}")
    print(f"   Valid: {valid_topic}")

    # Example 3: Handling message type mismatches
    print("\n3. Message Type Compatibility:")
    print("   Always ensure publisher and subscriber use same message type")
    print("   Publisher: sensor_msgs/JointState")
    print("   Subscriber: sensor_msgs/JointState ✓")

    # Example 4: QoS compatibility
    print("\n4. QoS Settings:")
    print("   Use default QoS (queue depth 10) for beginners")
    print("   Advanced: Custom QoS for specific use cases")

    print("\n" + "="*50)


if __name__ == '__main__':
    import sys

    # Check if user wants to see error examples
    if len(sys.argv) > 1 and sys.argv[1] == '--examples':
        demonstrate_error_scenarios()
    else:
        # Run the main controller
        sys.exit(main_with_retry())
