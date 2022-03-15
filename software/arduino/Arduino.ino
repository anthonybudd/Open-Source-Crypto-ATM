#include <Arduino.h>
#include <ReceiveOnlySoftwareSerial.h>
#include <Apex5400BillAcceptor.h>

#define PIN_ENABLE 7 // To Pin 12 (violet)
#define PIN_INTERRUPT_LINE 8 // To Pin 2 (orange)
#define PIN_SEND_LINE 9 // To Pin 14 (blue/white)
#define PIN_TTL_RX 10 // to Pin 5 (green)

Apex5400BillAcceptor *billAcceptor;

int code;
bool hasCredit = false;
bool isPrinting = false;
int ledPin = 6;
int switchPin = 5;
int ledState = LOW;
unsigned long previousMillis = 0;
const long interval = 500; 
int incomingByte = 0;

const byte numChars = 32;
char receivedChars[numChars];
boolean newData = false;

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(switchPin, INPUT);
  Serial.begin(9600);
  billAcceptor = new Apex5400BillAcceptor(PIN_ENABLE, PIN_INTERRUPT_LINE, PIN_SEND_LINE, PIN_TTL_RX);    
  billAcceptor->enable();
  Serial.println("READY");
}

void loop() {
  
  // Wait for credit
  if (isPrinting == false) {
    if (code = billAcceptor->checkForBill()) {
      Serial.println(billAcceptor->getDescription(code));

      switch(code) {
        case 0x81:
        case 0x83:
        case 0x84:
        case 0x85:
        case 0x86:
        case 0x87:
          hasCredit = true;
          billAcceptor->disable(); // Sync LED flashing on button and Apex
          billAcceptor->enable();
          break;
      }
    }
  }

  // We have credit, wait for button press
  if (hasCredit == true) {
    flash();
    
    if (digitalRead(switchPin) == HIGH) {
      Serial.println("PRINT");
      billAcceptor->disable();
      digitalWrite(ledPin, LOW);
      isPrinting = true;
      hasCredit = false;
    }
  }

  // Always listen for "RESET" signal
  isResetSigal();
  recvWithEndMarker(); 
}

void flash(){
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    if (ledState == LOW) {
      ledState = HIGH;
    } else {
      ledState = LOW;
    }

    digitalWrite(ledPin, ledState);
  }
}

void recvWithEndMarker() {
  static byte ndx = 0;
  char endMarker = '\n';
  char rc;
 
  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();
    
    if (rc != endMarker) {
      receivedChars[ndx] = rc;
      ndx++;
      if (ndx >= numChars) {
        ndx = numChars - 1;
      }
    } else {
      receivedChars[ndx] = '\0'; // terminate the string
      ndx = 0;
      newData = true;
    }
  }
}

void isResetSigal() {
  if (newData == true) {
    String input(receivedChars);
    Serial.println(input);
    if (input == "RESET") {
      reset();
    }
    newData = false;
  }
}

void reset(){
  Serial.println("RESETTING");
  billAcceptor->enable();
  isPrinting = false;
  hasCredit = false;
}
