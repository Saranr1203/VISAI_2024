#include <Arduino.h>
#include <Wire.h>
#include <TFLI2C.h>
#include<Servo.h>

TFLI2C tflI2C; 
int16_t  tfDist;
int16_t  tfAddr = TFL_DEF_ADR;

Servo micro_servo;
int pos = 0;
const int servo_pin = 5;
float duration, distance;

void setup() {
  // put your setup code here, to run once:
  pinMode(7, OUTPUT);
  pinMode(servo_pin,OUTPUT);
  Serial.begin(9600);
  micro_servo.attach(servo_pin);
  Wire.begin();
}

void loop() {
  // put your main code here, to run repeatedly:

  for(pos = 0;pos<=180; pos=pos+15)
  {
    micro_servo.write(pos);
    delay(50);
    if(tflI2C.getData(tfDist, tfAddr)){
      if (tfDist < 30){
          digitalWrite(7,LOW);
      }
      else{
        digitalWrite(7, HIGH);
      }
      Serial.print(pos);
      Serial.print(",");
      Serial.println(String(tfDist));
    }
  }

  for(pos = 180;pos >= 0; pos=pos-15)
  {
    micro_servo.write(pos);
    delay(50);
    if(tflI2C.getData(tfDist, tfAddr)){
      if (tfDist < 30){
        digitalWrite(7, LOW);
      }
      else{
        digitalWrite(7, HIGH);
      }
      Serial.print(pos);
      Serial.print(",");
      Serial.println(tfDist);
    }
  }
  // delay(200);
}