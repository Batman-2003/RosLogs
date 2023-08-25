#!/usr/bin/env python

##---------------------------------------------------------------------Imports------------------------------------------------------------------

import rospy

import tf_conversions

import tf2_ros
import geometry_msgs.msg
import math as m
import numpy as np

# import matplotlib.pyplot as plt

##------------------------------------------------------------Assignment of Variables-----------------------------------------------------------

##----------------------------------------------------------------------------------------------------------------------------------------------

i = 0
it = 0
forward_flag = True

##--------------------------------------------Default Values ( will get modified using data from spreadsheet------------------------------------

R = 0.05                                    ## Radius of Spherical Object
R_O = R + 0.002                             ## Radius with offset
N = 1                                       ## NO. of rotations 
NS = 480                                    ## NO.of samples per rotation
L = 0.200                                   ## Length of Spindle
Z_OFFSET = 0.025                            ## OFFSET by Z components of x & y axes
##------------------------------------------------------------------Function Defs---------------------------------------------------------------

def x_z_from_pitch(thetap, radius_of_sphere = R, radius_of_offset = R_O, length_of_spindle = L, z_offset = 0.025):
    x = np.zeros(NS * N)
    z = np.zeros(NS * N)
    for _ in range(NS * N):
        x[_] = (radius_of_offset * m.sin(thetap[_])) + (length_of_spindle * m.sin(thetap[_]))
        z[_] = z_offset + radius_of_sphere + (radius_of_offset * m.cos(thetap[_])) + (length_of_spindle * m.cos(thetap[_]))

    print(" x : {_}".format(_ = x))
    print(" z : {_}".format(_ = z))
    print(radius_of_sphere)
    print(radius_of_offset)
    print(length_of_spindle)
    return x,z

def handle_joint_pose(x, y, z,thetap, thetay):
    br = tf2_ros.TransformBroadcaster()

    t0 = geometry_msgs.msg.TransformStamped()
    t0.header.stamp = rospy.Time.now()
    t0.header.frame_id = "base_link"
    t0.child_frame_id = "x_axis_link"
    t0.transform.translation.x = x[it]    ##x[it]
    t0.transform.translation.y = 0
    t0.transform.translation.z = 0
    q = tf_conversions.transformations.quaternion_from_euler(0,0,0)
    t0.transform.rotation.x = q[0]
    t0.transform.rotation.y = q[1]
    t0.transform.rotation.z = q[2]
    t0.transform.rotation.w = q[3]
    br.sendTransform(t0)

    t2 = geometry_msgs.msg.TransformStamped()
    t2.header.stamp = rospy.Time.now()
    t2.header.frame_id = "base_link"
    t2.child_frame_id = "y_axis_link"
    t2.transform.translation.x = 0
    t2.transform.translation.y = y[it]  ##y[it]
    t2.transform.translation.z = 0
    q = tf_conversions.transformations.quaternion_from_euler(0,0,0)
    t2.transform.rotation.x = q[0]
    t2.transform.rotation.y = q[1]
    t2.transform.rotation.z = q[2]
    t2.transform.rotation.w = q[3]
    br.sendTransform(t2)

    t3 = geometry_msgs.msg.TransformStamped()
    t3.header.stamp = rospy.Time.now()
    t3.header.frame_id = "base_link"
    t3.child_frame_id = "rotor_link"
    t3.transform.translation.x = x[it] - 0.2125
    t3.transform.translation.y = y[it]
    t3.transform.translation.z = Z_OFFSET + R
    q = tf_conversions.transformations.quaternion_from_euler(thetay[it] % (2 * m.pi),0,0)
    t3.transform.rotation.x = q[0]
    t3.transform.rotation.y = q[1]
    t3.transform.rotation.z = q[2]
    t3.transform.rotation.w = q[3]
    br.sendTransform(t3)

    t4 = geometry_msgs.msg.TransformStamped()
    t4.header.stamp = rospy.Time.now()
    t4.header.frame_id = "base_link"
    t4.child_frame_id = "spindle_base_link"
    t4.transform.translation.x = 0
    t4.transform.translation.y = 0 - 0.008
    t4.transform.translation.z = 0.30 - 0.016 
    q = tf_conversions.transformations.quaternion_from_euler(0,0,3.1415)
    t4.transform.rotation.x = q[0]
    t4.transform.rotation.y = q[1]
    t4.transform.rotation.z = q[2]
    t4.transform.rotation.w = q[3]
    br.sendTransform(t4)

    t5 = geometry_msgs.msg.TransformStamped()
    t5.header.stamp = rospy.Time.now()
    t5.header.frame_id = "spindle_base_link"
    t5.child_frame_id = "spindle_nozzle_link"
    t5.transform.translation.x = 0
    t5.transform.translation.y = 0
    t5.transform.translation.z = 0
    q = tf_conversions.transformations.quaternion_from_euler(0,thetap[it] +3.1415,0)
    t5.transform.rotation.x = q[0]
    t5.transform.rotation.y = q[1]
    t5.transform.rotation.z = q[2]
    t5.transform.rotation.w = q[3]
    br.sendTransform(t5)

# def make_polar_plot():
#     ax = plt.subplot(111,projection='polar')
#     ax.plot(thetay, x)
#     plt.show()

def iterator_handler_spiral():
    global it
    if it == len(thetap) - 1:
        it = 0
    else :
        it = it + 1


##----------------------------------------------------------------------Main Func---------------------------------------------------------------

if __name__ == '__main__':
    rospy.init_node('tf2_broadcaster')
    rate = rospy.Rate(20)

    y = np.zeros(NS * N)
    thetay = np.linspace(0, N * 2 * m.pi, N * NS)
    thetap = np.zeros(N*NS)


    x = np.linspace(0,0.16, N*NS)
    z = np.zeros(N*NS)

    # make_polar_plot()

    while not rospy.is_shutdown():
        handle_joint_pose(x,y,z,thetap,thetay)
        iterator_handler_spiral()
        rate.sleep()