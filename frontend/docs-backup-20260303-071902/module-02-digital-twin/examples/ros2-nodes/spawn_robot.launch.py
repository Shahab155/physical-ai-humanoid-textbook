#!/usr/bin/env python3
"""
Spawn Robot Launch File
Launches Gazebo with the differential drive robot spawned

Usage:
    ros2 launch module2_digital_twin spawn_robot.launch.py
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
import os

pkg_name = 'module2_digital_twin'
robot_urdf_path = os.path.join(
    os.path.dirname(__file__),
    '../../robot-models/diff_drive_robot.urdf'
)

def generate_launch_description():
    # Launch Gazebo with empty world
    gazebo = ExecuteProcess(
        cmd=['gazebo', 'empty_world.world', '-s', 'libgazebo_ros_factory.so'],
        output='screen'
    )

    # Read robot URDF
    with open(robot_urdf_path, 'r') as f:
        robot_urdf = f.read()

    # Spawn robot using gazebo_ros spawn service
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'diff_drive_robot',
            '-topic', '/robot_description',
            '-x', robot_urdf,
            '-z', '0 0 0.2',  # Initial pose (x, y, z, roll, pitch, yaw)
        ],
        output='screen'
    )

    # Robot state publisher (publishes TF transforms)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_urdf}],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        RegisterEventHandler(
            OnProcessExit(
                target_action=gazebo,
                on_exit=[spawn_robot, robot_state_publisher]
            )
        ),
    ])