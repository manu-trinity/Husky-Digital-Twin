import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from sensor_msgs.msg import NavSatFix
import math

class PositionVerifier(Node):
    def __init__(self):
        super().__init__('position_verifier')
        self.odom_sub = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10)
        self.gps_sub = self.create_subscription(
            NavSatFix, '/reach_rs2/gps/data', self.gps_callback, 10)
        self.latest_odom = None
        self.latest_gps = None
        self.start_odom = None
        self.start_gps = None
        self.end_odom = None
        self.end_gps = None
        self.state = "start"

    def odom_callback(self, msg):
        self.latest_odom = msg.pose.pose.position

    def gps_callback(self, msg):
        self.latest_gps = msg

    def calculate_odom_distance(self):
        dx = self.end_odom.x - self.start_odom.x
        dy = self.end_odom.y - self.start_odom.y
        return math.sqrt(dx**2 + dy**2)

    def calculate_gps_distance(self):
        lat_to_m = 111139  # meters per degree
        lon_to_m = 111139  # Simplified, assuming small latitude
        dlat = (self.end_gps.latitude - self.start_gps.latitude) * lat_to_m
        dlon = (self.end_gps.longitude - self.start_gps.longitude) * lon_to_m
        return math.sqrt(dlat**2 + dlon**2)

    def run(self):
        while rclpy.ok():
            rclpy.spin_once(self)
            if self.latest_odom is None or self.latest_gps is None:
                continue

            if self.state == "start":
                print("Press Enter to record start position...")
                input()
                self.start_odom = self.latest_odom
                self.start_gps = self.latest_gps
                print(f"Start Odom: x={self.start_odom.x:.3f}, y={self.start_odom.y:.3f}")
                print(f"Start GPS: Lat={self.start_gps.latitude:.6f}, Lon={self.start_gps.longitude:.6f}")
                self.state = "move"

            elif self.state == "move":
                print("Move the robot forward with teleop, then press Enter...")
                input()
                self.end_odom = self.latest_odom
                self.end_gps = self.latest_gps
                print(f"End Odom: x={self.end_odom.x:.3f}, y={self.end_odom.y:.3f}")
                print(f"End GPS: Lat={self.end_gps.latitude:.6f}, Lon={self.end_gps.longitude:.6f}")
                self.state = "done"

            elif self.state == "done":
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