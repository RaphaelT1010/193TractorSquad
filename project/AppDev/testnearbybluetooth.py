from bluepy.btle import Scanner, DefaultDelegate

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device:", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

def discover_ble_devices():
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(10.0)  # Scan for 10 seconds

    for dev in devices:
        print("Device:", dev.addr)
        for (adtype, desc, value) in dev.getScanData():
            print("  %s = %s" % (desc, value))

if __name__ == "__main__":
    discover_ble_devices()
