import BlynkLib
from BlynkTimer import BlynkTimer
import serial.tools.list_ports
import time
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import sleep
import threading

global br
global com

br = 9600
com = "/dev/ttyACM0"

flag = 0

fig = plt.figure(facecolor='k')
fig.canvas.toolbar.pack_forget()
fig.canvas.manager.set_window_title('Lidar Radar Plot')
mng = plt.get_current_fig_manager()
#mng.window.state('zoomed')
ax = fig.add_subplot(1, 1, 1, polar=True, facecolor='#006b70')
ax.tick_params(axis='both', colors='w')
r_max = 100.0
ax.set_ylim([0.0, r_max])
ax.set_xlim([0.0, np.pi])
ax.set_position([-0.05, -0.05, 1.1, 1.05])
ax.set_rticks(np.linspace(0.0,r_max,5))
ax.set_thetagrids(np.linspace(0,180,10))
ax.grid(color='w', alpha=0.4)

angles = np.arange(0, 181, 1)
theta = angles * (np.pi/180.0)

pols, = ax.plot([], linestyle='', marker='o', markerfacecolor='r', markeredgecolor='w', markeredgewidth=1.0, markersize=3.0, alpha=0.9)
line1, = ax.plot([], color='w', linewidth=4.0)

fig.canvas.draw()
dists = np.ones((len(angles),))
fig.show()
fig.canvas.blit(ax.bbox)
fig.canvas.flush_events()
axbackground = fig.canvas.copy_from_bbox(ax.bbox)

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial(com,br)
serialInst.flush()

first_data_printed = False
last_print_time = time.time()
x = 0

BLYNK_AUTH_TOKEN = 'cUixGCQqeh8F1_vDaM8EcXUqm3jy73Om'
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)
timer = BlynkTimer()

thread = threading.Thread(target=sleep.cv)
thread.start()

@blynk.on("connected")
def blynk_connected():
    print("You have Connected to New Blynk2.0")

@blynk.on("V2")
def v3_write_handler(value):
    print('Current slider value: {}'.format(value[0]))


def prog():
    blynk.run()

    global first_data_printed
    global last_print_time
    global x

    if serialInst.in_waiting > 0:
        data = serialInst.readline()
        decoded = data.decode()
        packet = (decoded.replace('\r', '')).replace('\n', '')
        vals = [float(ii) for ii in packet.split(',')]
        angle, dist = vals

        dists[int(angle)] = dist
        pols.set_data(theta,dists)
        fig.canvas.restore_region(axbackground)
        ax.draw_artist(pols)
        line1.set_data(np.repeat((angle * (np.pi/180)), 2),
                       np.linspace(0.0, r_max, 2))
        ax.draw_artist(line1)
        fig.canvas.blit(ax.bbox)
        fig.canvas.flush_events()

        if not first_data_printed:
            if ((angle is not None) and (dist is not None)):
                print("Angle = ", angle, "  Distance = ", dist, "CM")
                blynk.virtual_write(0, angle)
                blynk.virtual_write(1, dist)
                print("Values sent to New Blynk Server!")
            else:
                print("Sensor failure. Check wiring.")
            first_data_printed = True

        else:
            current_time = time.time()
            if True:
                if ((angle is not None) and (dist is not None)):
                    print("Angle = ", angle, "  Distance = ", dist, "CM")
                    blynk.virtual_write(0, angle)
                    blynk.virtual_write(1, dist)
                    x += 1
                    if (dist<30):    
                        blynk.virtual_write(2,1)
                    else:
                        blynk.virtual_write(2,0)
                    print("Values sent to New Blynk Server!")
                    if x >= 20:
                        x = 0
                        raise ValueError("Restart Error")
    
                else:
                    print("Sensor failure. Check wiring.")
                last_print_time = current_time

def close_figure(event):
    if event.key == 'q':
        global flag
        plt.close('all')
        flag = 1
        
if __name__ == "__main__":
    while True:
        try:
            #IoT with local Plotting
            prog()
            fig.canvas.mpl_connect('key_press_event', close_figure)
            if flag == 1:
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Restarting program...")
            # time.sleep(0.1)

            ports = serial.tools.list_ports.comports()
            serialInst = serial.Serial(com,br)
            serialInst.flush()
            first_data_printed = False
            last_print_time = time.time()
