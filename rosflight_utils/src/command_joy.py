#!/usr/bin/env python3

# author: James Jackson

import time
import rospy
from rosflight_msgs.msg import Command
import pygame
import re
import os

os.environ["SDL_VIDEODRIVER"] = "dummy"

rospy.init_node('command_joy')
command_pub = rospy.Publisher('command', Command, queue_size=10)

pygame.display.init()
pygame.joystick.init()

joy = pygame.joystick.Joystick(0)
joy.init()

print("joystick:", joy.get_name())

mapping = dict()

if 'Taranis' in joy.get_name():
    print("found Taranis")
    mapping['x'] = 0
    mapping['y'] = 1
    mapping['z'] = 3
    mapping['F'] = 2
    mapping['xsign'] = 1
    mapping['ysign'] = 1
    mapping['zsign'] = 1
    mapping['Fsign'] = 1
elif 'Xbox' in joy.get_name() or 'X-Box' in joy.get_name():
    print("found xbox")
    mapping['x'] = 3
    mapping['y'] = 4
    mapping['z'] = 0
    mapping['F'] = 1
    mapping['xsign'] = 1
    mapping['ysign'] = 1
    mapping['zsign'] = 1
    mapping['Fsign'] = -1
else:
    print("using realflght mapping")
    mapping['x'] = 1
    mapping['y'] = 2
    mapping['z'] = 4
    mapping['F'] = 0
    mapping['xsign'] = 1
    mapping['ysign'] = 1
    mapping['zsign'] = 1
    mapping['Fsign'] = 1

# Main event loop
next_update_time = time.time()
while not rospy.is_shutdown():
    pygame.event.pump()

    # 50 Hz update
    if time.time() > next_update_time:
        next_update_time += 0.02

        msg = Command()
        msg.header.stamp = rospy.Time.now()

        msg.mode = 2

        msg.x = joy.get_axis(mapping['x']) * mapping['xsign'] * 0.785
        msg.y = joy.get_axis(mapping['y']) * mapping['ysign'] * 0.785
        msg.z = joy.get_axis(mapping['z']) * mapping['zsign'] * 1.507
        msg.F = joy.get_axis(mapping['F']) * mapping['Fsign'] * 0.5 + 0.5

        msg.ignore = 0
        command_pub.publish(msg)
