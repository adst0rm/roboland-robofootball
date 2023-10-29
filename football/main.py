#!/usr/bin/env pybricks-micropython
#фулл код для робофутбол - вратарь

___author___ = "Ergen Adil"


from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import print, wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


import struct

# Declare motors 
left_motor = Motor(Port.B) # передний рулевой
right_motor = Motor(Port.C) # задний правый
steer_motor = Motor(Port.A) # зданий левый
kicker_motor = Motor(Port.D) 
forward = 0
left = 0
ev3 = EV3Brick()
running = True


# Начало работы
ev3.speaker.beep()
# steer_motor.run_until_stalled(250)
# steer_motor.reset_angle(80)
# steer_motor.run_target(300,0)


# A helper function for converting stick values (0 - 255)
# to more usable numbers (-100 - 100)
def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
 
    val: float or int
    src: tuple
    dst: tuple
 
    example: print(scale(99, (0.0, 99.0), (-1.0, +1.0)))
    """
    return (float(val-src[0]) / (src[1]-src[0])) * (dst[1]-dst[0])+dst[0]


# Open the Gamepad event file:
# /dev/input/event3 is for PS3 gamepad
# /dev/input/event4 is for PS4 gamepad
# look at contents of /proc/bus/input/devices if either one of them doesn't work.
# use 'cat /proc/bus/input/devices' and look for the event file.
infile_path = "/dev/input/event4"

# open file in binary mode
in_file = open(infile_path, "rb")

# Read from the file
# long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'    
EVENT_SIZE = struct.calcsize(FORMAT)
event = in_file.read(EVENT_SIZE)
while running:
    while event:
        (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)
        if ev_type == 1: # A button was pressed or released.
            if code == 305:
                ev3.light.on(Color.RED)
            if code == 307:
                ev3.light.off()
            if code == 312:
                print("X button is pressed. Stopping.")
                running = False
                ev3.wait(2000) # Wait for the motor thread to finish
                break
            if code == 313:
                print("X button is pressed. Stopping.")
                running = True
                ev3.wait(2000) # Wait for the motor thread to finish
                break

            
            
        elif ev_type == 3: # Stick was moved
            if code == 0: 
                left = scale(value, (0,255), (100, -100))
            if code == 4: # Righ stick vertical
                forward = scale(value, (0,255), (-100,100))
            if code == 3:
                kicker = scale(value, (0,255), (-100,100))


        
        
    # Меняет направление
        left_motor.dc(left)
        right_motor.dc(left)
        
    # Вперед - назад
        steer_motor.dc(forward)
        right_motor.dc(-forward)

    # Кикер
        kicker_motor.dc(kicker)

    # Finally, read another event
        event = in_file.read(EVENT_SIZE)



    
     





in_file.close()