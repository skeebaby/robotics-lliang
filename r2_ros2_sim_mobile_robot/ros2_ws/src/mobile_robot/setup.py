from setuptools import setup
import os
from glob import glob

package_name = 'mobile_robot'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='user@example.com',
    description='ROS2 package for mobile robot control and simulation',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'teleop_node = mobile_robot.teleop_node:main',
            'simple_controller = mobile_robot.simple_controller:main',
            'logger_node = mobile_robot.logger_node:main',
        ],
    },
)
