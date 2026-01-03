#!/usr/bin/env python3

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description for bringing up mobile robot nodes."""
    
    # Launch configuration
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    
    # Declare launch arguments
    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time if true'
    )
    
    # Teleop node (commented out by default - uncomment if you want to use it)
    # teleop_node = Node(
    #     package='mobile_robot',
    #     executable='teleop_node',
    #     name='teleop_node',
    #     output='screen'
    # )
    
    # Simple controller node
    controller_node = Node(
        package='mobile_robot',
        executable='simple_controller',
        name='simple_controller',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )
    
    # Logger node
    logger_node = Node(
        package='mobile_robot',
        executable='logger_node',
        name='logger_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )
    
    return LaunchDescription([
        declare_use_sim_time,
        # teleop_node,  # Uncomment to enable teleoperation
        controller_node,
        logger_node,
    ])
