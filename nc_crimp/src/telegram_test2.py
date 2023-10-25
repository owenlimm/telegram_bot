#!/usr/bin/env python

import rospy
# from msg_pkg.msg import AlarmMsg
from robot_data_display.msg import AlarmMsg
#from nc_crimp.msg import AlarmMsg
from telegram import Bot
from telegram.error import TelegramError
# from robot_data_display.msg import CounterMsg
# from robot_data_display.msg import CurrentModeMsg
import tracemalloc
import asyncio
from datetime import datetime, time
from alarm_enum import Alarm

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot API token
TELEGRAM_BOT_TOKEN = '6427503877:AAHg5Th8BrJianple8NoqdPAZgbcSoSf1Oc'
CHAT_ID = '-4025128663'

print ("telegram bot running...")

async def send_telegram_message(msg_text):
    tracemalloc.start()

    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=msg_text)
    except TelegramError as e:
        rospy.logerr(f"Failed to send Telegram message: {e}")

    tracemalloc.stop()

def alarm_callback(msg):    
    message = f"Received Robot Message:\n{msg}"
    #rospy.loginfo(message)

    alarm_value = int(msg.alarm)

    if alarm_value in [e.value for e in Alarm]:
        # Use the Alarm enum to get the error message
        error_msg = Alarm(alarm_value).name.replace("_", " ").title()
    else:
        error_msg = "Error not recorded, check user manual"

   # timestamps = int(msg.header.stamp.nsecs + msg.header.stamp.secs)
    #datetime.fromtimestamp(timestamps).date()

    if msg.alarm != "0" and msg.alarm !="42":
        asyncio.run(send_telegram_message(msg.alarm + '\n' + error_msg))
        
        rospy.loginfo(msg.alarm + '\n' + error_msg)
         
if __name__ == '__main__':
    rospy.init_node('alarm_msg_listener')  # Initialize the ROS node
    rospy.Subscriber('alarm_msg', AlarmMsg, alarm_callback)  # Create the subscriber

    rospy.spin()
