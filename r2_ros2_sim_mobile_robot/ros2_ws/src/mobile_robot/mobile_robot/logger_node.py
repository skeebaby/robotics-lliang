#!/usr/bin/env python3
"""
Logger node for mobile robot.

This node subscribes to odometry data and publishes formatted log messages
with robot state information.
"""

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import String
import math


class LoggerNode(Node):
    """Logger node that monitors and logs robot state."""

    def __init__(self):
        super().__init__('logger_node')
        
        # Subscriber for odometry
        self.odom_sub = self.create_subscription(
            Odometry,
            'odom',
            self.odom_callback,
            10
        )
        
        # Publisher for logs
        self.log_pub = self.create_publisher(
            String,
            'robot/log',
            10
        )
        
        # Logging parameters
        self.log_interval = 1.0  # seconds
        self.last_log_time = self.get_clock().now()
        
        self.get_logger().info('Logger node started')
        self.get_logger().info(f'Logging interval: {self.log_interval} s')

    def odom_callback(self, msg):
        """Process odometry messages and publish logs."""
        current_time = self.get_clock().now()
        
        # Only log at specified interval to reduce spam
        time_since_last_log = (current_time - self.last_log_time).nanoseconds / 1e9
        
        if time_since_last_log >= self.log_interval:
            # Extract pose information
            pose = msg.pose.pose
            position = pose.position
            orientation = pose.orientation
            
            # Extract velocity information
            twist = msg.twist.twist
            linear_vel = twist.linear.x
            angular_vel = twist.angular.z
        
            # Convert quaternion to Euler angles (yaw)
            # yaw = atan2(2*(w*z + x*y), 1 - 2*(y^2 + z^2))
            w = orientation.w
            x = orientation.x
            y = orientation.y
            z = orientation.z
            
            yaw = math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))
            yaw_deg = math.degrees(yaw)
            
            # Format log message
            log_msg = (
                f"Robot State | "
                f"Position: ({position.x:.2f}, {position.y:.2f}, {position.z:.2f}) | "
                f"Yaw: {yaw_deg:.1f}° | "
                f"Velocity: linear={linear_vel:.2f} m/s, angular={angular_vel:.2f} rad/s"
            )
            
            # Publish log
            log_string = String()
            log_string.data = log_msg
            self.log_pub.publish(log_string)
            
            # Also log to console
            self.get_logger().info(log_msg)
            
            self.last_log_time = current_time


def main(args=None):
    rclpy.init(args=args)
    
    node = LoggerNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
