from fire_drone_interfaces.srv import Mission
import rclpy
from rclpy.node import Node

class MissionServer(Node):

    def __init__(self):
        super().__init__('mission_server')
        self.srv = self.create_service(Mission, 'mission_service', self.mission_srv_callback)

    def mission_srv_callback(self, request, response):
        response.success = False
        if request.fire_detected:
            #create mission here
            self.get_logger().info('Fire detected, mission generation and upload in progress')
            response.success = True
        self.get_logger().info('Returning a response: %s' % (response.success))
        return response
       

def main(args=None):
    rclpy.init(args=args)
    mission_server = MissionServer()
    rclpy.spin(mission_server)
    rclpy.shutdown()

if __name__ == "__main__":
    main()