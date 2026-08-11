import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class WallAvoider(Node):
    def __init__(self):
        super().__init__('wall_avoider')
        # Subscribe to Lidar scan data
        self.scan_subscriber = self.create_subscription(
            LaserScan,
            '/scan', # Change this to match your robot's scan topic
            self.scan_callback,
            10
        )
        # Publish velocity commands to move the robot
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.laser_forward = 10.0 # Initialize with a large safe distance
        self.cmd = Twist()

    def scan_callback(self, msg):
        # Read the middle 10 degrees of the laser scan (front of the robot)
        middle_index = len(msg.ranges) // 2
        front_ranges = msg.ranges[middle_index-5 : middle_index+5]
        
        # Filter out invalid readings (e.g., inf or NaN)
        valid_ranges = [r for r in front_ranges if r > msg.range_min]
        
        if valid_ranges:
            self.laser_forward = min(valid_ranges)
        else:
            self.laser_forward = msg.range_max

    def timer_callback(self):
        # Obstacle avoidance threshold (e.g., 0.8 meters)
        safe_distance = 0.8 

        if self.laser_forward < safe_distance:
            # Wall detected! Stop and turn right
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = -0.5 # Negative is clockwise, positive is counter-clockwise
            self.get_logger().info(f"Wall detected at {self.laser_forward:.2f}m. Turning...")
        else:
            # No wall in front, drive forward
            self.cmd.linear.x = 0.2
            self.cmd.angular.z = 0.0
            self.get_logger().info(f"Path clear. Distance: {self.laser_forward:.2f}m")

        self.publisher.publish(self.cmd)

def main(args=None):
    rclpy.init(args=args)
    node = WallAvoider()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

