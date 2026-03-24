#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient # (1)!

from tuos_interfaces.action import CameraSweep # (2)!

class CameraSweepActionClient(Node):

    def __init__(self):
        super().__init__("camera_sweep_action_client") # (3)!
        self.actionclient = ActionClient(
            node=self, 
            action_type=CameraSweep, 
            action_name="camera_sweep"
        ) # (4)!

        self.declare_parameters(
            namespace='',
            parameters=[
                ('goal_images', 0),
                ('goal_angle', 0)
            ]
        ) # (5)!

    def send_goal(self): # (6)!
        images = self.get_parameter(
            'goal_images' 
        ).get_parameter_value().integer_value 
        angle = self.get_parameter(
            'goal_angle'
        ).get_parameter_value().integer_value

        goal = CameraSweep.Goal() # (7)!
        goal.sweep_angle = float(angle)
        goal.image_count = images

        self.actionclient.wait_for_server() # (8)!

        # send the goal to the action server:
        return self.actionclient.send_goal_async(goal)

def main(args=None): # (9)!
    rclpy.init(args=args)
    action_client = CameraSweepActionClient()
    future = action_client.send_goal()
    rclpy.spin_until_future_complete(action_client, future)

if __name__ == '__main__':
    main()