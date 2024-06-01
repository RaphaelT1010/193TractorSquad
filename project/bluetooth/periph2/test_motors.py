import time
from motor import motor

def test_motor():
    # Initialize the motor object
    m = motor()
    print("Motor initialized")

    # Test drive forward
    print("Testing drive forward")
    #m.drive_forward()
    #time.sleep(1)  # Wait for 1 second
    
    print("Testing stop")
    m.stop()
    time.sleep(1)  # Wait for 1 second


    # Test drive backward
    #print("Testing drive backward")
    m.drive_backwards()
    #time.sleep(1)  # Wait for 1 second
    
    print("Testing stop")
    m.stop()
    time.sleep(1)  # Wait for 1 second


    # Test turn left
    print("Testing turn left")
    #m.turn_left()
    time.sleep(1)  # Wait for 1 second
    
    print("Testing stop")
    m.stop()
    time.sleep(1)  # Wait for 1 second


    # Test turn right
    print("Testing turn right")
    m.turn_right()
    time.sleep(1)  # Wait for 1 second

    # Test pivot clockwise
    #print("Testing pivot clockwise")
    m.pivotCW()
    time.sleep(1)  # Wait for 1 second

    # Test pivot counterclockwise
    #print("Testing pivot counterclockwise")
   # m.pivotCCW()
    time.sleep(1)  # Wait for 1 second
    
    print("Testing stop")
    m.stop()
    time.sleep(1)  # Wait for 1 second


    # Test stop
    print("Testing stop")
    m.stop()
    time.sleep(1)  # Wait for 1 second

    print("Motor test completed")

if __name__ == "__main__":
    test_motor()
