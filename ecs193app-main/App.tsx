

import React, { useState, useEffect } from "react";
import {
  SafeAreaView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  TextInput,
} from "react-native";
import DeviceConnectionModal from "./DeviceConnectionModal";
import EnableRobotModal from "./EnableRobotModal";
import useBLE from "./useBLE";

const App = () => {
  const {
    requestPermissions,
    scanForPeripherals,
    allDevices,
    connectToDevice,
    connectedDevice,
    disconnectFromDevice,
    handleArrowPress,
    //handleTimeoutAck,
    sendEnableSignal,
    sendDisableSignal,
    handleXYInput,
  } = useBLE();

  //State hooks for modals, robot toggle, and axis inputs
  const [isDeviceModalVisible, setIsDeviceModalVisible] = useState<boolean>(false);
  const [isEnableRobotModalVisible, setIsEnableRobotModalVisible] = useState<boolean>(false);
  const [robotToggle, setRobotToggle] = useState<boolean>(false);
  const [xAxis, setXAxis] = useState("");
  const [yAxis, setYAxis] = useState("");

  //Function to handle GPS input submission into text boxes
  const GPS_Input = () => {
    console.log("X-Axis is: ", xAxis);
    console.log("Y-Axis is: ", yAxis);
    handleXYInput(xAxis, yAxis);
  };

  //Function to scan for BLE devices after requesting permissions
  const scanForDevices = async () => {
    const isPermissionsEnabled = await requestPermissions();
    if (isPermissionsEnabled) {
      scanForPeripherals();
    }
  };

  //Function to hide the device connection modal
  const hideDeviceModal = () => {
    setIsDeviceModalVisible(false);
  };

  //Function to hide the enabled robot modal
  const hideEnableRobotModal = () => {
    setIsEnableRobotModalVisible(false);
  };

  //Function to open the enable robot modal
  const openEnableRobotModal = () => {
    setIsEnableRobotModalVisible(true);
  };
  

  //Function to open the device connection modal and initiate device scan
  const openDeviceModal = async () => {
    scanForDevices();
    setIsDeviceModalVisible(true);
  };

  //Function to toggle the robot's enable/disable state
  //Code does this by toggling the robotToggle state (true -> false or false -> true)
  const toggleRobot = () => {

    setRobotToggle((prev) => !prev);
    if(robotToggle) { //If the robot is currently enabled (robotToggle true), send a disable signal
      sendDisableSignal();
    }
    else { //If the robot is currently disabled (robotToggle is false), send an enable signal
      sendEnableSignal();
    }
  };

  //Currently commented out so testing won't spam robot with acks
  //Function which defines the interval for how frequent an ack should be sent
  /*useEffect(() => {
    const interval = setInterval(() => {
      handleTimeoutAck();
    }, 5000); // Every 5 seconds

    return () => clearInterval(interval); // Cleanup
  }, []);*/


  //How react native constructs the actual GUI based on calls to styles
  //If you want to modify how components are added, focus here
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.TitleWrapper}>
        {connectedDevice ? (
          <>
            <Text style={styles.TitleText}>
              Please Select GPS or Manual Input
            </Text>
          </>
        ) : (
          <Text style={styles.TitleText}>Tractor Squad App</Text>
        )}
      </View>
      <View style={styles.inputAxisContainer}>
        <TextInput
          style={styles.inputForAxis}
          onChangeText={setXAxis}
          value={xAxis}
          placeholder="X-Axis"
        />
        <TextInput
          style={styles.inputForAxis}
          onChangeText={setYAxis}
          value={yAxis}
          placeholder="Y-Axis"
        />
      </View>
      <TouchableOpacity onPress={GPS_Input} style={styles.gpsSubmitButton}>
        <Text style={styles.gpsSubmitButtonText}>Submit</Text>
      </TouchableOpacity>
      <View style={styles.arrowsContainer}>
        <View style={styles.arrowsContainerRow}>
          <TouchableOpacity
            onPressIn={() => handleArrowPress("up")}
            onPressOut={() => handleArrowPress("stop")}
            style={styles.arrowButton}
          >
            <Text style={styles.arrowText}>↑</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.arrowsContainerRow}>
          <TouchableOpacity
            onPressIn={() => handleArrowPress("left")}
            onPressOut={() => handleArrowPress("stop")}
            style={styles.arrowButton}
          >
            <Text style={styles.arrowText}>←</Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPressIn={() => handleArrowPress("down")}
            onPressOut={() => handleArrowPress("stop")}
            style={styles.arrowButton}
          >
            <Text style={styles.arrowText}>↓</Text>
          </TouchableOpacity>
          <TouchableOpacity
            onPressIn={() => handleArrowPress("right")}
            onPressOut={() => handleArrowPress("stop")}
            style={styles.arrowButton}
          >
            <Text style={styles.arrowText}>→</Text>
          </TouchableOpacity>
        </View>
      </View>
      <TouchableOpacity
        onPress={connectedDevice ? disconnectFromDevice : openDeviceModal}
        style={styles.connectButton}
      >
        <Text style={styles.enableButtonText}>
          {connectedDevice ? "Disconnect" : "Connect"}
        </Text>
      </TouchableOpacity>
      <TouchableOpacity onPress={openEnableRobotModal} style={styles.enableRobotButton}>
        {robotToggle ? (
          <>
          <TouchableOpacity onPress={toggleRobot} style={styles.disableRobotButton}>
          <Text style={styles.enableButtonText}>Enabled</Text>
          </TouchableOpacity></>
        ) : (
          <Text style={styles.enableButtonText}>Disabled</Text>
        )}
        
      </TouchableOpacity>
      <DeviceConnectionModal
        closeModal={hideDeviceModal}
        visible={isDeviceModalVisible}
        connectToPeripheral={connectToDevice}
        devices={allDevices}
      >
        <TouchableOpacity onPress={hideDeviceModal}>
          <Text style={styles.backButton}>Back</Text>
        </TouchableOpacity>
      </DeviceConnectionModal>
      <EnableRobotModal
        closeModal={hideEnableRobotModal}
        visible={isEnableRobotModalVisible}
        toggleOn={toggleRobot}
      />
    </SafeAreaView>
  );
};

//Styles for the components
//AKA GUI stuff. We really just carefully picked positions/values so this could
//be refactored for someone with more React Native GUI dev
//Also go here if you need to move around buttons
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f2f2f2",
    position: "relative", 

  },
  TitleWrapper: {
    position: "absolute", 
    top: 40, 
    left: 0, 
    right: 0, 
    justifyContent: "center",
    alignItems: "center",

  },
  TitleText: {
    fontSize: 30,
    fontWeight: "bold",
    textAlign: "center",
    marginHorizontal: 20,
    color: "black",
  },
  inputAxisContainer: {
    position: "absolute",
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "flex-start",
    marginHorizontal: 20,
    bottom: 150, 
    left: 90,
    width: 275
  },
  inputForAxis: {
    flex: 1,
    height: 40,
    borderColor: "gray",
    borderWidth: 1,
    paddingHorizontal: 10,
    borderRadius: 5,
    marginRight: 10,
    width: 30, 
  },
  arrowsContainer: {
    position: "absolute",
    bottom: 40,
    right: 40
  },
  arrowsContainerRow: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
  },
  arrowButton: {
    backgroundColor: "gray",
    justifyContent: "center",
    alignItems: "center",
    paddingVertical: 10,
    paddingHorizontal: 10,
    borderRadius: 20,
    margin: 10,
    width: 90,
    height: 90,
  },
  arrowText: {
    color: "white",
    fontSize: 24,
    fontWeight: "bold",
  },
  gpsSubmitButton: {
    backgroundColor: "#3065ba",
    justifyContent: "center",
    alignItems: "center",
    height: 40,
    marginHorizontal: 20,
    marginBottom: 10,
    borderRadius: 8,
    width: 100,
    alignSelf: "center",
    position: "absolute", 
    bottom: 20, 
    left: "30%",
    marginLeft: -50,
  },
  gpsSubmitButtonText: {
    fontSize: 18,
    fontWeight: "bold",
    color: "white",
  },
  enableButtonText: {
    fontSize: 18,
    fontWeight: "bold",
    color: "white",
    marginTop: 28.25, 
  },
  enableRobotButton: {
    backgroundColor: "#B53737", //Red
    justifyContent: "center",
    alignItems: "center",
    height: 60,
    top: 100, 
    marginBottom: 10,
    borderRadius: 8,
    width: 125,
    position: "absolute", 
    left: -62.5,
    transform: [{ rotate: "-90deg" }],
  },
  disableRobotButton: {
    backgroundColor: "#0F9D58", //Green
  justifyContent: "center",
    alignItems: "center",
    height: 60,
    marginBottom: 10,
    borderRadius: 8,
    width: 125, 
    position: "absolute",
  },
  connectButton: {
    backgroundColor: "#3065ba",
    justifyContent: "center",
    alignItems: "center",
    height: 60,
    top: 250,
    marginBottom: 10,
    borderRadius: 8,
    width: 125,
    position: "absolute",
    left: -62.5,
    transform: [{ rotate: "-90deg" }],
  },
  disableButtonText: {
    fontSize: 18,
    fontWeight: "bold",
    color: "white",
  },
  backButton: {
    fontSize: 18,
    fontWeight: "bold",
    color: "blue",
    marginTop: 10,
  },
});

export default App;