#!/usr/bin/env python

import rospy
# from msg_pkg.msg import AlarmMsg
#from robot_data_display.msg import AlarmMsg
from nc_crimp.msg import AlarmMsg
from telegram import Bot
from telegram.error import TelegramError
# from robot_data_display.msg import CounterMsg
# from robot_data_display.msg import CurrentModeMsg
import tracemalloc
import asyncio
from datetime import datetime, time

# Replace 'YOUR_BOT_TOKEN' with your actual Telegram Bot API token
TELEGRAM_BOT_TOKEN = '6427503877:AAHg5Th8BrJianple8NoqdPAZgbcSoSf1Oc'
CHAT_ID = '-4025128663'

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

    if alarm_value == 9000:
        error_msg = "Part drop while picking from left jig"

    elif alarm_value == 9001:
        error_msg = "Part drop while picking from right jig"

    elif alarm_value == 9002:
        error_msg = "Part Missing from Stamping Machine"
    
    elif alarm_value == 9003:
        error_msg = "Part drop after picking from Stamping Machine"
    
    elif alarm_value == 9004:
        error_msg = "Part stuck when unloading to basket"

    elif alarm_value == 9005:
        error_msg = "Part load to Stamping Machine Failed"

    elif alarm_value == 9006:
        error_msg = "Not in AUTO mode"

    elif alarm_value == 9007:
        error_msg = "Stamp Trigger Error"

    elif alarm_value == 9008:
        error_msg = "Pusher Unload Failed"

    elif alarm_value == 9009:
        error_msg = "Pusher Load Failed"

    elif alarm_value == 9010:
        error_msg = "Part drop while placing into Stamping Machine"

    elif alarm_value == 9011:
        error_msg = "Part Present Error"

    elif alarm_value == 9012:
        error_msg = "Part Present Error Dangerous"

    elif alarm_value == 9013:
        error_msg = "Robot Not at Home Position"
    
    elif alarm_value == 7:
        error_msg = "Emergency Stop"

    else:
        error_msg = "Error not recorded, check user manual."

   # timestamps = int(msg.header.stamp.nsecs + msg.header.stamp.secs)
    #datetime.fromtimestamp(timestamps).date()

    if msg.alarm != "0" and msg.alarm !="42":
        asyncio.run(send_telegram_message(msg.alarm + '\n' + error_msg))
        
        #rospy.loginfo(msg.alarm + '\n' + error_msg)
         
if __name__ == '__main__':
    rospy.init_node('alarm_msg_listener')  # Initialize the ROS node
    rospy.Subscriber('alarm_msg', AlarmMsg, alarm_callback)  # Create the subscriber

    rospy.spin()
