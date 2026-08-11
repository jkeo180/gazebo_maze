import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher

def generate_launch_description():
    package_dir = get_package_share_directory('rosbot_xl_bridge')
    
    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'rosbot_xl.wbt')
    )

    rosbot_driver = Node(
        package='webots_ros2_driver',
        executable='driver',
        output='screen',
        arguments=['--robot-name', 'rosbot_xl'],
        parameters=[
            {'robot_description': os.path.join(package_dir, 'resource', 'rosbot_xl.urdf')},
        ]
    )

    return LaunchDescription([
        webots,
        rosbot_driver,
    ])
