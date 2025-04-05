# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# from my_robot_interfaces.srv import turtlePose
# from turtlesim.msg import Pose

# class spawnPoseServiceNode(Node):
#     def __init__(self):
#         self.x = 100
#         self.y = 100
#         super().__init__("spawn_Pose_Service_Node")
#         self.srv = self.create_service(turtlePose,"turtle_pose",self.callback_srv)

#     def callback_srv(self, request: turtlePose.Request, response: turtlePose.Response):
#         topic = "/" + str(request.name) + "/pose"
#         self.sub = self.create_subscription(Pose,topic,self.callback_sub)
#         self.get_logger().info("the x and y are " + str(self.x) + " , " + self.y)
#         response.x = self.x
#         response.y = self.y
#         return response
    
#     def callback_sub(self,msg):
#         self.x = msg.x
#         self.y = msg.y
        
# def main(args=None):
#     rclpy.init(args=args)
#     rclpy.shutdown()