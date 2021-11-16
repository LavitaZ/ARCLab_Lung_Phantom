#include <Regexp.h>
#include <PID_v1.h>
#include <ADC.h>

#include <math.h>
// serial.settimeout()
const int SAMPLE_TIME = 50;
int tlastrec = 0;
double control = 0;
double measured_pressure;
double target_pressure = 505;
int state = 1;
String blowerlevels ;//pwm to blower
int blowerleveli;
int pressure;
String setpoint;
int num = 589;

double Kp=4, Ki=0.4, Kd=0.5;
//double Kp=1, Ki=0.1, Kd=0.25; //PID constants, 4, 0.4, 0.5
//double Kp=0.25, Ki=0.025, Kd=0.06; //PID constants, 4, 0.4, 0.5

PID myPID(&measured_pressure, &control, &target_pressure, Kp, Ki, Kd, DIRECT);
elapsedMillis t;

void setup()
{     
  pinMode(A0, INPUT);
  pinMode(15, OUTPUT);      
  Serial.begin(115200); 
  delay(200);
  Serial.setTimeout(1);

  myPID.SetMode(AUTOMATIC);
  myPID.SetSampleTime(SAMPLE_TIME);
  
}

void loop()  {
  analogWrite(15, control);

  
while(Serial.available()>0){
  setpoint = Serial.readStringUntil('\n');
  target_pressure = setpoint.toInt();
  Serial.println(measured_pressure);
}
  Serial.flush();
  measured_pressure = analogRead(A0);
  myPID.Compute();




  
  setpoint = "";
}
