#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// Define pulse range values for MG995 servo
#define SERVOMIN  150   // Pulse for 0°
#define SERVOMAX  600   // Pulse for 180°
#define SERVO_NUM_0  0     // Channel 0
#define SERVO_NUM_1  1     // Channel 1
#define SERVO_NUM_2  3     // Channel 2


// Map angle to pulse value
int angleToPulse(int angle) {
  return map(angle, 0, 180, SERVOMIN, SERVOMAX);
}

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(50); // Standard frequency for analog servos
  pinMode(13, OUTPUT); 
  pinMode(7, INPUT); 
  delay(10);
  Serial.println("Starting 0° → 180° → 0° loop...");
}

void loop() {

  int pin7State = digitalRead(7);  // Read the state of digital pin 6

  if (pin7State == HIGH) 
  {

  digitalWrite(13, HIGH);
  Serial.println("🔆 ONBOARD LED ON (Pin 6 is HIGH)");
  // 90° to 0° for channel 0
  for (int angle = 90; angle >= 0; angle -= 5) {
    int pulse = angleToPulse(angle);
    pwm.setPWM(SERVO_NUM_0, 0, pulse);
    Serial.print("Angle: ");
    Serial.println(angle);
    delay(100);
  }
  delay(1000);
  // 0° to 90° for channel 1
   for (int angle = 0; angle <= 90; angle += 5) {
    int pulse = angleToPulse(angle);
    pwm.setPWM(SERVO_NUM_1, 0, pulse);
    Serial.print("Angle: ");
    Serial.println(angle);
    delay(100); // Smooth motion
  }
  delay(1000);
  
  // 0° to 90° for channel 2
  for (int angle = 0; angle <= 90; angle += 5) {
    int pulse = angleToPulse(angle);
    pwm.setPWM(SERVO_NUM_2, 0, pulse);
    Serial.print("Angle: ");
    Serial.println(angle);
    delay(100); // Smooth motion
  }
  delay(500);

  // 90° to 0° for channel 2
  for (int angle = 90; angle >= 0; angle -= 5) {
    int pulse = angleToPulse(angle);
    pwm.setPWM(SERVO_NUM_2, 0, pulse);
    Serial.print("Angle: ");
    Serial.println(angle);
    delay(100);
  }
  delay(500);

   // 90° to 0° for channel 1
  for (int angle = 90; angle >= 0; angle -= 5) {
    int pulse = angleToPulse(angle);
    pwm.setPWM(SERVO_NUM_1, 0, pulse);
    Serial.print("Angle: ");
    Serial.println(angle);
    delay(100);
  }
  delay(1000);
  // 0° to 90° for channel 0
  for (int angle = 0; angle <= 90; angle += 5) {
    int pulse = angleToPulse(angle);
    pwm.setPWM(SERVO_NUM_0, 0, pulse);
    Serial.print("Angle: ");
    Serial.println(angle);
    delay(100); // Smooth motion
  }
  delay(1000);
  }
  
  else {
    digitalWrite(13, LOW);        // Turn OFF onboard LED
    Serial.println("💤 ONBOARD LED OFF (Pin 6 is LOW)");
  }

  delay(500); 
}