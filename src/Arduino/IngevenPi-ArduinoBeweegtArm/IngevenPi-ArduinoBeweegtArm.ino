
#include <InverseK.h>
#include <Braccio.h>
#include <Servo.h>
#include <Wire.h>

int count = 0;
boolean flag = false;
double x,y,z;
double x1,y1,z1;
double x2,y2,z2;
double x3,y3,z3;
double XGetal,YGetal,ZGetal;
int kracht;
int angle;
Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;
void setup() {
  Serial.begin(9600);
 
  Link base, upperarm, forearm, hand;
  
  base.init(0, b2a(0.0), b2a(180.0));
  upperarm.init(200, b2a(15.0), b2a(165.0));
  forearm.init(200, b2a(0.0), b2a(180.0));
  hand.init(270, b2a(0.0), b2a(180.0));


  InverseK.attach(base, upperarm, forearm, hand);

  
  Wire.begin(0x04);
  Wire.onReceive(receiveData);
  Serial.println("Ready!");
 

 
  
 Braccio.begin();
}



void loop() {
  float a0, a1, a2, a3;
  
  if(InverseK.solve(20, 20,660, a0, a1, a2, a3)) {
    Serial.print(a2b(a0)); Serial.print(',');
    Serial.print(a2b(a1)); Serial.print(',');
    Serial.print(a2b(a2)); Serial.print(',');
    Serial.println(a2b(a3));
  } else {
     Braccio.ServoMovement(100,90,90, 90, 90, 90,  60);
     
  }
  Braccio.ServoMovement(20,a2b(a0),a2b(a1), a2b(a2), a2b(a3), 90,  50);
  while (true)
  {
    delay(0.02);
   if(flag)
   {
    flag = false;
    Serial.println("flag true");

    

   if(InverseK.solve(XGetal, YGetal,ZGetal, a0, a1, a2, a3)) {
    Serial.print(a2b(a0)); Serial.print(',');
    Serial.print(a2b(a1)); Serial.print(',');
    Serial.print(a2b(a2)); Serial.print(',');
    Serial.println(a2b(a3));
  } else {
     Braccio.ServoMovement(100,90,90, 90, 90, 90,  60);
     Serial.println("out of reach");
  }
  Serial.println("hoek : " + angle);

  Serial.println("kracht : " + kracht);
  
 
  
   Braccio.ServoMovement(20,a2b(a0),a2b(a1), a2b(a2), a2b(a3), angle,  kracht);
   
   delay(2000);

   if(InverseK.solve(20, 20,660, a0, a1, a2, a3)) {
    Serial.print(a2b(a0)); Serial.print(',');
    Serial.print(a2b(a1)); Serial.print(',');
    Serial.print(a2b(a2)); Serial.print(',');
    Serial.println(a2b(a3));
  } else {
     Braccio.ServoMovement(100,90,90, 90, 90, 90,  60);
     Serial.println("out of reach");
  }
  
  
 
  
   Braccio.ServoMovement(20,a2b(a0),a2b(a1), a2b(a2), a2b(a3), 50,  50);
   }
   
  }
   
}


float b2a(float b){ 
  return b / 180.0 * PI - HALF_PI;
}


float a2b(float a) { 
  return (a + HALF_PI) * 180 / PI;
}

void receiveData(int byteCount) 
{
  

  if(count == 0)
  {
    while (Wire.available()) {
    x = Wire.read();
    Serial.print("Xsign:");
    Serial.println(x);
    count++;
  }
  }
  if(count == 1)
  {
    while (Wire.available()) {
    x1 = Wire.read();
    Serial.print("X1:");
    Serial.println(x1);
    count++;
  }
  }
  if(count == 2)
  {
    while (Wire.available()) {
    x2 = Wire.read();
    Serial.print("X2:");
    Serial.println(x2);
    count++;
  }
  }
  if(count == 3)
  {
    while (Wire.available()) {
    x3 = Wire.read();
    Serial.print("X3:");
    Serial.println(x3);
    count++;
  }
  }
  if(count == 4)
  {
    while (Wire.available()) {
    y = Wire.read();
    Serial.print("Ysign:");
    Serial.println(y);
    count++;
  }
  }
  if(count == 5)
  {
    while (Wire.available()) {
    y1 = Wire.read();
    Serial.print("y1:");
    Serial.println(y1);
    count++;
  }
  }
  if(count == 6)
  {
    while (Wire.available()) {
    y2 = Wire.read();
    Serial.print("y2:");
    Serial.println(y2);
    count++;
  }
  }
  if(count == 7)
  {
    while (Wire.available()) {
    y3 = Wire.read();
    Serial.print("y3:");
    Serial.println(y3);
    count++;
  }
  }
  if(count == 8)
  {
    while (Wire.available()) {
    z = Wire.read();
    Serial.print("Zsign:");
    Serial.println(z);
    count++;
  }
  }
  if(count == 9)
  {
    while (Wire.available()) {
    z1 = Wire.read();
    Serial.print("z1:");
    Serial.println(z1);
    count++;
  }
  }
  if(count == 10)
  {
    while (Wire.available()) {
    z2 = Wire.read();
    Serial.print("z2:");
    Serial.println(z2);
    count++;
  }
  }
  if(count == 11)
  {
    while (Wire.available()) {
    z3 = Wire.read();
    Serial.print("z3:");
    Serial.println(z3);
    XGetal = 0+x1+x2+x3;
    YGetal = 0+y1+y2+y3;
    ZGetal = 0+z1+z2+z3;

    if(x == 0)
    {
      XGetal=XGetal*-1;
    }
    
    
    if(y == 0)
    {
      YGetal=YGetal*-1;
    }
    
    if(z == 0)
    {
      ZGetal=ZGetal*-1;
    }
    Serial.print("Xwaarde: ");
    Serial.println(XGetal);
    Serial.println("Xwaarde: ");
    Serial.println(YGetal);
    Serial.println("Zwaarde: ");
    Serial.println(ZGetal);
    count++;
  }
  }
  if(count == 12)
  {
    while (Wire.available()) {
    angle = Wire.read();
    Serial.print("angle:");
    Serial.println(angle);
    count++;
  }
  }
  if(count == 13)
  {
    while (Wire.available()) {
    kracht = Wire.read();
    Serial.print("kracht:");
    Serial.println(kracht);
    flag = true;
    count = 0;
  }
  }
    
    

  }
