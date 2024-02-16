"""
This script shows a simple scripted flight path using the MotionCommander class.

Simple example that connects to the crazyflie at `URI` and runs a
sequence. Change the URI variable to your Crazyflie configuration.
"""
import logging
import time

import numpy as np
from matplotlib import pyplot as plt

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

# ****************************************************************
# The following libraries are needed for logging data while flying
# ****************************************************************
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
# ****************************************************************


# *************** URI Link to Connect to CrazyFlie ******************
#URI = 'radio://0/80/250K'
#uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')
#URI = 'radio://0/80/2M'
#URI = 'radio://0/80/2M/E7E7E7E7E7'
#URI = 'radio://0/100/2M/E7E7E7E702'   # Office Drone 1
URI = 'radio://0/100/2M/E7E7E7E705'  # ENEE4350 Drone 1
# *******************************************************************


# A variable that will be used in main program to start logging
is_deck_attached = True

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# Initializing the x, y, z, roll, pitch, and yaw position variable
position_estimate = [0, 0, 0, 0, 0, 0]

#  Initializing numpy array to store logs
array = []
yarray = []
tarray = []

logging_period = 200


# *******************************************************************
# Defining the step-by-step movements as a funcion to run the Crazyflie 
# *******************************************************************
# Default height for the Crzyflie to hover
DEFAULT_HEIGHT = 0.5

def move_simple(scf):
    with MotionCommander(scf, default_height=DEFAULT_HEIGHT) as mc:
        time.sleep(1)
        
        print('Moving forward 4m')
        mc.forward(2)
        time.sleep(2)
        
        print('Turning left 180 degrees')
        mc.turn_left(180)
        time.sleep(2)
        
        print('Moving forward 0.5m')
        mc.forward(.5)
        time.sleep(2)
        
        print('Moving up by 0.2m')
        mc.up(0.5)
        time.sleep(4)
        
        print('Moving down by 0.2m')
        mc.down(0.5)
        time.sleep(2)
        
        #print('Rolling left 0.2m at 0.6m/s')   
        #mc.left(0.2, velocity=0.6)
        # Wait a bit
        #time.sleep(1)
        
        # We land when the MotionCommander goes out of scope
        print('Landing!')
# *******************************************************************        


def take_off_simple(scf):
    ...


# ****************************************************************
# Assigning the x, y, z, roll, pitch, and yaw data to the variable 
# ****************************************************************
def log_pos_callback(timestamp, data, logconf):
    
    global position_estimate
    position_estimate[0] = data['stateEstimate.x']
    position_estimate[1] = data['stateEstimate.y']
    position_estimate[2] = data['stateEstimate.z']
    position_estimate[3] = data['stateEstimate.roll']
    position_estimate[4] = data['stateEstimate.pitch']
    position_estimate[5] = data['stateEstimate.yaw']
    array.append(data['stateEstimate.x'])
    yarray.append(data['stateEstimate.y'])
    

# ****************************************************************


def param_deck_flow(name, value_str):
    ...


if __name__ == '__main__':
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        time.sleep(1)

        logconf = LogConfig(name='Position', period_in_ms=logging_period)
        logconf.add_variable('stateEstimate.x', 'float')
        logconf.add_variable('stateEstimate.y', 'float')
        logconf.add_variable('stateEstimate.z', 'float')
        logconf.add_variable('stateEstimate.roll', 'float')
        logconf.add_variable('stateEstimate.pitch', 'float')
        logconf.add_variable('stateEstimate.yaw', 'float')

        scf.cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_pos_callback)

        if is_deck_attached:
            logconf.start()

            move_simple(scf)
            logconf.stop()

            #for i in range(len(array)):
                #i *= logging_period/1000
                #tarray.append(i)

            #plt.plot(tarray, array)
            #plt.ylabel('X-axis')
            #plt.xlabel('time')
            #plt.show()

