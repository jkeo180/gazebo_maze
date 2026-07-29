import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class Mover(Node):
    def __init__(self):
        super().__init__('mover')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.5, self.move)
        self.get_logger().info('Mover started!')

    def move(self):
        msg = Twist()
        msg.linear.x = 0.5
        msg.angular.z = 0.0
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = Mover()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()