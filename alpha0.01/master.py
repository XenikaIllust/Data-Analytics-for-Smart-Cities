#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
import timeit
import time
from functools import partial
import cv2
import numpy as np
from cv_bridge import CvBridge
x=0
a=0

def gps_callback(data):
        print("1: ", data.pose.covariance)
        file1.write(str(data.pose.covariance) + "\n")

def rgb_callback(data): 
        # print("rgb ROS sending delay: " + str(timeit.default_timer() * (10 ** 3) - (data.header.stamp.secs * (10 ** 3) + data.header.stamp.nsecs * (10 ** -6))) + "ms")
        br = CvBridge()
        
        im = br.imgmsg_to_cv2(data, desired_encoding="bgr8")
        #cv2.imwrite("/media/nvidia/ExtremeSSD/rgb_images/" + str(time.time()) + ".jpg", im)
        timestamp1 = '%.10f' % time.time()
        
        filename = "/media/nvidia/ExtremeSSD/rgb_images/" + str(timestamp1) + ".npz"
        
        np.savez_compressed(filename, im)
        # timestamp2 = time.time()
        
        # print(im.shape)
        # im.tofile("/media/nvidia/ExtremeSSD/rgb_images/xxx.txt", sep="\t", format="%s")
        # cv2.imwrite("/media/nvidia/ExtremeSSD/rgb_images/xxx.png", im)
        # print("rgb npz save time: " + str(timestamp2-timestamp1) + "s")
        print(filename)

def depth_callback(data, args):
        idx = args[0]
        global x
        print(data.header.frame_id + "channel=" + str(idx))
        # print("depth ROS sending delay: " + str(timeit.default_timer() * (10 ** 3) - (data.header.stamp.secs * (10 ** 3) + data.header.stamp.nsecs * (10 ** -6))) + "ms")
        br = CvBridge()
        im = br.imgmsg_to_cv2(data, desired_encoding="mono16")
        timestamp1 = time.time()
        filename = "/media/nvidia/ExtremeSSD/depth_images/" + str(data.header.frame_id) + '-channel' + str(idx) + ".npz"
        np.savez_compressed(filename, im)
        #print('fdf')
        timestamp2 = time.time()
        print("depth npz save time: " + str(timestamp2-timestamp1) + "s")
        # print(filename)
        #timestamp2 = time.time()
        #print(timestamp2)
        #depth_callback.counter+=1
        x+=1
        
        #print(x)

def master():
    global a
    rospy.init_node('master', anonymous=True)
    
    a =  time.time()
    
    #de-multiplex the packages
    for idx in range(10):
    	rospy.Subscriber("depth"+str(idx), Image, depth_callback, (idx,))
 
    #timestamp2 = time.time()
    #print(a)
    #rospy.Subscriber("depth1", Image, depth_callback)
    # rospy.Subscriber('RGB', Image, rgb_callback)

    rospy.spin()
         
if __name__ == "__main__":
     
        master()
        global a
        #print(a)
        b = time.time()
        c=int(b)-int(a)
        #print(c)
        #print("rgb npz save time: " + str(c) + "s")
        #print(b)
        #print(c/x)

