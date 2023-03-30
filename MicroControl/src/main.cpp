#include <Arduino.h>
#include <Wire.h>
#include <JY901.h>
#include <Servo.h>
#include "PINOUT.h"
/*
http://item.taobao.com/item.htm?id=43511899945
Test on mega2560.
JY901   mega2560
TX <---> 0(Rx)
*/
Servo turnServo;
Servo throttleServo;
float x = 0;
float y = 0;

void setup() {
  Serial.begin(9600);
  JY901.StartIIC();  
  turnServo.attach(TURN_SERVO_PIN);
  throttleServo.attach(THROTTLE_SERVO_PIN);
  turnServo.write(90);
  throttleServo.write(90);
}

void setSpeed(float speed, Servo * servo){
  if(speed > 1) speed = 1;
  if(speed < -1) speed = -1;
  speed = (speed + 1) / 90; // scale the speed from -1 to 1 to 0 to 180
  servo->write(speed);
}

void printData(){
  Serial.print("!TIME,");
  Serial.print(JY901.stcTime.ucYear);
  Serial.print(",");
  Serial.print(JY901.stcTime.ucMonth);
  Serial.print(",");
  Serial.print(JY901.stcTime.ucDay);
  Serial.print(",");
  Serial.print(JY901.stcTime.ucHour);
  Serial.print(",");
  Serial.print(JY901.stcTime.ucMinute);
  Serial.print(",");
  Serial.print((float)JY901.stcTime.ucSecond+(float)JY901.stcTime.usMiliSecond/1000);
  Serial.println(";");
               
  Serial.print("!ACC,");
  Serial.print((float)JY901.stcAcc.a[0]/32768*16);
  Serial.print(",");
  Serial.print((float)JY901.stcAcc.a[1]/32768*16);
  Serial.print(",");
  Serial.print((float)JY901.stcAcc.a[2]/32768*16);
  Serial.println(";");
  
  Serial.print("!GYRO,");
  Serial.print((float)JY901.stcGyro.w[0]/32768*2000);
  Serial.print(",");
  Serial.print((float)JY901.stcGyro.w[1]/32768*2000);
  Serial.print(",");
  Serial.print((float)JY901.stcGyro.w[2]/32768*2000);
  Serial.println(";");
  
  Serial.print("!ANGLE,");
  Serial.print((float)JY901.stcAngle.Angle[0]/32768*180);
  Serial.print(",");
  Serial.print((float)JY901.stcAngle.Angle[1]/32768*180);
  Serial.print(",");
  Serial.print((float)JY901.stcAngle.Angle[2]/32768*180);
  Serial.println(";");
  
  Serial.print("!MAG,");
  Serial.print(JY901.stcMag.h[0]);
  Serial.print(",");
  Serial.print(JY901.stcMag.h[1]);
  Serial.print(",");
  Serial.print(JY901.stcMag.h[2]);
  Serial.println(";");
  
  Serial.print("!PRESSURE,");
  Serial.print(JY901.stcPress.lPressure);
  Serial.print(",");
  Serial.print((float)JY901.stcPress.lAltitude/100);
  Serial.println(";");
  
  Serial.print("!DSTATUS,");
  Serial.print(JY901.stcDStatus.sDStatus[0]);
  Serial.print(",");
  Serial.print(JY901.stcDStatus.sDStatus[1]);
  Serial.print(",");
  Serial.print(JY901.stcDStatus.sDStatus[2]);
  Serial.print(",");
  Serial.print(JY901.stcDStatus.sDStatus[3]);
  Serial.println(";");
  
 Serial.print("Longitude:");
 Serial.print(JY901.stcLonLat.lLon/10000000);
 Serial.print("Deg");
 Serial.print((double)(JY901.stcLonLat.lLon % 10000000)/1e5);
 Serial.print("m Lattitude:");
 Serial.print(JY901.stcLonLat.lLat/10000000);
 Serial.print("Deg");
 Serial.print((double)(JY901.stcLonLat.lLat % 10000000)/1e5);
 Serial.println("m");
 
 Serial.print("GPSHeight:");
 Serial.print((float)JY901.stcGPSV.sGPSHeight/10);
 Serial.print("m GPSYaw:");
 Serial.print((float)JY901.stcGPSV.sGPSYaw/10);
 Serial.print("Deg GPSV:");
 Serial.print((float)JY901.stcGPSV.lGPSVelocity/1000);
 Serial.println("km/h");
  
  Serial.print("SN:");
  Serial.print(JY901.stcSN.sSVNum);
  Serial.print(" PDOP:");
  Serial.print((float)JY901.stcSN.sPDOP/100);
  Serial.print(" HDOP:");
  Serial.print((float)JY901.stcSN.sHDOP/100);
  Serial.print(" VDOP:");
  Serial.println((float)JY901.stcSN.sVDOP/100);

//  while (Serial.available()) 
//  {
//    JY901.CopeSerialData(Serial.read()); //Call JY901 data cope function
//  }

}

void loop() {
  JY901.GetTime();
  JY901.GetAcc();
  JY901.GetGyro();
  JY901.GetAngle();
  JY901.GetMag();
  JY901.GetPress();
  JY901.GetDStatus();
  JY901.GetLonLat();
  JY901.GetGPSV();

  float accelX = float(JY901.stcAcc.a[0])/32768*16;
  float accelY = float(JY901.stcAcc.a[1])/32768*16;
  float accelZ = float(JY901.stcAcc.a[2])/32768*16;
  float gyroX = float(JY901.stcGyro.w[0])/32768*2000;
  float gyroY = float(JY901.stcGyro.w[1])/32768*2000;
  float gyroZ = float(JY901.stcGyro.w[2])/32768*2000;
  float angleX = float(JY901.stcAngle.Angle[0])/32768*180;
  float angleY = float(JY901.stcAngle.Angle[1])/32768*180;
  float angleZ = float(JY901.stcAngle.Angle[2])/32768*180;

  x = 0.9 * x + 0.1 * angleX;
  y = 0.9 * y + 0.1 * angleY;

  setSpeed(x, &turnServo);
  setSpeed(y, &throttleServo);
  // printData();
  
}