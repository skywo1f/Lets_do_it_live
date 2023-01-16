import time
import websocket
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create an empty list to store the coordinates
coords = []

def update_plot(x, y, z):
    # Add the new coordinates to the list
    coords.append((x, y, z))

    # Plot the coordinates in 3D
    ax.scatter([p[0] for p in coords], [p[1] for p in coords], [p[2] for p in coords], c='b', marker='o')
    ax.scatter(x, y, z, c='r', marker='o') # red dot for the most recent point

    # Update the plot
    plt.draw()
    plt.pause(0.0001)

def ask_words(ws,words):
    data = words
    print("sending message")
    ws.send(data)
    return ws.recv()

def calculate_coordinates(Bx, By, Bz, rx, ry, rz, L):
    # Create rotation matrices
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(rx), -np.sin(rx)],
                    [0, np.sin(rx), np.cos(rx)]])
    R_y = np.array([[np.cos(ry), 0, np.sin(ry)],
                    [0, 1, 0],
                    [-np.sin(ry), 0, np.cos(ry)]])
    R_z = np.array([[np.cos(rz), -np.sin(rz), 0],
                    [np.sin(rz), np.cos(rz), 0],
                    [0, 0, 1]])

    # Combine rotations
    R = R_z @ R_y @ R_x

    # Calculate coordinates
    Ax = Bx + L * R[0, 2]
    Ay = By + L * R[1, 2]
    Az = Bz + L * R[2, 2]

    return Ax, Ay, Az

ws = websocket.create_connection("ws://localhost:8080/MyWebSocket")

L = .2
while True:

    data = "message request"
    coordinate = ask_words(ws,data)
    print(coordinate)
    fdata = [float(x) for x in coordinate.split(',')]
    position = calculate_coordinates(fdata[0],fdata[1],fdata[2],fdata[3],fdata[4],fdata[5],L)
    angle = [fdata[3],fdata[4],fdata[5]]
    print(position, angle)
    update_plot(position[0], position[1],position[2])
    time.sleep(.1)
