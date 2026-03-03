#!/usr/bin/env python3
"""
Sensor Visualizer Launch File
Launches Gazebo with sensor-equipped robot and RViz2 for visualization

Usage:
    ros2 launch module2_digital_twin sensor_visualizer.launch.py
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
import os

pkg_name = 'module2_digital_twin'
robot_urdf_path = os.path.join(
    os.path.dirname(__file__),
    '../../robot-models/robot_with_sensors.urdf'
)

def generate_launch_description():
    # Launch Gazebo with obstacle course
    gazebo = ExecuteProcess(
        cmd=['gazebo', '-s', 'libgazebo_ros_factory.so',
              'obstacle_course.world'],
        output='screen'
    )

    # Read robot URDF
    with open(robot_urdf_path, 'r') as f:
        robot_urdf = f.read()

    # Spawn robot with sensors
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'robot_with_sensors',
            '-topic', '/robot_description',
            '-x', robot_urdf,
            '-z', '0 0 0.2',
        ],
        output='screen'
    )

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_urdf}],
        output='screen'
    )

    # RViz2 with pre-configured sensor displays
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(
            os.path.dirname(__file__),
            'sensor_visualizer.rviz'
        )],
        condition=LaunchConfigurationEquals('launch_rviz', 'true')
    )

    return LaunchDescription([
        gazebo,
        RegisterEventHandler(
            OnProcessExit(
                target_action=gazebo,
                on_exit=[spawn_robot, robot_state_publisher]
            )
        ),
        rviz,
    ])