#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry

import cv2
import numpy as np
from cv_bridge import CvBridge


def gps_callback(data, file1):
        print("1: ", data.pose.covariance)
        file1.write(str(data.pose.covariance) + "\n")

        
def rgb_callback(data, file2):
	# print("2: ", data.width,data.step, data.encoding)
        #image = Im.frombytes("RGB", (data.width, data.height), data.data)
        #image.show()
        # file2.write()
        
        # br = CvBridge()
        # im = br.imgmsg_to_cv2(data, desired_encoding="rgb16")
        # cv2.imwrite("./test.png", im)
        pass

def depth_callback(data, file3):
        br = CvBridge()
        im = br.imgmsg_to_cv2(data, desired_encoding="mono16")
        print(im[360][640])
        cv2.imwrite("./test5.png", im)

def master(file1, file2):
	rospy.init_node('master', anonymous=True)
        rospy.Subscriber('gps_meas', Odometry, gps_callback, file1)
        rospy.Subscriber('RGB', Image, rgb_callback, file2)
        rospy.Subscriber('depth', Image, depth_callback, file3)
	rospy.spin()
	

if __name__ == "__main__":
	file1 = open('coords.txt', 'w')
        file2 = open('depth.txt', 'w')
        file3 = open('image.txt', 'w')
	master(file1, file2)
	file1.close()
        file2.close()
