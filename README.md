## IOT Konker demonstration
This project is a simple simulation of a iot application with the konker platform using the mqtt protocol for communication.

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
