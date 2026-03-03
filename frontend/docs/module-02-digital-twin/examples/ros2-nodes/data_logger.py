#!/usr/bin/env python3
"""
Sensor Data Logger
Records sensor data (LiDAR, Depth Camera, IMU) to CSV files

Usage:
    ros2 run module2_digital_twin data_logger.py
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image, Imu
import csv
from datetime import datetime
import os

class SensorDataLogger(Node):
    def __init__(self):
        super().__init__('sensor_data_logger')

        # Create output directory
        self.output_dir = os.path.join(
            os.path.dirname(__file__),
            '../../logs/'
        )
        os.makedirs(self.output_dir, exist_ok=True)

        # Initialize CSV files
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        self.lidar_file = open(os.path.join(self.output_dir, f'lidar_{timestamp}.csv'), 'w')
        self.imu_file = open(os.path.join(self.output_dir, f'imu_{timestamp}.csv'), 'w')

        # CSV writers
        self.lidar_writer = csv.writer(self.lidar_file)
        self.imu_writer = csv.writer(self.imu_file)

        # Write headers
        self.lidar_writer.writerow(['timestamp', 'angle_min', 'angle_max', 'range_min', 'range_max', 'ranges'])
        self.imu_writer.writerow(['timestamp', 'orientation_x', 'orientation_y', 'orientation_z', 'orientation_w',
                                   'angular_vel_x', 'angular_vel_y', 'angular_vel_z',
                                   'linear_acc_x', 'linear_acc_y', 'linear_acc_z'])

        # Subscribers
        self.lidar_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10
        )

        self.imu_sub = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )

        self.depth_sub = self.create_subscription(
            Image,
            '/depth/image_raw',
            self.depth_callback,
            10
        )

        self.get_logger().info('Sensor data logger started')
        self.get_logger().info(f'Logging to: {self.output_dir}')

    def lidar_callback(self, msg):
        """Log LiDAR scan data"""
        timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9
        ranges_str = ','.join([str(r) for r in msg.ranges])

        self.lidar_writer.writerow([
            timestamp,
            msg.angle_min,
            msg.angle_max,
            msg.range_min,
            msg.range_max,
            f'[{ranges_str}]'
        ])
        self.lidar_file.flush()

    def imu_callback(self, msg):
        """Log IMU data"""
        timestamp = msg.header.stamp.sec + msg.header.stamp.nanosec * 1e-9

        self.imu_writer.writerow([
            timestamp,
            msg.orientation.x,
            msg.orientation.y,
            msg.orientation.z,
            msg.orientation.w,
            msg.angular_velocity.x,
            msg.angular_velocity.y,
            msg.angular_velocity.z,
            msg.linear_acceleration.x,
            msg.linear_acceleration.y,
            msg.linear_acceleration.z
        ])
        self.imu_file.flush()

    def depth_callback(self, msg):
        """Log depth camera (just count frames for now)"""
        # Full depth image logging is memory-intensive
        self.get_logger().info(f'Depth frame received: {msg.header.stamp.sec}', once=True)

    def __del__(self):
        """Close files on shutdown"""
        self.lidar_file.close()
        self.imu_file.close()

def main(args=None):
    rclpy.init(args=args)
    node = SensorDataLogger()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()