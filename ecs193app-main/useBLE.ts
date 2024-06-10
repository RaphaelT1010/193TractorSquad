import { useMemo, useState } from "react";
import { PermissionsAndroid, Platform } from "react-native";
import { BleManager, Device } from "react-native-ble-plx";
import * as ExpoDevice from "expo-device";
import base64 from "react-native-base64";

//UUIDs for specific services and characteristics to the robot
const CONTROL_SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb";
const CONTROL_CHARACTERISTIC_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb";
const GPS_SERVICE_UUID = "0392fac1-9fd3-1023-a4e2-39109fa39aa2";
const GPS_CHARACTERISTIC_UUID = "0102aaaa-3333-1111-abcd-0123456831fd";

//Interface defining the API calls we're using for this app
interface BluetoothLowEnergyApi {
  requestPermissions(): Promise<boolean>;
  scanForPeripherals(): void;
  connectToDevice: (device: Device) => Promise<void>;
  disconnectFromDevice: () => void;
  connectedDevice: Device | null;
  allDevices: Device[];
  handleArrowPress: (direction: string) => void;
  //handleTimeoutAck: () => void;
  sendEnableSignal: () => void;
  sendDisableSignal: () => void;
  handleXYInput: (x: string, y: string) => void;
}

//Custom hook to manage BLE operations
function useBLE(): BluetoothLowEnergyApi {
  const bleManager = useMemo(() => new BleManager(), []);
  const [allDevices, setAllDevices] = useState<Device[]>([]);
  const [connectedDevice, setConnectedDevice] = useState<Device | null>(null);
  
  //Function to request permissions for Android 31+
  const requestAndroid31Permissions = async () => {
    const bluetoothScanPermission = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.BLUETOOTH_SCAN,
      {
        title: "Location Permission",
        message: "Bluetooth Low Energy requires Location",
        buttonPositive: "OK",
      }
    );
    const bluetoothConnectPermission = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.BLUETOOTH_CONNECT,
      {
        title: "Location Permission",
        message: "Bluetooth Low Energy requires Location",
        buttonPositive: "OK",
      }
    );
    const fineLocationPermission = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
      {
        title: "Location Permission",
        message: "Bluetooth Low Energy requires Location",
        buttonPositive: "OK",
      }
    );

    return (
      bluetoothScanPermission === "granted" &&
      bluetoothConnectPermission === "granted" &&
      fineLocationPermission === "granted"
    );
  };

  //Function to request necessary permissions based on the platform and Android version
  const requestPermissions = async () => {
    if (Platform.OS === "android") {
      if ((ExpoDevice.platformApiLevel ?? -1) < 31) {
        const granted = await PermissionsAndroid.request(
          PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
          {
            title: "Location Permission",
            message: "Bluetooth Low Energy requires Location",
            buttonPositive: "OK",
          }
        );
        return granted === PermissionsAndroid.RESULTS.GRANTED;
      } else {
        const isAndroid31PermissionsGranted =
          await requestAndroid31Permissions();

        return isAndroid31PermissionsGranted;
      }
    } else {
      return true;
    }
  };

  //Function to check for duplicate devices
  const isDuplicateDevice = (devices: Device[], nextDevice: Device) =>
    devices.findIndex((device) => nextDevice.id === device.id) > -1;

  //Function to start scanning for peripherals
  const scanForPeripherals = () =>
    bleManager.startDeviceScan(null, null, (error, device) => {
      if (error) {
        console.log(error);
      }
      if (device && device.name == 'tractorsquad') {
        setAllDevices((prevState: Device[]) => {
          if (!isDuplicateDevice(prevState, device)) {
            return [...prevState, device];
          }
          return prevState;
        });
      }
    });

  //Function to connect to a device
  const connectToDevice = async (device: Device) => {
    try {
      await bleManager.connectToDevice(device.id);
      setConnectedDevice(device);
      await device.discoverAllServicesAndCharacteristics();
      bleManager.stopDeviceScan();
      sendEnableSignal();
    } catch (e) {
      console.log("FAILED TO CONNECT", e);
    }
  };

  //Function to disconnect from a device
  const disconnectFromDevice = () => {
    if (connectedDevice) {
      bleManager.cancelDeviceConnection(connectedDevice.id);
      setConnectedDevice(null);
      sendDisableSignal();
    }
  };

  //*********************************************************************** */
  //We don't recommend you change characterstics/UUIDS unless
  //you know what you're doing. sendGPSCommand and sendControlCommand
  //probably shouldn't be changed, but instead just added onto to unless
  //if you're doing a major overhaul of the app/characteristic UUID interpretation
  //*********************************************************************** */


  //Function to send a control command to the connected device
  //This is a movement command
  const sendControlCommand = async (command: string) => {
    if (!connectedDevice) {
      console.log("No device connected");
      return;
    }

    try {
      const characteristics = await connectedDevice.characteristicsForService(
        CONTROL_SERVICE_UUID
      );
      const controlCharacteristic = characteristics.find(
        (c) => c.uuid === CONTROL_CHARACTERISTIC_UUID
      );
      if (controlCharacteristic) {
        //await controlCharacteristic.writeWithoutResponse(base64.encode(command));
        await controlCharacteristic.writeWithResponse(base64.encode(command));
      }
    } catch (error) {
      console.log("Error sending control command", error);
    }
  };

  // Function to send a GPS command to the connected device
  //This is a GPS coordinate 
  const sendGPSCommand = async (gps: string) => {
    if (!connectedDevice) {
      console.log("No device connected");
      return;
    }

    try {
      const characteristics = await connectedDevice.characteristicsForService(
        GPS_SERVICE_UUID
      );
      const controlCharacteristic = characteristics.find(
        (c) => c.uuid === GPS_CHARACTERISTIC_UUID
      );
      if (controlCharacteristic) {
        //await controlCharacteristic.writeWithoutResponse(base64.encode(gps));
        await controlCharacteristic.writeWithResponse(base64.encode(gps));
      }
    } catch (error) {
      console.log("Error sending control command", error);
    }
  };

  const handleXYInput = (x: string, y: string) => {
    var long = +x;
    var lat = +y;
    long = (long * 1000000) | 0;
    lat = (lat * 1000000) | 0;
    var index = 0;


    var toWrite = String.fromCharCode((index << 1) + ((long & (1 << 28)) >> 28));

    for (var i = 255 << 20, j = 20; i > 15; i >>= 8, j -= 8) {
      toWrite += String.fromCharCode((long & i) >> j);
    }

    toWrite += String.fromCharCode(((long & 15) << 4) + ((lat & (15 << 24)) >> 24))

    for (var i = 255 << 16, j = 16; i > 0; i >>= 8, j -= 8) {
      toWrite += String.fromCharCode((lat & i) >> j);
    }

    sendGPSCommand(toWrite);
  }
  
  //Function to handle arrow press input and send corresponding control command
  //Left = "l"
  //Up = "u"
  //Right = "r"
  //Down = "d"
  //Stop = "s"
  //A stop signal should send after a button is let go. For redundancy and safety
  const handleArrowPress = (direction: string) => {
    switch (direction) {
      case "left":
        console.log(direction);
        sendControlCommand("l");
        break;
      case "up":
        console.log(direction);
        sendControlCommand("u");
        break;
      case "right":
        console.log(direction);
        sendControlCommand("r");
        break;
      case "down":
        console.log(direction);
        sendControlCommand("d");
        break;
      case "stop":
        console.log(direction);
        sendControlCommand("s");
        break;
      default:
        break;
    }
  };

  //Currently commented out so PI won't be flooded with acks
  //Sends a perioduc signal to the PI
  //Ack = "@"
  /*const handleTimeoutAck = () => {
    console.log("Acknwoledgement signal sent");
    //& is 38 in ascii being sent to the Pi
    sendControlCommand("@");
  };*/

  //Function to send an enable signal to the device
  //Enable = "&"
  const sendEnableSignal = () => {
    console.log("Turning on the Robot");
    //& is 38 in ascii being sent to the Pi
    sendControlCommand("&");
  };

  //Function to send a disable signal to the device
  //Disable = "#"
  const sendDisableSignal = () => {
    console.log("Turning off the Robot");
    //& is 38 in ascii being sent to the Pi
    sendControlCommand("#");
  };

  return {
    scanForPeripherals,
    requestPermissions,
    connectToDevice,
    allDevices,
    connectedDevice,
    disconnectFromDevice,
    handleArrowPress,
    //handleTimeoutAck,
    sendEnableSignal,
    sendDisableSignal,
    handleXYInput,
  };
}

export default useBLE;