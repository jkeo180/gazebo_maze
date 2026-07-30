import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math

class OdomStop(Node):
    def __init__(self):
        super().__init__('odom_stop_node')
        # Topics must match your specific robot
        self.publisher = self.create_publisher(Twist, '/model/vehicle_blue/cmd_vel', 10)
        self.subscription = self.create_subscription(Odometry, '/model/vehicle_blue/odometry', self.odom_callback, 10)
        
        self.start_x = None
        self.start_y = None
        self.goal_distance = 1.0  # Move exactly 1 meter
        self.finished = False

    def odom_callback(self, msg):
        curr_x = msg.pose.pose.position.x
        curr_y = msg.pose.pose.position.y

        if self.start_x is None:
            self.start_x, self.start_y = curr_x, curr_y
            return

        # Calculate distance using the distance formula: sqrt(dx^2 + dy^2)
        dist = math.sqrt((curr_x - self.start_x)**2 + (curr_y - self.start_y)**2)

        if dist < self.goal_distance and not self.finished:
            move = Twist()
            move.linear.x = 0.2  # Speed
            self.publisher.publish(move)
            self.get_logger().info(f'Distance: {dist:.2f}m')
        else:
            self.publisher.publish(Twist())  # Stop!
            self.get_logger().info('Target 1.0m reached!')
            self.finished = True

def main():
    rclpy.init()
    node = OdomStop()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
