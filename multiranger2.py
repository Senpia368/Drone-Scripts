import logging
import sys
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander
from cflib.utils.multiranger import Multiranger
from cflib.crazyflie.log import LogConfig

URI = 'radio://0/100/2M/E7E7E7E705'

# A variable that will be used in main program to start logging
is_deck_attached = True

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# Initializing the x, y, z, roll, pitch, and yaw position variable
position_estimate = [0, 0, 0, 0, 0, 0]

x_data = []
y_data = []
z_data = []

def is_close(range):
    MIN_DISTANCE = 0.3  # m

    if range is None:
        return False
    else:
        return range < MIN_DISTANCE
    
def ranger(scf):
     with MotionCommander(scf) as motion_commander:
            with Multiranger(scf) as multiranger:
                keep_flying = True

                while keep_flying:
                    VELOCITY = 0.5
                    velocity_x = 0.0
                    velocity_y = 0.0

                    if is_close(multiranger.front):
                        velocity_x -= VELOCITY
                    if is_close(multiranger.back):
                        velocity_x += VELOCITY

                    if is_close(multiranger.left):
                        velocity_y -= VELOCITY
                    if is_close(multiranger.right):
                        velocity_y += VELOCITY

                    if is_close(multiranger.up):
                        keep_flying = False

                    motion_commander.start_linear_motion(
                        velocity_x, velocity_y, 0)

                    time.sleep(0.1)

            print('Demo terminated!')
    
def log_pos_callback(timestamp, data, logconf):
    print(data)
    global position_estimate
    position_estimate[0] = data['stateEstimate.x']
    position_estimate[1] = data['stateEstimate.y']
    position_estimate[2] = data['stateEstimate.z']
    position_estimate[3] = data['stateEstimate.roll']
    position_estimate[4] = data['stateEstimate.pitch']
    position_estimate[5] = data['stateEstimate.yaw']

    x_data.append(position_estimate[0])
    y_data.append(position_estimate[1])
    z_data.append(position_estimate[2])
# ****************************************************************

def param_deck_flow(name, value_str):
    ...

def take_off_simple(scf):
    ...

if __name__ == '__main__':
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:

        scf.cf.param.add_update_callback(group='deck', name='bcFlow2',
                                         cb=param_deck_flow)
        time.sleep(1)

        logconf = LogConfig(name='Position', period_in_ms=200)
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

            ranger(scf)
            logconf.stop()

    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()  
    ax = plt.axes(projection='3d')

    # Data for a three-dimensional line
    zline = np.linspace(0, 0.1, 2)
    xline = np.linspace(0, 0.1, 2)
    yline = np.linspace(0, 0.1, 2)
    ax.plot3D(xline, yline, zline, 'gray')

    # Data for three-dimensional scattered points
    zdata = z_data
    xdata = x_data
    ydata = y_data
    ax.scatter3D(xdata, ydata, zdata);
    ax.plot(xdata, ydata, zdata)
    plt.show()
    
