#!/usr/bin/env python 

import rclpy 
from rclpy.node import Node
import rclpy.node
from my_robot_interfaces.msg import TargetPositionCordinates
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
from my_robot_interfaces.srv import KillTurtle


class chaseNode(Node):
    def __init__(self):
        super().__init__("chaseNode")

        self.target_pose_x = None
        self.target_pose_y = None

        self.target_sub = self.create_subscription(TargetPositionCordinates,"target_pose",self.callback_target_sub,10)
        self.cmd_vel_pub = self.create_publisher(Twist,"/turtle1/cmd_vel",10)

        # subscribing to main turtle position
        self.turtle_pose_sub = self.create_subscription(Pose,"/turtle1/pose",self.callback_pose_sub,10)

        #initiating kill client:
        self.kill_client = self.create_client(KillTurtle,"kill_catched_turtle")

    def callback_target_sub(self,data):
        self.target_pose_x = data.target_pose[0]
        self.target_pose_y = data.target_pose[1]
        # self.get_logger().info("target = " + str(self.target_pose_x) + str(self.target_pose_y))

    def callback_pose_sub(self,pose):
        # ***
        # function decides whether to kill a spawn or not
        # ***


        cmd_msg = Twist()
        if not (self.target_pose_x == None) or (self.target_pose_y == None):
            
            slope = (self.target_pose_y - pose.y) / (self.target_pose_x - pose.x)
            angle_radians = math.atan2((self.target_pose_y - pose.y),(self.target_pose_x - pose.x))

            # Allowable error for angle comparison
            epsilon = 0.09
            turn_flag = True

            # Compare the angles with a tolerance for precision issues
            if (abs(pose.theta - angle_radians) > epsilon):
                self.get_logger().info("rotating") 
                cmd_msg.angular.z = 1.0  # Rotate if not aligned
            else:
                cmd_msg.angular.z = 0.0  # Stop rotation once aligned

            if (((abs(pose.x - self.target_pose_x) > (epsilon)) or (abs(pose.y - self.target_pose_y) > (epsilon) )) ):
                self.get_logger().info("moving") 
                cmd_msg.linear.x = 0.5  
            else:
                cmd_msg.linear.x = 0.0 
                self.chase_success_client_call()

            # Publish the movement commanda
            self.cmd_vel_pub.publish(cmd_msg)
    
    def chase_success_client_call(self):

        while not self.kill_client.wait_for_service():
            self.get_logger().warning("Waiting for the add two int service ...")
        request = KillTurtle.Request()
        request.confirm_kill = True
        future = self.kill_client.call_async(request)
        future.add_done_callback(self.callback_respawn_service_done)

    def callback_respawn_service_done(self,future):
        response = future.result()
        # self.get_logger().info(str(response))

        
def main(args=None):
    rclpy.init(args=args)
    node = chaseNode()
    rclpy.spin(node)
    rclpy.shutdown()