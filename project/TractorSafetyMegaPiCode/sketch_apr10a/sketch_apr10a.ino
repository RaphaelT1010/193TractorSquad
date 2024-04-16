#include <Servo.h>
Servo my_servo1;
Servo my_servo2;
int STOP_POWER = 90;

void setup () {
  my_servo1.attach(5); // Use PWM pin 5 to control Sabertooth.
  my_servo2.attach(3);
  Serial.begin(9600);
}

void loop() {  
  // 0 means full power in one direction.
  // Actually the minimum value for me is around 30.
  // A smaller value won't drive the motor.
   
  // 90 means stopping the motor.
 
  // 180 means full power in the other direction.
  // Actually the maximum value for me is around 160.
  // A larger value won't drive the motor either.
  
  stopBot();

  pivotCW();
  // move forward
  stopBot();

}
    
void moveBotForward(int power){
  power = constrain(power, 0, 89);
  Serial.println("Moving forward");
  my_servo1.write(power);
  my_servo2.write(power);
  delay(2000);
}


void moveBotBackwards(int power){
  power = constrain(power, 91, 180);
  Serial.println("Moving backwards");
  my_servo1.write(power);
  my_servo2.write(power);
  delay(2000);
}


void stopBot(){  
  Serial.println("Stopping");
  my_servo1.write(STOP_POWER);
  my_servo2.write(STOP_POWER);
  delay(2000);
}



void pivotCW(){  
  Serial.println("Pivot CC");
  my_servo1.write(30);
  my_servo2.write(120);
  delay(2000);
}


  
      
      