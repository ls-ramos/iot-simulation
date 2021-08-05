## IOT Konker demonstration
This project is a simulation of a iot application with the konker platform using the mqtt protocol for communication.

In this project, the simulated scenario is a smart house where the user can control the lights and the house cleaning robot with his phone. It is also simulated that the house has a presence sensor that can tell if the user is in the house or not (the phone could also be used for this, but in this simulation the presence sensor was modeled as another device). With these sensors the app also turns off the lights automatically for the user if he leaves the house with the lights on and also if the cleaning robot is turned off when the user leaves the house, the app notifies the user asking if he wants to turn on the robot.

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
This project was presented as the final project of my computer engineering graduation and this simulation was used to write a paper about IoT simulations

## The konker plataform
### Hosted plataform
You can access the hosted konker plataform in the link https://www.konkerlabs.com/ 

### Running locally
You can also run konker locally getting the konker docker image https://hub.docker.com/r/konkerlabs/konker-platform/ (This is recommended because of simplicity of configuration)

But you can also get the project on github https://github.com/KonkerLabs/konker-platform and configure the environment yourself
