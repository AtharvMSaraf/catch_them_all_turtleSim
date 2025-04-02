#!/usr/bin/env python3 

import rclpy
from rclpy.node import Node

class respawnNode(Node):

    def __init__(self):
        super().__init__("respawnService")

        self.srv = self.create_service()



def main(args=None):
    rclpy.init(args=args)



    rclpy.shutdown()