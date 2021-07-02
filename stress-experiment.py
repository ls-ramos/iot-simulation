from threading import Thread
from time import sleep
import paho.mqtt.client as mqtt
import json
import time
import sys
import os
import argparse

from credentials import devices, server_url_mqtt
final_time = []

class HouseTest(Thread):
    def __init__(self, house_id, device_rate=1, request_num=1, wait=1, attempts=1, details=False):
        super(HouseTest, self).__init__()
        self.house_id = house_id
        self.device_rate = device_rate
        self.wait = wait
        self.attempts = attempts
        self.request_num = request_num
        self.request_time = {"lamp": [], "robot": [], "sensor": []}
        self.answer_time = {"lamp": [], "robot": [], "sensor": [] }
        self.details = details

    def run(self):
        phone_pub = DevicePubTest("phone", self.device_rate,self.request_num, self.house_id, self.request_time)
        presence_pub = DevicePubTest("presence", self.device_rate,self.request_num, self.house_id, self.request_time)
        lamp_sub = DeviceSubTest("lamp",self.house_id, self.answer_time)
        robot_sub = DeviceSubTest("robot",self.house_id, self.answer_time)
        presence_sub = DeviceSubTest("presence",self.house_id, self.answer_time, "sensor")

        lamp_sub.start()
        robot_sub.start()
        presence_sub.start()
        phone_pub.start()
        presence_pub.start()
        for count in range(self.attempts):
            if len(self.answer_time["lamp"]) == self.request_num and len(self.answer_time["robot"]) == self.request_num and len(self.answer_time["sensor"]) == self.request_num:
                break
            time.sleep(self.wait)

        if self.details:
            print("Request time FINAL:", self.request_time)
            print("Answer time FINAL:", self.answer_time)

        delay = {}
        avg = {}
        for key in self.request_time.keys():
            delay[key] = []
            avg[key] = 0
            for request, answer in zip(self.request_time[key], self.answer_time[key]):
                time_passed = answer - request
                delay[key].append(time_passed)
                avg[key] += time_passed
            if len(delay[key]) > 0:                
                avg[key] = avg[key] / len(delay[key])
            else:
                avg[key] = 0
        
        global final_time
        for key in delay:
            for re_time in delay[key]:
                if re_time > 0:
                    final_time.append(re_time)

        if self.details:
            print("Time of request:", delay)
        print("Avg time of request:", avg)

class DeviceSubTest(Thread):
    def __init__(self, name, house_id, answer_time, channel_name=None):
        super(DeviceSubTest, self).__init__()
        self.name = name
        if channel_name is None:
            self.channel_name = name
        else:
            self.channel_name = channel_name
        self.house_id = house_id
        self.answer_time = answer_time

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe(devices[self.name]["sub"]+devices[self.name]["subchannel"])

    def on_message(self, client, data, msg):
        msg_json = json.loads(msg.payload)
        test_id = msg_json['test']
        if test_id == self.house_id:
            self.answer_time[self.channel_name].append(time.time())

    def run(self):
        lamp_client = mqtt.Client()
        lamp_client.on_message = self.on_message
        lamp_client.on_connect = self.on_connect
        lamp_client.username_pw_set(devices[self.name]["username"], devices[self.name]["password"])
        lamp_client.connect(server_url_mqtt, 1883)
        lamp_client.loop_forever()

    def stop(self):
        sys.exit()
    
class DevicePubTest(Thread):
    def __init__(self, name,rate,request_num, house_id, request_time):
        super(DevicePubTest, self).__init__()
        self.name = name    
        self.rate = rate
        self.request_num = request_num
        self.house_id = house_id
        self.request_time = request_time
        

    def run(self):
        client = mqtt.Client()
        client.username_pw_set(devices[self.name]["username"], devices[self.name]["password"])
        client.connect(server_url_mqtt, 1883)
        
        device = devices[self.name]
        channels = device["pubchannel"]

        for count in range(self.request_num):
            for channel in channels:
                self.request_time[channel].append(time.time())
                client.publish(device["pub"]+channel, json.dumps({"test": self.house_id}))
            time.sleep(self.rate)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-n',
                        '--nhouses',
                        dest='house_num',
                        const=1,
                        default=1,
                        action='store',
                        nargs='?',
                        type=int,
                        help='Number of houses to be simulated')
    parser.add_argument('-r',
                        '--rate',
                        dest='device_rate',
                        const=1,
                        default=1,
                        action='store',
                        nargs='?',
                        type=float,
                        help='Update rate of the simulated devices in seconds')
    parser.add_argument('-re', 
                        '--requests',
                        dest='request_num',
                        const=1,
                        default=1,
                        action='store',
                        nargs='?',
                        type=int,
                        help='Number of request that each device will send')
    parser.add_argument('-w', 
                        '--wait',
                        dest='wait',
                        const=5,
                        default=5,
                        action='store',
                        nargs='?',
                        type=int,
                        help='How much time to wait for all devices send all the requests')
    parser.add_argument('-a', 
                        '--attempts',
                        dest='attempts',
                        const=1,
                        default=1,
                        action='store',
                        nargs='?',
                        type=int,
                        help='How many attempts to check if the devices are finished sending the requests')
    parser.add_argument('-d',
                        '--details',
                        dest='details',
                        const=True,
                        default=False,
                        action='store',
                        nargs='?',
                        type=bool,
                        help='Should show simulation details')
    args = parser.parse_args()
    for i in range(args.house_num):
        test = HouseTest(i, args.device_rate,args.request_num, args.wait,args.attempts, args.details)
        test.start()

    print("Running simulation...")
    
    while len(final_time)<args.house_num*3*args.request_num:
        time.sleep(15)

        sum = 0
        highest = 0
        avg_final = 0
        if len(final_time) > 0:
            for num in final_time:
                if num > highest:
                    highest = num
                sum += num
            avg_final = sum/len(final_time)

        print("AVG:", avg_final)
        print("Highest:", highest)


    os._exit(1) # not clean exit but works in this case...