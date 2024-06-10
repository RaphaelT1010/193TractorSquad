# Getting Started

This is the main repository for our robotic dummy platform and mobile app which is used for the autonomous tractor safety research project. This repo exists as what progress
we have done for our undergraduate senior capstone project during the 2024 Winter and Spring quarters. Due to the complexity and nature of the project, there will be some old
code laying around in the repo, which we kept for documentation purposes to highlight our progress. This repo can be continued from either directly or by copying its contents
for future development. Therefore, we consider this project, code, and documentation to be a living repository. All code and rights belong to Farzaneh Khorsandi, Ph.D and her lab.

This ReadMe file will explain specific code and versions that you will need to run and continue the project. Do note that this contains separate configuration for the Raspberry Pi
which controls the robot and configuration for the mobile app which sends signals to the Raspberry Pi. The Mobile app directory will have its own ReadMe for documentation, startup,
and use instructions and procedures.

# Python Versions and Raspberry Pi Setup
All Raspberry Pi code was developed in python. The versions of python that we used were: Python 3.7. As well, some libraries may have to be installed on the Raspberry Pi so that
the code can use different APIs and functions. The original SD card on the Raspberry Pi should have everything setup, however. This includes correct python versions, all relevant python libaries,
the peripheral name of the Raspberry Pi as seen on Bluetooth, SSH and VNC is enabled, and Bluetooth Low Energy is enabled. Regarding the peripheral name, we have named the Raspberry Pi as
"tractorsquad" and on Bluetooth scanning, the Pi will appear with that name. The mobile app to control the robot will *only* detect Bluetooth peripherals with the name "tractorsquad" unless
the build is changed to look for any other name. Keep this in mind in case you use a different Pi, change the app code, change the Pi name, or anything similar.

# Directories To Use
There are a lot of files and code that we have developed over the two quarters that this project was built in. A lot of this configuration is old and outdated, but we kept it in for documentation purposes.
This section is to describe what directories and files should be used to control the robot and continue development configuration.

## Bluetooth Configuration Files
The exact Bluetooth files that we have developed are located in the following directory: "193TractorSquad -> project -> bluetooth -> periph2". Specifically, we use the following python files:
- peripheral_main.py
- application.py
- service.py
- exceptions.py
- advertisement.py

Our driver files depend on these for proper Bluetooth connection, so it is advised to have all of them in the same directory. If making a project and using a differently named directory, ensure
that all includes in the following driver files and in the above files are named accordingly. Failure to do so may prevent the program from working.

## All Bluetooth and GPS Drivers
We consider all code in the following directory to be necessary to run the robot: "193TractorSquad -> project -> bluetooth_arduino_driver". Despite the name, no Arduino is used in this configuration. The
hardware that should be used are:
- The Raspberry Pi with correct SD card with development code
- The GPS module connected onto GPIO pins
- The IMU connected onto GPIO pins
- The Motor Controller connected onto GPIO pins
- The Robot platform itself

Additionally, the following code files that you will need in the "bluetooth_arduino_driver directory" are:
- adafruit_ultimate_gps.py
- gps_driver.py
- gps_movement.py
- motor.py
- simple_movement_driver.py
- test_com_arduino.py
- test_gps.py
- test_motors.py

While the test files may not be entirely necessary, they do contain important development progress.

## Other files
Any other files/directories not mentioned previously are considered old and obsolete. We have checked that the files needed to operate the robot do not depend on the other old code.
However, in any unlikely event that this is the case, it would be advisable to download/install the entire project onto the Pi and run it as is (excluding the mobile app directory).

## Running the Robot
The Robot uses two different programs to run. The original SD card contains a bash script that runs these two programs upon Pi startup. However, in the event that the bash script does not work, 
running the "peripheral_main.py" script and then "simple_movement_driver.py" script should open up both the bluetooth and all movement capabilities for the robot.

# Movement speed
Currently, the speed on the motors are fixed. However, we had plans to allow for a change in speeds. This would be easy to implement, but we had no time remaining. This would be a control on the app
using either a slider or preset buttons, and it would alter the movement speed of the motors that the Pi uses in its program. The values for the motors do not represent speed or power, but probably
some other variable. To view the values, please look at the "motor.py" file located in "193TractorSquad -> project -> bluetooth_arduino_driver". These were calibrated to ensure the motors would run the same
speed when moving forward and backward. As well, these were calibrated so that the robot could correctly turn left or right.

# Issues/Errors
There can be a lot of issues and dependencies. To make sure you have the correct dependency versions, we suggest consulting the original SD card for its proper python libraries installed and python versions.
If not found, the proper python versions are: 3.7

Another thing to note, a lot of Raspberry Pi configuration was made to allow SSH/VNC and Bluetooth. If a new Pi is used, this will have to be reset again if the features are needed. Let us know if you have any other errors.

