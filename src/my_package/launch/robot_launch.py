import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.utils import get_wbt_filename_from_launch_file

def generate_launch_description():
    package_dir = get_package_share_directory('my_package')
    
    # 1. Start Webots
    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'my_world.wbt')
    )

    # 2. Start the ROS 2 driver node
    ros2_supervisor = Node(
        package='webots_ros2_driver',
        executable='ros2_supervisor',
    )

    # 3. Define your robot driver
    # Note: 'my_robot.urdf' must match the filename in your resource folder
    robot_description_path = os.path.join(package_dir, 'resource', 'my_robot.urdf')
    
    my_robot_driver = Node(
        package='webots_ros2_driver',
        executable='driver',
        output='screen',
        parameters=[
            {'robot_description': robot_description_path},
        ]
    )

    return LaunchDescription([
        webots,
        ros2_supervisor,
        my_robot_driver,
        # This shuts down everything when Webots is closed
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        )
    ])
