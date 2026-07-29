import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class FigureEight(Node):
    def __init__(self):
        super().__init__('figure_eight_node')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.run_shape)
        self.msg = Twist()
        self.start_time = time.time()

    def run_shape(self):
        now = time.time() - self.start_time
        
        # First 4 seconds: Turn Left
        if now < 4.0:
            self.msg.linear.x = 1.5
            self.msg.angular.z = 1.5
        # Next 4 seconds: Turn Right
        elif now < 8.0:
            self.msg.linear.x = 1.5
            self.msg.angular.z = -1.5
        # Stop
        else:
            self.msg.linear.x = 0.0
            self.msg.angular.z = 0.0
            self.publisher_.publish(self.msg)
            self.get_logger().info('Figure 8 Complete!')
            raise SystemExit # Stops the node

        self.publisher_.publish(self.msg)

def main():
    rclpy.init()
    node = FigureEight()
    try:
        rclpy.spin(node)
    except SystemExit:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
