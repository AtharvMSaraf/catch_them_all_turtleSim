#!/usr/bin/env python 

import rclpy 
from rclpy.node import Node
import rclpy.node
from my_robot_interfaces.msg import TargetPositionCordinates
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math


class chaseNode(Node):
    def __init__(self):
        super().__init__("chaseNode")

        self.target_pose_x = None
        self.target_pose_y = None

        self.target_sub = self.create_subscription(TargetPositionCordinates,"target_pose",self.callback_target_sub,10)
        self.cmd_vel_pub = self.create_publisher(Twist,"/turtle1/cmd_vel",10)

        # subscribing to main turtle position
        self.turtle_pose_sub = self.create_subscription(Pose,"/turtle1/pose",self.callback_pose_sub,10)

    def callback_target_sub(self,data):
        self.target_pose_x = data.target_pose[0]
        self.target_pose_y = data.target_pose[1]
        self.get_logger().info("target = " + str(self.target_pose_x) + str(self.target_pose_y))

    def callback_pose_sub(self,pose):
        # ***
        # function decides whether to kill a spawn or not
        # ***

        cmd_msg = Twist()
        if not (self.target_pose_x == None) or (self.target_pose_y == None):
            self.get_logger().info("rotating")
            if pose.x != self.target_pose_x:
                cmd_msg.linear.x = 1.0
            else:
                cmd_msg.linear.x = 1.0

            if pose.y != self.target_pose_y:
                cmd_msg.linear.y = 1.0
            else:
                cmd_msg.linear.y = 0.0

        self.cmd_vel_pub.publish(cmd_msg)
        
def main(args=None):
    rclpy.init(args=args)
    node = chaseNode()
    rclpy.spin(node)
    rclpy.shutdown()