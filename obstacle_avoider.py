import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from front_distance import get_front_distance


class ObstacleAvoider(Node):

    def __init__(self):
        super().__init__('obstacle_avoider')
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10)
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)

    def lidar_callback(self, msg):
        ranges_list = list(msg.ranges)
        num_readings = len(ranges_list)

        if num_readings == 0:
            self.get_logger().warn("Empty LaserScan readings received")
            return

        # 1. Map target indices (assuming 0 is rear, num_readings//2 is front)
        front_index = num_readings // 2
        left_index = (3 * num_readings) // 4
        right_index = num_readings // 4

        window = max(1, num_readings // 18)

        # 2. Extract ranges safely using a bounded list-slicing method
        front_ranges = ranges_list[max(0, front_index - window) : min(num_readings, front_index + window)]
        left_ranges = ranges_list[max(0, left_index - window) : min(num_readings, left_index + window)]
        right_ranges = ranges_list[max(0, right_index - window) : min(num_readings, right_index + window)]

        # 3. Calculate filtered distances using custom helper
        front_distance = get_front_distance(front_ranges, msg.range_min, msg.range_max)
        left_distance = get_front_distance(left_ranges, msg.range_min, msg.range_max)
        right_distance = get_front_distance(right_ranges, msg.range_min, msg.range_max)

        twist = Twist()

        # 4. Guard clause for blind front sensors
        if front_distance is None:
            self.get_logger().warn("No valid front readings")
            self.publisher_.publish(twist)
            return

        self.get_logger().info(f"Front: {front_distance:.2f} m")
        self.get_logger().info(f"Left: {left_distance if left_distance is not None else 'unknown'}")
        self.get_logger().info(f"Right: {right_distance if right_distance is not None else 'unknown'}")

        # 5. Avoidance execution using the left_room vs right_room heuristic
        if front_distance < 0.6:
            left_room = left_distance if left_distance is not None else 0.0
            right_room = right_distance if right_distance is not None else 0.0

            if left_room > right_room:
                self.get_logger().warn(f"Wall at {front_distance:.2f}m! Turning LEFT (more room).")
                twist.linear.x = 0.0
                twist.angular.z = 0.5   # Positive = counter-clockwise (Left)
            else:
                self.get_logger().warn(f"Wall at {front_distance:.2f}m! Turning RIGHT (more room).")
                twist.linear.x = 0.0
                twist.angular.z = -0.5  # Negative = clockwise (Right)
        else:
            self.get_logger().info("Path clear, moving forward")
            twist.linear.x = 0.2
            twist.angular.z = 0.0

        self.publisher_.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    obstacle_avoider = ObstacleAvoider()
    rclpy.spin(obstacle_avoider)
    obstacle_avoider.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
