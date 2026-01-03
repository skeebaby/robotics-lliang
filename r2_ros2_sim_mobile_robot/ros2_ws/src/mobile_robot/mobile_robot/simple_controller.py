#!/usr/bin/env python3
"""
Simple controller node for mobile robot.

This node subscribes to /cmd_vel and converts the velocity commands
into wheel velocities for a differential drive robot.
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64


class SimpleController(Node):
    """Simple controller node that converts cmd_vel to wheel commands."""

    def __init__(self):
        super().__init__('simple_controller')
        
        # Robot parameters
        self.wheel_separation = 0.3  # meters (distance between wheels)
        self.wheel_radius = 0.1  # meters
        
        # Subscriber for velocity commands
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10
        )
        
        # Publishers for wheel commands
        self.left_wheel_pub = self.create_publisher(
            Float64,
            'wheel_left/cmd_vel',
            10
        )
        self.right_wheel_pub = self.create_publisher(
            Float64,
            'wheel_right/cmd_vel',
            10
        )
        
        self.get_logger().info('Simple controller node started')
        self.get_logger().info(f'Wheel separation: {self.wheel_separation} m')
        self.get_logger().info(f'Wheel radius: {self.wheel_radius} m')

    def cmd_vel_callback(self, msg):
        """
        Convert cmd_vel (Twist) to wheel velocities.
        
        For a differential drive robot:
        - linear.x: forward velocity (m/s)
        - angular.z: angular velocity (rad/s)
        
        Wheel velocities:
        v_left = (2 * v - omega * L) / 2
        v_right = (2 * v + omega * L) / 2
        where:
        - v = linear.x
        - omega = angular.z
        - L = wheel_separation
        """
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        
        # Calculate wheel velocities
        # v = (v_left + v_right) / 2
        # omega = (v_right - v_left) / L
        # Solving for v_left and v_right:
        v_left = linear_x - (angular_z * self.wheel_separation / 2.0)
        v_right = linear_x + (angular_z * self.wheel_separation / 2.0)
        
        # Convert linear velocities to angular velocities (rad/s)
        # omega_wheel = v_wheel / r_wheel
        left_angular_vel = v_left / self.wheel_radius
        right_angular_vel = v_right / self.wheel_radius
        
        # Publish wheel commands
        left_cmd = Float64()
        left_cmd.data = left_angular_vel
        self.left_wheel_pub.publish(left_cmd)
        
        right_cmd = Float64()
        right_cmd.data = right_angular_vel
        self.right_wheel_pub.publish(right_cmd)
        
        # Log occasionally (reduce spam)
        self.get_logger().debug(
            f'Cmd: v={linear_x:.2f} m/s, ω={angular_z:.2f} rad/s | '
            f'Wheels: L={left_angular_vel:.2f}, R={right_angular_vel:.2f} rad/s'
        )


def main(args=None):
    rclpy.init(args=args)
    
    node = SimpleController()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
