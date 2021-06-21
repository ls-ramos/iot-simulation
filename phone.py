from json import decoder
from threading import Thread
import paho.mqtt.client as mqtt
import json
import signal

from credentials import devices

# Config stop waiting for input when notification arrives
def interrupted(signum, frame):
    raise EOFError

signal.signal(signal.SIGALRM, interrupted)

def read_input(string):
    try:
            inp = input(string)
            return inp
    except:
            # timeout
            return -1


request_user_action = False

class Notification(Thread):
    def __init__ (self):
        Thread.__init__(self)

    # Presence state
    def on_connect_notification(self, client, userdata, flags, rc):
        client.subscribe("data/"+devices["phone"]["username"]+"/sub/request")
    
    def on_message(self, client, data, msg):
        msg_json = json.loads(msg.payload)
        should_turn_on = msg_json['should_turn_on']
        
        global request_user_action
        request_user_action = should_turn_on
        if should_turn_on == True:
            signal.alarm(1)
    
    def run(self):
        notification_client = mqtt.Client()
        notification_client.on_message = self.on_message
        notification_client.on_connect = self.on_connect_notification
        notification_client.username_pw_set(devices["phone"]["username"], devices["phone"]["password"])
        notification_client.connect("mqtt.prod.konkerlabs.net", 1883)
        notification_client.loop_forever()

notification = Notification()
notification.daemon = True # thread should stop when main thread stops
notification.start()

phone_client = mqtt.Client()
phone_client.username_pw_set(devices["phone"]["username"], devices["phone"]["password"])
phone_client.connect("mqtt.prod.konkerlabs.net", 1883)

presence_client = mqtt.Client()
presence_client.username_pw_set(devices["presence"]["username"],devices["presence"]["password"])
presence_client.connect("mqtt.prod.konkerlabs.net", 1883)

# Inicial state
phone_client.publish("data/"+devices["phone"]["username"]+"/pub/lamp", json.dumps({"is_lamp_on": True}))
phone_client.publish("data/"+devices["phone"]["username"]+"/pub/robot", json.dumps({"is_robot_on": False}))
presence_client.publish("data/"+devices["presence"]["username"]+"/pub/sensor", json.dumps({"is_present": True}))

while True:
    if request_user_action == True:
        print("You left the house and your cleaning robot is off.")
        inp = input("Would you like to turn it on ? (1-Yes/0-No): ")
        command = int(inp)
        print("\n\n")

        allow_client = mqtt.Client()
        allow_client.username_pw_set(devices["phone"]["username"], devices["phone"]["password"])
        allow_client.connect("mqtt.prod.konkerlabs.net", 1883)
    
        if command == 1:
            allow_client.publish("data/"+devices["phone"]["username"]+"/pub/robot", json.dumps({"is_robot_on": True}))
        
        allow_client.publish("data/"+devices["phone"]["username"]+"/pub/ask", json.dumps({"should_turn_on": False}))
        request_user_action = False

    print("Which action would like to perform ?\n"
    +"(Phone_Action) 1 - Turn on lights\n"
    +"(Phone_Action) 2 - Turn off lights\n"
    +"(Phone_Action) 3 - Turn on robot\n"
    +"(Phone_Action) 4 - Turn off robot\n"
    +"(Physical_Action) 5 - Enter the house\n"
    +"(Physical_Action) 6 - Leave the house\n"
    +"0 - Close\n")
    inp = read_input("Type the number of the action: ")
    command = int(inp)
    signal.alarm(0)

    if command == 1:    
        phone_client.publish("data/"+devices["phone"]["username"]+"/pub/lamp", json.dumps({"is_lamp_on": True}))
    elif command == 2:
        phone_client.publish("data/"+devices["phone"]["username"]+"/pub/lamp", json.dumps({"is_lamp_on": False}))
    elif command == 3:
        phone_client.publish("data/"+devices["phone"]["username"]+"/pub/robot", json.dumps({"is_robot_on": True}))
    elif command == 4:
        phone_client.publish("data/"+devices["phone"]["username"]+"/pub/robot", json.dumps({"is_robot_on": False}))
    elif command == 5:
        presence_client.publish("data/"+devices["presence"]["username"]+"/pub/sensor", json.dumps({"is_present": True}))
    elif command == 6:
        presence_client.publish("data/"+devices["presence"]["username"]+"/pub/sensor", json.dumps({"is_present": False}))
    elif command == -1:
        pass # ignore this command probably came from notification
    elif command == 0:
        break
    else:
        print("Invalid action, try again...\n")
    print("\n\n")



