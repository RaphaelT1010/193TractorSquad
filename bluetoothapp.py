import tkinter as tk
import threading
import time
import bluetooth
import socket
import sys

def windowBoot():
    global window
    window = tk.Tk()
    window.title("Tractor Squad")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")

    global awaitingBluetoothLabel
    awaitingBluetoothLabel = tk.Label(window, font=("Arial", 25), text="Awaiting bluetooth connection...")
    awaitingBluetoothLabel.place(relx=0.5, rely=0.5, anchor="center")

    window.protocol("WM_DELETE_WINDOW", exitProcedure)
    window.mainloop()

def exitProcedure():
    window.quit()
    sys.exit()

def tryConnectingToPiWithBluetooth():
    #Replace target_mac_address with the raspberry pi's mac address
    targetMacAddress = "04:CF:4B:BB:D8:10"
    nearbyDevices = bluetooth.discover_devices()

    if targetMacAddress in nearbyDevices:
        awaitingBluetoothLabel.config(text="Bluetooth connection established")
        window.update()
        window.after(4000, startBluetoothControls)
    else:
        awaitingBluetoothLabel.config(text="Could not find device")
        window.update()
        window.after(4000, exitProcedure)

def setUpControlPanel():
    control_panel = tk.Frame(window)
    control_panel.place(relx=0.5, rely=0.5, anchor="center")
    up_arrow_button = tk.Button(control_panel, text="↑", font=("Arial", 50), command=moveUp)
    up_arrow_button.grid(row=0, column=1)
    left_arrow_button = tk.Button(control_panel, text="←", font=("Arial", 50), command=moveLeft)
    left_arrow_button.grid(row=1, column=0)
    right_arrow_button = tk.Button(control_panel, text="→", font=("Arial", 50), command=moveRight)
    right_arrow_button.grid(row=1, column=2)
    down_arrow_button = tk.Button(control_panel, text="↓", font=("Arial", 50), command=moveDown)
    down_arrow_button.grid(row=2, column=1)
    stop_button = tk.Button(control_panel, text="STOP", font=("Arial", 30), command=stopRobot)
    stop_button.grid(row=1, column=1)

def startBluetoothControls():
    awaitingBluetoothLabel.destroy()
    setUpControlPanel()
    
def moveUp():
    print("Move Up")

def moveLeft():
    print("Move Left")

def moveRight():
    print("Move Right")

def moveDown():
    print("Move Down")

def stopRobot():
    print("Robot stopped")

def startWindowAndBluetooth():
    threading.Thread(target=windowBoot).start()
    tryConnectingToPiWithBluetooth()

if __name__ == '__main__': 
    startWindowAndBluetooth()
