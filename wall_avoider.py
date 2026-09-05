import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class PIDController:
    """A simple PID controller helper class."""
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.integral = 0.0
        self.previous_error = 0.0

    def compute(self, setpoint, measurement, dt=0.1):
        error = setpoint - measurement
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        self.previous_error = error
        return (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)


class WallAvoider(Node):
    def __init__(self):
        super().__init__('wall_avoider')
        
        # Subscribers and Publishers
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10
        )        
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10) 

        # Control Parameters
        self.desired_distance = 0.60    # Desired distance from the wall (meters)
        self.obstacle_threshold = 0.50  # Distance threshold to trigger turns (meters)
        self.move_forward_speed = 0.2   # m/s
        self.rotational_speed = 0.5     # rad/s
        
        # Controller Setup
        self.pid_controller = PIDController(Kp=1.5, Ki=0.0, Kd=0.1)

    def lidar_callback(self, msg):
        ranges = list(msg.ranges)
        if not ranges:
            return

        # 1. Clean data (replace 0.0 or inf values with a max value)
        cleaned_ranges = [r if (r > 0.0 and r != float('inf')) else msg.range_max for r in ranges]

        # 2. Extract specific laser sub-sections (Assuming 360-degree LiDAR)
        # Front field of view (e.g., -10 to +10 degrees around index 0)
        front_indices = list(range(0, 90))
        front_distances = [cleaned_ranges[i % len(cleaned_ranges)] for i in front_indices]
        min_front_distance = min(front_distances)

        # Left side field of view (e.g., around 90 degrees)
        left_index = len(cleaned_ranges) // 4  # 90 degrees
        min_left_distance = min(cleaned_ranges[left_index-10 : left_index+11])

        self.get_logger().info(
            f'Front: {min_front_distance:.2f}m | Left: {min_left_distance:.2f}m'
        )

        # 3. Navigation / Wall Avoiding Logic
        twist_msg = Twist()

        if min_front_distance < self.obstacle_threshold:
            # Obstacle ahead! Pivot right immediately to avoid a crash.
            twist_msg.linear.x = 0.0
            twist_msg.angular.z = -self.rotational_speed
            self.get_logger().warn('Obstacle detected ahead! Turning right.')
        else:
            # Safe ahead: Use PID to follow the wall on the left side
            # Control signal adjusts the robot's angular steering
            control_signal = self.pid_controller.compute(self.desired_distance, min_left_distance)
            
            twist_msg.linear.x = self.move_forward_speed
            # Clip the control signal to avoid radical spinning
            twist_msg.angular.z = max(min(control_signal, self.rotational_speed), -self.rotational_speed)

        # Publish the velocities
        self.publisher_.publish(twist_msg)


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


