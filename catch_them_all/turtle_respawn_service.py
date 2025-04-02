#!/usr/bin/env python3

import rclpy
from rclpy.node import Node


class respawnNode(Node):

    def __init__(self):
        super().__init__("respawnNode")
        self.get_logger().info("success")



def main(args=None):
    rclpy.init(args=args)
    node = respawnNode()
    rclpy.shutdown()