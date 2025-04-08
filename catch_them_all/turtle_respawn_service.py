#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn, Kill
from turtlesim.msg import Pose
from my_robot_interfaces.msg import TargetPositionCordinates

import random

class respawnNode(Node):

    def __init__(self):
        super().__init__("respawnNode")
        
        self.spawn_pose_dic = {}

        self._client = self.create_client(Spawn,"/spawn")
        self.kill_client = self.create_client(Kill,"/kill")
        
        #initiating 3 initial spawn turtles
        self.spawn_turtle_client_call()
        self.spawn_turtle_client_call()
        self.spawn_turtle_client_call()
        self.get_logger().info("Respawn client called")

        #Publisher for the publishing the target
        self.target_publisher = self.create_publisher(TargetPositionCordinates,"target_pose",10)

        #clock for publishing the msg every 0.1 sec 
        self.clk = self.create_timer(0.011,self.publish_target)

        # subscribing to main turtle position
        self.sub = self.create_subscription(Pose,"/turtle1/pose",self.callback_pose_sub,10)

    def spawn_turtle_client_call(self):
        self.random_name = "spawn" + str(random.randint(0,100))
        while not self._client.wait_for_service():
            self.get_logger().warning("Waiting for the add two int service ...")

        request = Spawn.Request() 
        x = random.uniform(0,10)
        y = random.uniform(0,10)
        request.x = x
        request.y = y
        request.name = self.random_name

        self.spawn_pose_dic[request.name] = [int(request.x), int(request.y)]
        # self.get_logger().info("the dictionary is " + str(self.spawn_pose_dic))
        future = self._client.call_async(request)
        future.add_done_callback(self.callback_respawn_service_done)

    def callback_respawn_service_done(self,future):
        response = future.result()
        self.get_logger().info(str(response)+" has been spawned")


    def publish_target(self):
        msg = TargetPositionCordinates()
        msg.target_pose = list(self.spawn_pose_dic.values())[0]
        self.target_publisher.publish(msg)

    def callback_pose_sub(self,pose):
        # ***
        # function decides whether to kill a spawn or not
        # ***

        main_turtle_pose_array = [int(pose.x), int(pose.y)]
        # self.get_logger().info(str(main_turtle_pose_array))

        if main_turtle_pose_array in self.spawn_pose_dic.values():
            self.get_logger().info("killed")
            for k,v in self.spawn_pose_dic.items():
                kill_turtle_key = None
                if v == main_turtle_pose_array:
                    kill_turtle_key = k
                    break
            del self.spawn_pose_dic[kill_turtle_key]
            self.kill_spwan_client_call(kill_turtle_key)
            self.spawn_turtle_client_call()
            
    
    def kill_spwan_client_call(self,name):


        while not self.kill_client.wait_for_service():
            self.get_logger().warning("Waiting for the add two int service ...")

        request = Kill.Request() 
        request.name = str(name)
        self.get_logger().info("Killed " + str(request.name))
        future = self.kill_client.call_async(request)
        future.add_done_callback(self.callback_respawn_service_done)


def main(args=None):
    rclpy.init(args=args)
    node = respawnNode()
    rclpy.spin(node)
    rclpy.shutdown()