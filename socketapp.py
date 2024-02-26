import tkinter as tk
import threading
import time
import bluetooth
import socket
import sys

global piIp
piIP = "192.168.1.176"
global receiverPort
piPort = 12345



def windowBoot():
    global window
    window = tk.Tk()
    window.title("Tractor Squad")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")

    global awaitingLabel
    awaitingLabel = tk.Label(window, font=("Arial", 20), text="Attempting to connect with Pi...")
    awaitingLabel.place(relx=0.5, rely=0.5, anchor="center")

    window.protocol("WM_DELETE_WINDOW", exitProcedure)
    window.mainloop()

def exitProcedure():
    window.quit()
    sys.exit()


def establishSocketConnection():
    try:
        global sender_socket
        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the receiver
        sender_socket.connect((piIP, piPort))
        awaitingLabel.config(text="Socket connection established")
        window.update()
        window.after(4000, startBluetoothControls)
    except Exception as e:
        awaitingLabel.config(text="Could not establish connection. Exiting...")
        window.update()
        window.after(4000, exitProcedure) 
    
   
def tryConnectingToPi():
    establishSocketConnection()

def setUpControlPanel():
    control_panel = tk.Frame(window)
    control_panel.place(relx=0.5, rely=0.5, anchor="center")
    
    # Define the common width and height for arrow buttons
    button_width = 3
    button_height = 1
    
    # Create and place the buttons
    up_arrow_button = tk.Button(control_panel, text="↑", font=("Arial", 50), command=moveUp, width=button_width, height=button_height)
    up_arrow_button.grid(row=0, column=1)
    
    left_arrow_button = tk.Button(control_panel, text="←", font=("Arial", 50), command=moveLeft, width=button_width, height=button_height)
    left_arrow_button.grid(row=1, column=0)
    
    down_arrow_button = tk.Button(control_panel, text="↓", font=("Arial", 50), command=moveDown, width=button_width, height=button_height)
    down_arrow_button.grid(row=1, column=1)
    
    right_arrow_button = tk.Button(control_panel, text="→", font=("Arial", 50), command=moveRight, width=button_width, height=button_height)
    right_arrow_button.grid(row=1, column=2)
    
    stop_button = tk.Button(control_panel, text="STOP", font=("Arial", 30), command=stopRobot)
    stop_button.grid(row=3, column=1, pady=(20, 0))


def startBluetoothControls():
    awaitingLabel.destroy()
    setUpControlPanel()
    
def moveUp():
    message = "Up"
    sender_socket.send(message.encode())

def moveLeft():
    message = "Left"
    sender_socket.send(message.encode())

def moveRight():
    message = "Right"
    sender_socket.send(message.encode())

def moveDown():
    message = "Down"
    sender_socket.send(message.encode())

def stopRobot():
    message = "Stop"
    sender_socket.send(message.encode())

def startWindowAndBluetooth():
    threading.Thread(target=windowBoot).start()
    tryConnectingToPi()

if __name__ == '__main__': 
    startWindowAndBluetooth()
