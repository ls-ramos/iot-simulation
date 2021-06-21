from threading import Thread
import paho.mqtt.client as mqtt
import json

from credentials import devices

lamp_state = False
robot_state = False
presence_state = False

state_map = {False: "off", True: "on"}

def print_states():
    print("LAMP = "+state_map[lamp_state]+"  /  "+"ROBOT = "+state_map[robot_state]+"  /  "+"PRESENCE = "+state_map[presence_state]+"\n")

class Lamp(Thread):
    def __init__ (self):
        Thread.__init__(self)

    # Lamp state
    def on_connect_lamp(self, client, userdata, flags, rc):
        print("Connected Lamp")
        client.subscribe("data/"+devices["lamp"]["username"]+"/sub/state")

    def on_message(self, client, data, msg):
        global lamp_state
        msg_json = json.loads(msg.payload)
        lamp_state = msg_json['is_lamp_on']
        print_states()

    def run(self):
        lamp_client = mqtt.Client()
        lamp_client.on_message = self.on_message
        lamp_client.on_connect = self.on_connect_lamp
        lamp_client.username_pw_set(devices["lamp"]["username"], devices["lamp"]["password"])
        lamp_client.connect("mqtt.prod.konkerlabs.net", 1883)
        lamp_client.loop_forever()

class Robot(Thread):
    def __init__ (self):
        Thread.__init__(self)

    # Robot state
    def on_connect_robot(self, client, userdata, flags, rc):
        print("Connected Robot")
        client.subscribe("data/"+devices["robot"]["username"]+"/sub/state")

    def on_message(self, client, data, msg):
        global robot_state
        msg_json = json.loads(msg.payload)
        robot_state = msg_json['is_robot_on']
        print_states()

    def run(self):
        robot_client = mqtt.Client()
        robot_client.on_message = self.on_message
        robot_client.on_connect = self.on_connect_robot
        robot_client.username_pw_set(devices["robot"]["username"], devices["robot"]["password"])
        robot_client.connect("mqtt.prod.konkerlabs.net", 1883)
        robot_client.loop_forever()

class PresenceSensor(Thread):
    def __init__ (self):
        Thread.__init__(self)

    # Presence state
    def on_connect_presence(self, client, userdata, flags, rc):
        print("Connected Presence Sensor")
        client.subscribe("data/"+devices["presence"]["username"]+"/sub/state")
    
    def on_message(self, client, data, msg):
        global presence_state
        msg_json = json.loads(msg.payload)
        presence_state = msg_json['is_present']
        print_states()

    def run(self):
        presence_client = mqtt.Client()
        presence_client.on_message = self.on_message
        presence_client.on_connect = self.on_connect_presence
        presence_client.username_pw_set(devices["presence"]["username"], devices["presence"]["password"])
        presence_client.connect("mqtt.prod.konkerlabs.net", 1883)
        presence_client.loop_forever()

class Notification(Thread):
    def __init__ (self):
        Thread.__init__(self)

    # Presence state
    def on_connect_notification(self, client, userdata, flags, rc):
        print("Connected Notification")
        client.subscribe("data/"+devices["phone"]["username"]+"/sub/notification")
    
    def on_message(self, client, data, msg):
        msg_json = json.loads(msg.payload)
        is_present = msg_json['is_present']
        
        global lamp_state
        if is_present == False and lamp_state == True:
            print("Automatically turning off lights...")
            phone_client = mqtt.Client()
            phone_client.username_pw_set(devices["phone"]["username"], devices["phone"]["password"])
            phone_client.connect("mqtt.prod.konkerlabs.net", 1883)
            phone_client.publish("data/"+devices["phone"]["username"]+"/pub/lamp", json.dumps({"is_lamp_on": False}))

        global robot_state
        if is_present == False and robot_state == False:
            print("Ask to turn on cleaning robot...")
            phone_client = mqtt.Client()
            phone_client.username_pw_set(devices["phone"]["username"], devices["phone"]["password"])
            phone_client.connect("mqtt.prod.konkerlabs.net", 1883)
            phone_client.publish("data/"+devices["phone"]["username"]+"/pub/ask", json.dumps({"should_turn_on": True}))
            

    def run(self):
        notification_client = mqtt.Client()
        notification_client.on_message = self.on_message
        notification_client.on_connect = self.on_connect_notification
        notification_client.username_pw_set(devices["phone"]["username"], devices["phone"]["password"])
        notification_client.connect("mqtt.prod.konkerlabs.net", 1883)
        notification_client.loop_forever()

lamp = Lamp()
lamp.start()

robot = Robot()
robot.start()

presence = PresenceSensor()
presence.start()

notification = Notification()
notification.start()