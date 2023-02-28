import rclpy
from rclpy.node import Node 
from fire_drone_interfaces.msg import FireProbability

class FireSniffer(Node):

    def __init__(self):
        super().__init__('fire_sniffer')
        self.publisher = self.create_publisher(FireProbability, 'fire_probability', 10)
        timer_period = 10 # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 1

    def timer_callback(self):
        self.sniff()

    def sniff(self):
        # read carbon levels from bosch sensor
        if self.i<2:
            msg = FireProbability()
            msg.fire_probability = 0.8    # placeholder for sensor val
            self.publisher.publish(msg)
            self.i = self.i + 1
        
       

def main(args=None):
    rclpy.init(args=args)

    fire_sniffer = FireSniffer()
    rclpy.spin(fire_sniffer)

    fire_sniffer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
        

