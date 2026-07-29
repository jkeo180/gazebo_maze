import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class Seer(Node):
    def __init__(self):
        super().__init__('seer')
        self.publisher_ = self.create_publisher(Float32, 'sensor_data', 10)
        self.timer = self.create_timer(1.0, self.read_sensor)
        self.get_logger().info('Seer node started')

    def read_sensor(self):
        msg = Float32()
        msg.data = 98.6  # pretend body temp reading
        self.get_logger().info(f'Sensing: {msg.data}')
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = Seer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
