import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class Doer(Node):
    def __init__(self):
        super().__init__('doer')
        self.subscription = self.create_subscription(
            Float32, 'sensor_data', self.act, 10)
        self.get_logger().info('Doer node started')

    def act(self, msg):
        if msg.data > 100.4:
            self.get_logger().info(f'FEVER DETECTED: {msg.data} — take action!')
        else:
            self.get_logger().info(f'Temperature normal: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = Doer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
