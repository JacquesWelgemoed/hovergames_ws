import rclpy
from rclpy.node import Node 
from fire_drone_interfaces.msg import FireProbability
from fire_drone_interfaces.srv import Mission
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup


class FireSub(Node):

    def __init__(self):
        super().__init__('fire_sub')

        client_cb_group = MutuallyExclusiveCallbackGroup()
        sub_cb_group = None

        self.subscription = self.create_subscription(
            FireProbability, 
            'fire_probability', 
            self.carbon_callback,
            10, callback_group=sub_cb_group)
        self.subscription   # prevent unused variable warning

        self.cli = self.create_client(Mission, 'mission_service', callback_group=client_cb_group)
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('service not available, waiting again...')
        self.req = Mission.Request()
        self.client_futures = []


    def carbon_callback(self, msg):
        if msg.fire_probability > 0.6:   # If fire probability > 0.6 deploy drone
            self.get_logger().info('High probability of fire detected')
            # call mission server
            res = self.send_mission_request(True)
            self.get_logger().info('Responce received')
            if res.success:
                self.get_logger().info('Mission sent successfully')
            else:
                self.get_logger().info('Mission upload failed')

        else:
            self.get_logger().info("Low probability of fire detected")

    def send_mission_request(self, fire_detected):
        
        self.req.fire_detected = fire_detected
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        self.get_logger().info("After spin")
        return self.future.result()
    
  

        
def main(args=None):
    rclpy.init(args=args)

    fire_sub = FireSub()
    executor = MultiThreadedExecutor()
    executor.add_node(fire_sub)
    #rclpy.spin(fire_sub)
    
    try:
        fire_sub.get_logger().info("Starting fire_sub")
        executor.spin()
    except KeyboardInterrupt:
        fire_sub.get_logger().info("Keyboard interrupt, shutting down")
    


    fire_sub.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

    

