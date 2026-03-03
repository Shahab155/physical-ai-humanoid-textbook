#!/usr/bin/env python3
"""
ROS 2 Publisher (Talker) Example

This node publishes messages to a topic, simulating a humanoid robot
sending status updates.

Learning Points:
- Creating a publisher with a specific message type
- Publishing messages at regular intervals using a timer
- Understanding message types (String in this case)
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HumanoidStatusPublisher(Node):
    """Publishes humanoid robot status messages

    This simulates a humanoid robot broadcasting its state.
    In a real robot, this would publish joint states, sensor readings, etc.
    """

    def __init__(self):
        """Initialize the publisher node"""
        # Call the Node constructor with a unique name
        super().__init__('humanoid_status_publisher')

        # Create a publisher for String messages
        # Topic: '/humanoid/status'
        # QoS: Queue size of 10 (how many messages to buffer if subscriber is slow)
        self.publisher = self.create_publisher(
            String,
            '/humanoid/status',
            10
        )

        # Create a timer to trigger periodic callbacks
        # Publish every 1 second (1.0 second interval)
        self.timer = self.create_timer(1.0, self.timer_callback)

        # Counter to simulate changing status
        self.counter = 0

        self.get_logger().info('Humanoid Status Publisher started')
        self.get_logger().info('Publishing to topic: /humanoid/status')


def timer_callback(self):
    """Callback function called periodically by the timer

    This publishes a new message each time it's called.
    """
    # Create a String message
    msg = String()

    # Set the message data
    # In a real robot, this would be actual joint angles, sensor data, etc.
    msg.data = f'Humanoid status message #{self.counter}'

    # Publish the message
    self.publisher.publish(msg)

    # Log what we published (useful for debugging)
    self.get_logger().info(f'Publishing: "{msg.data}"')

    # Increment counter for next message
    self.counter += 1


def main(args=None):
    """Main entry point for the publisher node"""
    rclpy.init(args=args)

    # Create our publisher node
    publisher_node = HumanoidStatusPublisher()

    try:
        # Spin the node (keep it alive and processing callbacks)
        rclpy.spin(publisher_node)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        publisher_node.get_logger().info('Keyboard interrupt, shutting down...')

    finally:
        # Clean up
        publisher_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
