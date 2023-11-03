// Notes
// - Serial Monitor is located in the top right of the Arduino IDE
// - Nothing is plugged into the Channel A and B pins definied below, those pins are routed via the MotorShield PCB traces to the motor controls

// channel A motor
int directionPin = 12;
int brakePin = 9;
int pwmPin = 3;

//uncomment if using channel B, and remove above definitions
//int directionPin = 13;
//int brakePin = 8;
//int pwmPin = 11;

// set bool motorOn
bool motorOn = false;
// set char motorDirOld
char motorDirOld = false;


void setup() {
  // put your setup code here, to run once

  // define pins
  pinMode(directionPin, OUTPUT);
  pinMode(pwmPin, OUTPUT);
  pinMode(brakePin, OUTPUT);

  pinMode(A0, INPUT); // not necessary since all pins start as input
  pinMode(A1, INPUT); // not necessary since all pins start as input
  pinMode(A2, INPUT); // not necessary since all pins start as input
  pinMode(A3, INPUT); // not necessary since all pins start as input 
  pinMode(A4, INPUT); // not necessary since all pins start as input
  pinMode(A5, INPUT); // not necessary since all pins start as input 

  Serial.begin(9600);
  Serial.println("Starting program...");
}



void loop() {
  // put your main code here, to run repeatedly

  // * read pins *
  int sensorA0 = analogRead(A0);
  int sensorA1 = analogRead(A1);

  int voltageA0 = round(sensorA0 * (5.0 / 1023.0));
  int voltageA1 = round(sensorA1 * (5.0 / 1023.0));
  /*
  Serial.print("A0: ");
  Serial.println(voltageA0);
  Serial.print("A1: ");
  Serial.println(voltageA1);
  */

  // * check status and peform motor action *
  
  // switch forward
  if(voltageA0 > 1) {
    Serial.println("Motor forward");
    motorOn = directionChannelA(motorOn, HIGH);
    // open blast gate
     pinMode(A5, OUTPUT);
  }
  
  // switch backwards
  if(voltageA1 > 1) {
    Serial.println("Motor backwards");
    motorOn = directionChannelA(motorOn, LOW);
    // close blast gate
    pinMode(A5, INPUT);
  }
  
  // switch middle
  if(voltageA0 <= 1 and voltageA1 <= 1) {
    motorOn = brakeChannelA();
  }
  
  // print motor status
  //Serial.print("motorOn: ");
  //Serial.println(motorOn);

  // delay loop
  delay(100);
}



// functions
bool brakeChannelA() {
  Serial.println("Motor brake");
  digitalWrite(brakePin, HIGH); // engage the Brake for Channel A
  delay(500);
  return false;
}

bool directionChannelA(bool motorOn, char motorDir) {
  digitalWrite(brakePin, LOW); // disengage the Brake for Channel A
  digitalWrite(directionPin, motorDir);
  
  // if the motor switch is changed from one direction to the other to fast, the brake will trigger
  if(motorOn == true and motorDir != motorDirOld) {
    Serial.println("* Motor direction change to fast *");
    motorOn = brakeChannelA();
  }

  // slowly spin up the motor on Channel A if the motor was off
  if(motorOn == false) {
    motorDirOld = motorDir;
    Serial.println("Motor spin up");
    delay(200);
    analogWrite(pwmPin, 100);
    delay(200);
    analogWrite(pwmPin, 200);
    delay(200);
    analogWrite(pwmPin, 255);
    return true;
  }

  // motor is already on at this point
  return true;
}
