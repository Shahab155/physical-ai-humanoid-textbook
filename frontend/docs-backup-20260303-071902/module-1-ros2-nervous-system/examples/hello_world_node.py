#!/usr/bin/env python3
"""
Minimal ROS 2 "Hello World" Node

This example demonstrates the simplest possible ROS 2 node.
It initializes ROS 2, creates a node, and prints a greeting.

Learning Points:
- Basic ROS 2 node lifecycle (init → create node → spin → shutdown)
- Every ROS 2 program must initialize and shutdown properly
- Nodes run independently until explicitly stopped
"""

import rclpy
from rclpy.node import Node


def main(args=None):
    """Main entry point for ROS 2 node

    Args:
        args: Command-line arguments (None uses sys.argv)
    """
    # 1. Initialize ROS 2 communications
    # This sets up the communication infrastructure
    rclpy.init(args=args)

    # 2. Create a node with a unique name
    # The node name identifies this process in the ROS 2 network
    node = Node('hello_world_node')

    # Get the node's logger (built-in logging system)
    logger = node.get_logger()

    # Log a message (appears in console)
    logger.info('Hello, ROS 2! This is my first humanoid robot node.')

    # 3. Spin the node
    # This keeps the node alive and processing callbacks
    # Since we have no callbacks, we'll spin once just to demonstrate
    try:
        logger.info('Node is running. Press Ctrl+C to exit...')
        rclpy.spin_once(node)  # Process one iteration of callbacks

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        logger.info('Node received interrupt signal')

    finally:
        # 4. Clean up
        # Always destroy nodes and shutdown to release resources
        node.destroy_node()
        rclpy.shutdown()
        logger.info('Node shutdown complete')


if __name__ == '__main__':
    main()
