#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Twist

from pyModbusTCP.client import ModbusClient

plc = ModbusClient(host="192.168.1.5",port=502,auto_open=True)

wheel_bias = 0.36
wheel_radius = 0.16

brake = 2
left_reg = 4
right_reg = 6

class modbus:

    def __init__(self) -> None:
        rospy.init_node("Modbus_Velocity_sender")
        print("Node Started")
        self.left_rpm = 0
        self.right_rpm = 0
        self.write_flag = 1
        rospy.Subscriber('/cmd_vel', Twist, self.vel_callback)


    def vel_callback(self, msg):
        self.vel_x = msg.linear.x
        self.vel_z = msg.angular.z
        while self.write_flag > 10000:
            write_flag = 1
            plc.write_single_register(0, self.write_flag)
            check = plc.read_holding_registers(0, 1)
            if check[0] == self.write_flag:
                print("Flag Reset")
                break
        self.left_rpm = ((self.vel_x - (self.vel_z * wheel_bias / 2.0)) / wheel_radius) * 60 / (2*3.14159)
        self.right_rpm = -((self.vel_x + (self.vel_z * wheel_bias / 2.0)) / wheel_radius) * 60 / (2*3.14159)
        print("LEFT RPM = {}, RIGHT RPM = {}".format(self.left_rpm, self.right_rpm))

        while(1):
            self.write_data = [self.write_flag,self.left_rpm, self.right_rpm]
            plc.write_multiple_registers(0,4,6,self.write_data)
            check_flag = plc.read_holding_registers(0,1)
            if check_flag:
                print("Check FLAG")
            else:
                print("Error Reading check flag")
            if check_flag[0] == self.write_flag:
                self.write_flag = self.write_flag + 1
                break

if __name__ == '__main__':
    try:
        start = modbus()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
