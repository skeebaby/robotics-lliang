#!/usr/bin/env python3
"""
Teleoperation node for mobile robot.

This node reads keyboard input and publishes velocity commands to /cmd_vel.
Controls:
- Arrow Up/Down: Move forward/backward
- Arrow Left/Right: Rotate left/right
- Space: Stop
- q: Quit
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import select
import termios
import tty


class TeleopNode(Node):
    """Keyboard teleoperation node for mobile robot."""

    def __init__(self):
        super().__init__('teleop_node')
        
        # Publisher for velocity commands
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # Velocity parameters
        self.linear_speed = 0.5  # m/s
        self.angular_speed = 1.0  # rad/s
        
        self.get_logger().info('Teleop node started. Use arrow keys to control the robot.')
        self.get_logger().info('Controls:')
        self.get_logger().info('  Arrow Up: Move forward')
        self.get_logger().info('  Arrow Down: Move backward')
        self.get_logger().info('  Arrow Left: Rotate left')
        self.get_logger().info('  Arrow Right: Rotate right')
        self.get_logger().info('  Space: Stop')
        self.get_logger().info('  q: Quit')

    def get_key(self):
        """Get a single keypress from stdin (non-blocking)."""
        if sys.platform == 'win32':
            import msvcrt
            if msvcrt.kbhit():
                key = msvcrt.getch()
                return key.decode('utf-8') if isinstance(key, bytes) else key
        else:
            # Unix-like systems
            tty.setraw(sys.stdin.fileno())
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                key = sys.stdin.read(1)
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
                return key
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return None

    def publish_velocity(self, linear_x, angular_z):
        """Publish velocity command."""
        twist = Twist()
        twist.linear.x = linear_x
        twist.angular.z = angular_z
        self.cmd_vel_pub.publish(twist)

    def run(self):
        """Main loop for teleoperation."""
        global settings
        if sys.platform != 'win32':
            settings = termios.tcgetattr(sys.stdin)
        
        try:
            while rclpy.ok():
                key = self.get_key()
                
                if key is None:
                    continue
                
                if key == '\x1b':  # Escape sequence for arrow keys
                    key = self.get_key()
                    if key == '[':
                        key = self.get_key()
                        if key == 'A':  # Up arrow
                            self.publish_velocity(self.linear_speed, 0.0)
                            self.get_logger().info('Forward')
                        elif key == 'B':  # Down arrow
                            self.publish_velocity(-self.linear_speed, 0.0)
                            self.get_logger().info('Backward')
                        elif key == 'C':  # Right arrow
                            self.publish_velocity(0.0, -self.angular_speed)
                            self.get_logger().info('Rotate right')
                        elif key == 'D':  # Left arrow
                            self.publish_velocity(0.0, self.angular_speed)
                            self.get_logger().info('Rotate left')
                elif key == ' ':  # Space
                    self.publish_velocity(0.0, 0.0)
                    self.get_logger().info('Stop')
                elif key == 'q' or key == '\x03':  # q or Ctrl+C
                    self.publish_velocity(0.0, 0.0)
                    self.get_logger().info('Quitting...')
                    break
                
                rclpy.spin_once(self, timeout_sec=0.01)
        except KeyboardInterrupt:
            pass
        finally:
            self.publish_velocity(0.0, 0.0)
            if sys.platform != 'win32':
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
            self.get_logger().info('Teleop node shutdown')


def main(args=None):
    rclpy.init(args=args)
    
    node = TeleopNode()
    try:
        node.run()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
