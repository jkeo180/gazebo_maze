import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from front_distance import get_front_distance

class WallAvoider(Node):
    def __init__(self):
        super().__init__('wall_avoider')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10)        
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10) 
        self.desired_distance = 0.60  # Desired distance from the wall
        self.obstacle_threshold = 0.5  # Distance threshold for obstacle detection
        self.move_forward_speed = 0.2  # Forward speed when no obstacle is detected
        self.rotational_speed = 0.5  # Rotational speed when avoiding obstacles
        self.pid_controller = PIDController(Kp=1.0, Ki=0.0, Kd=0.0)  # PID controller for wall following
        self.previous_error = 0.0  # Previous error for PID controller

    def lidar_callback(self, msg):
        ranges = list(msg.ranges)
        front_ranges = min_distance = float('inf')
        for i in range(-10, 11):  
            index = (i + len(ranges)) % len(ranges)  
            if ranges[index] < min_distance:
                min_distance = ranges[index]
                min_distance = min(front_ranges)
                measured_distance = min_distance 
                self.get_logger().info(
                    f'Front distance: {min_distance:.2f} m'
                    f'Left distance: {min(ranges[:len(ranges)//2]):.2f} m'
                    )
                control_signal = self.compute_measurement(
                measured_distance
                )
        if all_ranges > self.obstacle_threshold:
            if min_distance > self.obstacle_threshold:
                    twist_msg = Twist()
                    twist_msg.linear.x = self.move_forward_speed
                    twist_msg.angular.z = 0.0
                    self.publish_twist(twist_msg)
            else:
                    twist_msg = Twist()
                    twist_msg.linear.x = 0.0
                    twist_msg.angular.z = self.rotational_speed
                    self.publish_twist(twist_msg)
                    angular.z = self.Pcontroller(error)
                    cmd.linear.x = self.move_forward_speed
                    cmd.angular.z = angular.z

    def compute_measurement(self, measured_distance):
        error = self.desired_distance - measured_distance
        control_signal = self.Pcontroller(error)
        return control_signal
   
    def Pcontroller(self, error):
        Kp = 0.5  # Proportional gain
        angular.z = Kp * error
        return Kp * error
   
    def publish_twist(self, twist_msg):
        self.publisher_.publish(twist_msg)
        cmd_vel_msg = Twist()

    if __name__ == '__main__':  
        rclpy.init()
        wall_avoider = WallAvoider()
        rclpy.spin(wall_avoider)
        wall_avoider.destroy_node()
        rclpy.shutdown()

