#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn

class respawnNode(Node):

    def __init__(self):
        super().__init__("respawnNode")

        self._client = self.create_client(Spawn,"/spawn")
        self.callback_client()
        self.get_logger().info("Respawn client called")

    def callback_client(self):

        while not self._client.wait_for_service():
            self.get_logger().warning("Waiting for the add two int service ...")

        request = Spawn.Request() 
        request.x = 2.0
        request.y = 2.0
        request.name = "spawn2"

        future = self._client.call_async(request)
        future.add_done_callback(self.callback_respawn_service_done)

    def callback_respawn_service_done(self,future):
        response = future.result()
        self.get_logger().info(str(response.name))
        self.get_logger().info(str(response)+" has been spawned")



def main(args=None):
    rclpy.init(args=args)
    node = respawnNode()
    rclpy.spin(node)
    rclpy.shutdown()