#!/usr/bin/env python

import rospy
from robot_data_display.msg import AlarmMsg
import json
import socket
from datetime import datetime
import time

LOCAL_IP = '127.0.0.1'
LOCAL_PORT = 80
REMOTE_IP = '192.168.4.4'
REMOTE_PORT = 9760

alarm_triggered = False
prev_alarm_msg = None

print ("alarm node running...")

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((REMOTE_IP, REMOTE_PORT))
    
except socket.error as e:
    print("Socket error:", str(e))
    client_socket.close()
    exit(1)

data = {
    "dsID": "www.hc-system.com.RemoteMonitor",
    "reqType": "query",
    "packID": "0",
    "queryAddr": ['curAlarm']
}

json_data = json.dumps(data).encode('utf-8')

rospy.init_node('alarm_msg_publisher')
pub = rospy.Publisher('alarm_msg', AlarmMsg, queue_size=10)

rate = rospy.Rate(10)

while not rospy.is_shutdown():
    clear_prev_alarm = 0
    alarm_triggered = False
    try:
        client_socket.sendall(json_data)
        received_data = client_socket.recv(1024)
        
    except socket.timeout:
        print("Socket timeout occurred!")
        client_socket.close()
        exit(1)

    except socket.error as e:
        print("Socket error:", str(e))
        client_socket.close()
        exit(1)

    try:
        json_response = json.loads(received_data.decode('utf-8'))
        query_data = json_response['queryData']
        alarm = query_data[0]

        alarm_msg = AlarmMsg()
        alarm_msg.header.stamp = rospy.Time.now()
        alarm_msg.alarm = alarm

        if alarm_triggered == False and alarm_msg.alarm != "0":

            if alarm_msg.alarm != prev_alarm_msg:
                alarm_triggered = True
                start_time = time.time()

                pub.publish(alarm_msg)          
                rospy.loginfo(alarm_msg)
                print("Message Published.")
                #alarm_triggered = False

            if (time.time() - start_time) > 5:
                alarm_triggered = False
                #prev_alarm_msg = None
                clear_prev_alarm = 1 
                start_time = time.time()
                print("Timeout, Alarm Reset.") 

            else:
                print (alarm_msg.alarm)
                print("Message NOT Published.")
                #rospy.loginfo(alarm_msg)    


    except Exception as e:
        rospy.logerr(f"An error occurred: {e}")

    prev_alarm_msg = alarm_msg.alarm
    if clear_prev_alarm == 1:
        prev_alarm_msg = None
        
    rate.sleep()

client_socket.close()