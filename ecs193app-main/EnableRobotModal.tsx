import React from "react";
import { Modal, View, Text, TouchableOpacity, StyleSheet } from "react-native";

interface EnableRobotModalProps {
  visible: boolean;
  closeModal: () => void;
  toggleOn: () => void
}

const EnableRobotModal: React.FC<EnableRobotModalProps> = ({ visible, closeModal, toggleOn }) => {
  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={visible}
      onRequestClose={closeModal}
    >
      <View style={styles.centeredView}>
        <View style={styles.modalView}>
          <Text style={styles.modalText}>Are you sure you want to turn the robot on?</Text>
          <TouchableOpacity onPress={closeModal} onPressIn={toggleOn}>
            <Text style={styles.closeButton}>Yes, Turn it on</Text>
          </TouchableOpacity>
          <TouchableOpacity onPress={closeModal}>
            <Text style={styles.closeButton}>No, Keep it off</Text>
          </TouchableOpacity>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  centeredView: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
  modalView: {
    backgroundColor: "white",
    borderRadius: 20,
    padding: 35,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  modalText: {
    marginBottom: 15,
    textAlign: "center",
    fontSize: 20,
    fontWeight: "bold",
  },
  closeButton: {
    marginTop: 10,
    fontSize: 18,
    color: "blue",
    fontWeight: "bold",
  },
});

export default EnableRobotModal;
