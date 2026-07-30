import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math

def euler_from_quaternion(x, y, z, w):
    """Convert a quaternion into euler angles (roll, pitch, yaw)"""
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    return math.atan2(t3, t4)

class OdomTurn(Node):
    def __init__(self):
        super().__init__('odom_turn_node')
        self.publisher = self.create_publisher(Twist, '/model/vehicle_blue/cmd_vel', 10)
        self.subscription = self.create_subscription(Odometry, '/model/vehicle_blue/odometry', self.odom_callback, 10)
        
        self.start_yaw = None
        self.target_yaw = None
        self.finished = False

    def odom_callback(self, msg):
        # 1. Get current orientation
        q = msg.pose.pose.orientation
        current_yaw = euler_from_quaternion(q.x, q.y, q.z, q.w)

        # 2. Set targets on first run
        if self.start_yaw is None:
            self.start_yaw = current_yaw
            # Turn 90 degrees (pi/2 radians)
            self.target_yaw = self.start_yaw + (math.pi / 2.0)
            return

        # 3. Calculate difference (handling angle wrapping)
        diff = self.target_yaw - current_yaw
        
        if abs(diff) > 0.05 and not self.finished:
            move = Twist()
            move.angular.z = 0.3  # Turning speed
            self.publisher.publish(move)
            self.get_logger().info(f'Current Yaw: {current_yaw:.2f}, Goal: {self.target_yaw:.2f}')
        else:
            self.publisher.publish(Twist())  # Stop
            self.get_logger().info('90-Degree Turn Complete!')
            self.finished = True

def main():
    rclpy.init()
    node = OdomTurn()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
