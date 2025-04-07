#!/usr/bin/env python 

import rclpy 
from rclpy.node import Node
import rclpy.node
from my_robot_interfaces.msg import TargetPositionCordinates

class chaseNode(Node):
    def __init__(self):
        super().__init__("chaseNode")
        self.target_sub = self.create_subscription(TargetPositionCordinates,"target_pose",self.callback_target_sub,10)

    def callback_target_sub(self,data):
        self.target_pose = data
        self.get_logger().info("data = " + str(data.target_pose))

def main(args=None):
    rclpy.init(args=args)
    node = chaseNode()
    rclpy.spin(node)
    rclpy.shutdown()