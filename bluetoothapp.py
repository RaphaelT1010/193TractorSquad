import tkinter as tk
import threading
import time
import bluetooth

def windowBoot():
    global window
    window = tk.Tk()
    window.title("Tractor Squad")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")

    global bluetoothLabel
    bluetoothLabel = tk.Label(window, font=("Arial", 30), text="Awaiting bluetooth connection...")
    bluetoothLabel.place(relx=0.5, rely=0.5, anchor="center")

    window.mainloop()

def listenForBluetooth():
    #Simulate listening for bluetooth connection here
    time.sleep(2)
    bluetoothLabel.destroy()
    window.after(0, startBluetoothControls)

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
    # Create arrow icons for controlling robot movement
    setUpControlPanel()
    

def moveUp():
    #Send movement
    print("Move Up")

def moveLeft():
    #Send movement
    print("Move Left")

def moveRight():
    #Send movement
    print("Move Right")

def moveDown():
    #Send movement
    print("Move Down")

def stopRobot():
    #Send movement
    print("Robot stopped")



def startWindowAndBluetooth():
    # Start the Tkinter window in a separate thread
    threading.Thread(target=windowBoot).start()
    
    # Start listening for Bluetooth connections in the main thread
    listenForBluetooth()

if __name__ == '__main__': 
    startWindowAndBluetooth()
