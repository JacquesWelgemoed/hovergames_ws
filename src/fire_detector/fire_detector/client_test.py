import sys

from fire_drone_interfaces.srv import Mission
import rclpy
from rclpy.node import Node

class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(Mission, 'mission_service')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Mission.Request()

    def send_request(self, fire):
        self.req.fire_detected = fire
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()
    
def main(args=None):
    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()
    response = minimal_client.send_request(bool(sys.argv[1]))
    minimal_client.get_logger().info('Result of mission request: %s' %
        (response.success))

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()