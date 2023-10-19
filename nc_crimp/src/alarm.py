#!/usr/bin/env python

import rospy
#from robot_data_display.msg import AlarmMsg
from nc_crimp.msg import AlarmMsg
# from msg_pkg.msg import AlarmMsg
import json
import socket
from datetime import datetime

LOCAL_IP = '127.0.0.1'  # usually fixed
LOCAL_PORT = 80  # usually fixed
REMOTE_IP = '192.168.4.4'  # follow the machine
REMOTE_PORT = 9760  # follow the machine

while True:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((REMOTE_IP, REMOTE_PORT))
        break
    except socket.error as e:
        print("Socket error:", str(e))
        print("Retrying..")
        #exit(1)

data = {
    "dsID": "www.hc-system.com.RemoteMonitor",
    "reqType": "query",
    "packID": "0",
    "queryAddr":['curAlarm']
}   

json_data = json.dumps(data).encode('utf-8')

rospy.init_node('alarm_msg_publisher')  # Initialize the ROS node
pub = rospy.Publisher('alarm_msg', AlarmMsg, queue_size=10)  # Create the publisher

rate = rospy.Rate(10)  # Publish at 10 Hz

while not rospy.is_shutdown():
    try:
        client_socket.sendall(json_data)  # Send the JSON packet to the server
        received_data = client_socket.recv(1024)  # Receive data from the server
    except socket.timeout:
        print("Socket timeout occurred!")
        print("Retrying..")
        #client_socket.close()
        #exit(1)
    except socket.error as e:
        print("Socket error:", str(e))
        print("Retrying..")
        #client_socket.close()
        #exit(1)

    # Decode the JSON response
    json_response = json.loads(received_data.decode('utf-8'))

    query_data = json_response['queryData']

    alarm = query_data[0]

    alarm_msg = AlarmMsg()
    alarm_msg.header.stamp = rospy.Time.now()
    alarm_msg.alarm = alarm

    pub.publish(alarm_msg)  # Publish the Alarm message
    rospy.loginfo(alarm_msg)
    
    rate.sleep()

client_socket.close()