#!/usr/bin/env python3 

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class turtlePositionNode(Node):
    
    def __init__(self):

        super().__init__("tutle_position_tracker")
        self.sub = self.create_subscription(Pose,"/turtle1/pose",self.callback_pose_sub,10)
        self.sub2 = self.create_subscription(Pose,"/spawn2/pose",self.callback_pose_sub2,10)

    def callback_pose_sub(self,pose):
        self.get_logger().info("current position = " + str(pose.x) + " , " + str(pose.y))
    
    def callback_pose_sub2(self,pose):
        self.get_logger().info("current position of spwan2 = " + str(pose.x) + " , " + str(pose.y))

def main(args=None):
    rclpy.init(args=args)
    node = turtlePositionNode()
    rclpy.spin(node)
    rclpy.shutdown()