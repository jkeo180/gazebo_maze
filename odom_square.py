import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math

class OdomDrive(Node):
    def __init__(self):
        super().__init__('odom_drive_node')
        self.publisher = self.create_publisher(Twist, '/model/vehicle_blue/cmd_vel', 10)
        self.subscription = self.create_subscription(Odometry, '/model/vehicle_blue/odometry', self.odom_callback, 10)
        
        self.start_x = None
        self.start_y = None
        self.distance_goal = 1.0 # 1 meter
        self.is_moving = True

    def odom_callback(self, msg):
        curr_x = msg.pose.pose.position.x
        curr_y = msg.pose.pose.position.y

        # Initialize start position once
        if self.start_x is None:
            self.start_x, self.start_y = curr_x, curr_y
            return

        # Calculate how far we've gone
        diff_x = curr_x - self.start_x
        diff_y = curr_y - self.start_y
        dist_traveled = math.sqrt(diff_x**2 + diff_y**2)

        if self.is_moving:
            if dist_traveled < self.distance_goal:
                move_msg = Twist()
                move_msg.linear.x = 0.2 # Slow and steady
                self.publisher.publish(move_msg)
                self.get_logger().info(f'Distance: {dist_traveled:.2f}m')
            else:
                self.publisher.publish(Twist()) # Stop
                self.get_logger().info("Target reached!")
                self.is_moving = False

def main():
    rclpy.init()
    node = OdomDrive()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
