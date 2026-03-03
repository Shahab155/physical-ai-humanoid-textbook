#!/usr/bin/env python3
"""
ROS 2 Service Server and Client Example

This demonstrates synchronous request-response communication,
simulating a humanoid robot's calibration service.

Learning Points:
- Creating a service server (provides the service)
- Creating a service client (calls the service)
- Request-response pattern vs. pub-sub pattern
"""

from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class CalibrationService(Node):
    """ROS 2 Service Server

    Provides a service to calibrate a humanoid robot's joints.
    In this example, we use AddTwoInts as a simple proxy for calibration.
    """

    def __init__(self):
        """Initialize the service server node"""
        super().__init__('calibration_service')

        # Create a service server
        # Service type: AddTwoInts (example service with two integers)
        # Service name: '/humanoid/calibrate_joint'
        # Callback: self.calibrate_joint_callback (handles requests)
        self.srv = self.create_service(
            AddTwoInts,
            '/humanoid/calibrate_joint',
            self.calibrate_joint_callback
        )

        self.get_logger().info('Calibration Service started')
        self.get_logger().info('Ready to calibrate joints...')


def calibrate_joint_callback(self, request, response):
    """Callback function called when a service request arrives

    Args:
        request: The service request (contains a and b)
        response: The service response (we fill in sum)

    Returns:
        response: The modified response object
    """
    # Log the request
    self.get_logger().info(
        f'Calibration request received: joint_id={request.a}, '
        f'calibration_value={request.b}'
    )

    # Simulate calibration work
    # In a real robot, this would:
    # 1. Move joint to home position
    # 2. Measure sensor readings
    # 3. Store calibration data
    # 4. Return success status

    # For this example, we just add the two numbers
    response.sum = request.a + request.b

    self.get_logger().info(f'Calibration complete: result={response.sum}')

    return response


class CalibrationClient(Node):
    """ROS 2 Service Client

    Calls the calibration service to calibrate a specific joint.
    """

    def __init__(self):
        """Initialize the service client node"""
        super().__init__('calibration_client')

        # Create a service client
        # Service type: AddTwoInts (must match server)
        # Service name: '/humanoid/calibrate_joint' (must match server)
        self.cli = self.create_client(AddTwoInts, '/humanoid/calibrate_joint')

        # Flag to track if request is complete
        self.future = None


def send_calibrate_request(self, joint_id, calibration_value):
    """Send a calibration request to the service

    Args:
        joint_id: ID of the joint to calibrate
        calibration_value: Calibration value to apply
    """
    # Wait for the service to be available
    self.get_logger().info('Waiting for calibration service...')
    if not self.cli.wait_for_service(timeout_sec=5.0):
        self.get_logger().error('Service not available!')
        return

    # Create a request
    request = AddTwoInts.Request()
    request.a = joint_id
    request.b = calibration_value

    # Send the request asynchronously
    self.future = self.cli.call_async(request)
    self.get_logger().info(
        f'Calibration request sent: joint_id={joint_id}, '
        f'value={calibration_value}'
    )


def send_request_sync(joint_id, calibration_value):
    """Simplified version that sends request and waits for response

    This is a standalone function that demonstrates the client side
    without needing to manage the node spinning.
    """
    # Initialize ROS 2
    rclpy.init()

    # Create client node
    client = CalibrationClient()

    # Send request
    client.send_calibrate_request(joint_id, calibration_value)

    # Spin until response received
    while rclpy.ok():
        rclpy.spin_once(client)
        if client.future.done():
            break

    # Get the response
    response = client.future.result()
    client.get_logger().info(
        f'Calibration result: {response.sum}'
    )

    # Clean up
    client.destroy_node()
    rclpy.shutdown()

    return response.sum


if __name__ == '__main__':
    # Example: Calibrate joint 5 with value 42
    print("Sending calibration request...")
    result = send_request_sync(5, 42)
    print(f"Calibration completed with result: {result}")
