import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import Twist
from rosgraph_msgs.msg import Clock
import math
import threading
import time

class PositionVerifier(Node):
    def __init__(self):
        super().__init__('position_verifier')
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.gps_sub = self.create_subscription(NavSatFix, '/reach_rs2/gps/data', self.gps_callback, 10)
        self.clock_sub = self.create_subscription(Clock, '/clock', self.clock_callback, 10)
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.latest_odom = None
        self.latest_gps = None
        self.start_odom = None
        self.start_gps = None
        self.end_odom = None
        self.end_gps = None
        self.sim_time = 0.0
        self.state = "start"
        self.spin_thread = threading.Thread(target=self.ros_spin)
        self.spin_thread.daemon = True
        self.spin_thread.start()

    def ros_spin(self):
        rclpy.spin(self)

    def odom_callback(self, msg):
        self.latest_odom = msg.pose.pose.position

    def gps_callback(self, msg):
        self.latest_gps = msg

    def clock_callback(self, msg):
        self.sim_time = msg.clock.sec + msg.clock.nanosec * 1e-9

    def move_forward(self, speed=1.0, duration=15.0):
        twist_msg = Twist()
        twist_msg.linear.x = speed
        while self.sim_time == 0.0 and rclpy.ok():
            time.sleep(0.1)
        start_sim_time = self.sim_time
        print(f"Start simulated time: {start_sim_time:.3f} s")
        while (self.sim_time - start_sim_time < duration) and rclpy.ok():
            self.cmd_vel_pub.publish(twist_msg)
            time.sleep(0.02)  # 50 Hz publishing
        end_sim_time = self.sim_time
        print(f"End simulated time: {end_sim_time:.3f} s")
        print(f"Elapsed simulated time: {end_sim_time - start_sim_time:.3f} s")
        twist_msg.linear.x = 0.0
        self.cmd_vel_pub.publish(twist_msg)
        self.get_logger().info("Movement stopped.")

    def calculate_odom_distance(self):
        dx = self.end_odom.x - self.start_odom.x
        dy = self.end_odom.y - self.start_odom.y
        return math.sqrt(dx**2 + dy**2)

    def calculate_gps_distance(self):
        R = 6371000
        lat1, lon1 = math.radians(self.start_gps.latitude), math.radians(self.start_gps.longitude)
        lat2, lon2 = math.radians(self.end_gps.latitude), math.radians(self.end_gps.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def run(self):
        while rclpy.ok():
            if self.latest_odom is None or self.latest_gps is None or self.sim_time == 0.0:
                continue
            if self.state == "start":
                self.start_odom = self.latest_odom
                self.start_gps = self.latest_gps
                print(f"Start Odom: x={self.start_odom.x:.3f}, y={self.start_odom.y:.3f}")
                print(f"Start GPS: Lat={self.start_gps.latitude:.6f}, Lon={self.start_gps.longitude:.6f}")
                self.move_forward()
                time.sleep(1.0)
                self.state = "done"
            elif self.state == "done":
                self.end_odom = self.latest_odom
                self.end_gps = self.latest_gps
                print(f"End Odom: x={self.end_odom.x:.3f}, y={self.end_odom.y:.3f}")
                print(f"End GPS: Lat={self.end_gps.latitude:.6f}, Lon={self.end_gps.longitude:.6f}")
                odom_dist = self.calculate_odom_distance()
                gps_dist = self.calculate_gps_distance()
                print(f"\nDistance (Odom): {odom_dist:.3f} meters")
                print(f"Distance (GPS): {gps_dist:.3f} meters")
                print(f"Difference: {abs(odom_dist - gps_dist):.3f} meters")
                break

def main():
    rclpy.init()
    node = PositionVerifier()
    node.run()
    rclpy.shutdown()

if __name__ == '__main__':
    main()