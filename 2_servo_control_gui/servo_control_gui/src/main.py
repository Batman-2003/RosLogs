#!/usr/bin/env python

import tkinter as tk

import rospy 
from std_msgs.msg import UInt16
import subprocess
import time

message_pub = rospy.Publisher("servo", UInt16, queue_size=1)
rospy.init_node("This_One!!!")


def run():
    yaw_int = int( float(entry1.get()) * 180 / 3.1415 )
    x = '0'
    y = '0'
    z = '1.3'
    r = '0'
    p = '0'
    yaw = entry1.get() 
    message_pub.publish(yaw_int)
    process = subprocess.Popen(['rosrun','tf2_ros','static_transform_publisher',x,y,z,yaw,p,r,'world_link','knob_link'])
    # process.wait()
    print("ID : ", process.pid)
    time.sleep(0.5)
    print("Killing : ",process.pid)
    process.kill()
    print('done')


global flag_0
flag_0 = True

def updo():
    run()

root = tk.Tk()
root.geometry("600x600")
root.title("Servo GUI")
root.configure(bg="#333333")

lb1 = tk.Label(root, text="Servo Controller", font="Cascadia 24", fg="white" , bg="#333333")
lb1.pack(padx= 20, pady = 20)

txtbx = tk.Text(root, font=("Cascadia" ,24), bg = "orange" , height = 3)
txtbx.pack(padx = 20, pady = 20 )

entry1 = tk.Entry(root)
entry1.pack(padx = 20, pady = 20)

btn1 = tk.Button(root, text="Press to Confirm", command = updo)
btn1.pack(padx=20, pady=20)

root.mainloop()
