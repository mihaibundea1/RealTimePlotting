from typing import Union

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import numpy as np
import serial as sr
from time import sleep
from serial import Serial

data = np.array([])
cond = False
s = sr.Serial()

delay = 1

try:
    s = sr.Serial(
        port="COM4",
        baudrate=115200
    )
    print("connected to:" + s.portstr)
except ValueError:
    print("Error setting up serial")


def plot_data():
    global cond, data, highest, lowest
    if (cond == True):
        a= s.readline()
        a.decode()

        if len(data) < 100:
            data = np.append(data, float(a[0:4]))
        else:
            data[0:99] = data[1:100]
            data[99] = float(a[0:4])
        lines.set_xdata(np.arange(0, len(data), dtype=int))
        lines.set_ydata(data)

        canvas.draw()

    root.after(1, plot_data)

def plot_start():
    global cond
    cond = True
    s.reset_input_buffer()


def plot_stop():
    global cond
    cond = False


root = tk.Tk()
root.title("RealTimePlot")
root.configure(background="light blue")
root.geometry("900x600")

fig = Figure()
ax = fig.add_subplot(111)

ax.set_title("Temperature Sensor")
ax.set_xlabel("Time")
ax.set_ylabel("Temperature (Time)")
ax.set_xlim(0, 100)
ax.set_ylim(10, 35)
lines = ax.plot([], [])[0]

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(x=10, y=10, width=600, height=400)
canvas.draw()

root.update();
start = tk.Button(root, text="Start", command=lambda: plot_start())
start.place(x=100, y=500)

root.update()
stop = tk.Button(root, text="Stop", command=lambda: plot_stop())
stop.place(x=start.winfo_x() + start.winfo_reqwidth() + 20, y=500)

s.reset_input_buffer()
root.after(1, plot_data)
root.mainloop()
