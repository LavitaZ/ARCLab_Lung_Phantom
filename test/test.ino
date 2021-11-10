#include <math.h>
#include <ArduinoJson.h>
const int SAMPLE_TIME = 50;
double measured_pressure;
double control = 0;

double start_time = 0;
double elapsed_time = 0;
double target = 505;
String werd;
String command;

void setup()
{     
  pinMode(A0, INPUT);
  pinMode(15, OUTPUT);      
  Serial.begin(115200); //auto set for teensy to something fast?
}

void loop()                     
{
  elapsedMillis t0;
  //---------------------------------------------------------
  //shutdown after 20 seconds 
  //---------------------------------------------------------
  elapsed_time = (millis() - start_time)/1000;
  //508
  //if((elapsed_time > 20)||(target_pressure <= 508)||(target <= 508)){
    //control = 0;
  //}

  //---------------------------------------------------------
  //update actuators / fan
  //---------------------------------------------------------
    analogWrite(15, control);//pwm 0-255
    
  //---------------------------------------------------------
  //get command from serial port
  //---------------------------------------------------------
    while(Serial.available() > 0){
      //delay(5);
      werd = Serial.read();
      command += werd;
    }
    Serial.flush();
    if(command.length() > 0){
      control = command.toInt();
      start_time = millis();//start counting time after last command
    }
    
  //---------------------------------------------------------
  //read sensors
  //---------------------------------------------------------
      measured_pressure = analogRead(A0);
          
    //---------------------------------------------------------
    //print to serial
    //---------------------------------------------------------
//    Serial.println(target_pressure - measured_pressure, t);
    Serial.println(measured_pressure);

    if(t0 < SAMPLE_TIME){
      delay(SAMPLE_TIME - t0);
    }
//    Serial.println(t0);

    command = "";

}
