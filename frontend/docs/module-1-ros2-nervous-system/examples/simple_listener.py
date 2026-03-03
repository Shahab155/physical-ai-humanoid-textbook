#!/usr/bin/env python3
"""
ROS 2 Subscriber (Listener) Example

This node subscribes to messages from a topic, simulating a monitoring
system that tracks humanoid robot status.

Learning Points:
- Creating a subscriber with a specific message type
- Defining callback functions to handle incoming messages
- Understanding how subscribers receive data asynchronously
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HumanoidStatusSubscriber(Node):
    """Subscribes to humanoid robot status messages

    This simulates a monitoring system that receives and displays
    the robot's status updates.
    """

    def __init__(self):
        """Initialize the subscriber node"""
        # Call the Node constructor with a unique name
        super().__init__('humanoid_status_subscriber')

        # Create a subscription to String messages
        # Topic: '/humanoid/status' (same topic the publisher uses)
        # QoS: Queue size of 10 (how many messages to buffer if processing is slow)
        # Callback: self.status_callback (function to call when message arrives)
        self.subscription = self.create_subscription(
            String,
            '/humanoid/status',
            self.status_callback,
            10
        )

        self.get_logger().info('Humanoid Status Subscriber started')
        self.get_logger().info('Listening to topic: /humanoid/status')


def status_callback(self, msg):
    """Callback function called when a new message arrives

    Args:
        msg: The message received from the topic
    """
    # Process the incoming message
    # In a real robot, this might update state, trigger actions, etc.
    self.get_logger().info(f'Received: "{msg.data}"')

    # Example: Parse message and take action
    if 'error' in msg.data.lower():
        self.get_logger().warn('Error condition detected in robot status!')
    elif 'ready' in msg.data.lower():
        self.get_logger().info('Robot is ready for commands')


def main(args=None):
    """Main entry point for the subscriber node"""
    rclpy.init(args=args)

    # Create our subscriber node
    subscriber_node = HumanoidStatusSubscriber()

    try:
        # Spin the node (keep it alive and processing callbacks)
        # The node will now receive messages and call status_callback
        rclpy.spin(subscriber_node)

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        subscriber_node.get_logger().info('Keyboard interrupt, shutting down...')

    finally:
        # Clean up
        subscriber_node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
