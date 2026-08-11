import rclpy
from geometry_msgs.msg import Twist

class MyRobotDriver:
    def init(self, webots_node, properties):
        # 1. Get the Webots robot instance from the node
        self.__robot = webots_node.robot

        # 2. Initialize your motors (replace names with your Webots motor names)
        self.__left_motor = self.__robot.getDevice('left wheel motor')
        self.__right_motor = self.__robot.getDevice('right wheel motor')

        # 3. Set motors to velocity control mode
        self.__left_motor.setPosition(float('inf'))
        self.__left_motor.setVelocity(0)
        self.__right_motor.setPosition(float('inf'))
        self.__right_motor.setVelocity(0)

        # 4. Initialize ROS 2 node and subscribe to /cmd_vel
        rclpy.init(args=None)
        self.__node = rclpy.create_node('my_robot_driver')
        self.__node.create_subscription(Twist, '/cmd_vel', self.__cmd_vel_callback, 1)

    def __cmd_vel_callback(self, twist):
        # Logic to convert Twist (linear/angular) to motor speeds
        # (Simplified example: mapping linear x directly to motors)
        self.__left_motor.setVelocity(twist.linear.x)
        self.__right_motor.setVelocity(twist.linear.x)

    def step(self):
        # This loop runs every simulation time step
        rclpy.spin_once(self.__node, timeout_sec=0)
