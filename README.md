## IOT Konker demonstration
Smart Home IoT Simulation with Konker & MQTT

This project is a simulation of an IoT-based smart home application, leveraging the Konker IoT platform and the MQTT protocol for communication.

### Project Overview

The simulation models a smart home environment where a user can control key household devices remotely via a mobile phone. The core functionalities include:
	•	Smart Lighting Control: Users can turn lights on and off manually, and the system can automatically switch them off if the user leaves them on while exiting the house.
	•	Automated Cleaning Robot: Users can activate or deactivate a cleaning robot remotely. If the robot is off when the user leaves, the system sends a notification prompting them to turn it on.
	•	Presence Detection: A presence sensor determines whether the user is home or away. (In a real-world scenario, the user’s phone could serve as the presence detector, but for this simulation, it is modeled as a separate IoT device.)

The structure of the project in konker is:
![alt text](https://github.com/lucasR23/iot-simulation/blob/main/konkerStructure.png?raw=true)

## Run simulation
To run this simulation first install the dependencies:

    pip install -r requirements.txt

Run states.py - This program will show you the state of all sensors in the house

    python states.py

Run phone.py - This program simulates what would run on the phone of the user
    
    python phone.py

Now you can give inputs and see the state changes

It is important to note that in this simulation there is two programs for a better visualization in the terminal but in a real application all of this logic would be running on the phone of the user

## Crendentials
To add the credentials of your devices from the konker plataform you should create a file name credentials.py and add the data like the exemple bellow:

    server_url_mqtt = "mqtt.prod.konkerlabs.net"

    devices = {
        "phone": {
            "username": "KONKER_MQTT_USERNAME",
            "password": "KONKER_MQTT_PASSWORD",
            "pub": "data/KONKER_MQTT_USERNAME/pub/",
            "sub": "data/KONKER_MQTT_USERNAME/sub/"
        },
        "lamp": {
            "username": "KONKER_MQTT_USERNAME",
            "password": "KONKER_MQTT_PASSWORD",
            "pub": "data/KONKER_MQTT_USERNAME/pub/",
            "sub": "data/KONKER_MQTT_USERNAME/sub/"
        },
        "robot": {
            "username": "KONKER_MQTT_USERNAME",
            "password": "KONKER_MQTT_PASSWORD",
            "pub": "data/KONKER_MQTT_USERNAME/pub/",
            "sub": "data/KONKER_MQTT_USERNAME/sub/"
        },
        "presence": {
            "username": "KONKER_MQTT_USERNAME",
            "password": "KONKER_MQTT_PASSWORD",
            "pub": "data/KONKER_MQTT_USERNAME/pub/",
            "sub": "data/KONKER_MQTT_USERNAME/sub/"
        },
    }

The fields pub and sub are usually in the form "data/KONKER_MQTT_USERNAME/pub/" but if you are running konker locally it can be "pub/KONKER_MQTT_USERNAME/" just as the server_url_mqtt that can be "127.0.0.1" when running locally. To make easily this project easily interchangeble between running locally or not this data is stored in credentials.

## Goal
This simulation demonstrates an IoT-driven automation system that enhances convenience and energy efficiency. It showcases practical MQTT-based communication between devices and a cloud platform, making it a strong example of real-world IoT application development.

The simulation served as the basis for a research paper on IoT simulation scalability and bottlenecks, presented as the final project of my computer engineering graduation.

## The konker plataform
### Hosted plataform
You can access the hosted konker plataform in the link https://www.konkerlabs.com/ 

### Running locally
You can also run konker locally getting the konker docker image https://hub.docker.com/r/konkerlabs/konker-platform/ (This is recommended because of simplicity of configuration)

But you can also get the project on github https://github.com/KonkerLabs/konker-platform and configure the environment yourself
