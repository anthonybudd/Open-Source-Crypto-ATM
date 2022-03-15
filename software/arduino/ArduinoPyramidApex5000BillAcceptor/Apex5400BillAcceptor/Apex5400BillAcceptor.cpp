#include <Apex5400BillAcceptor.h>

Apex5400BillAcceptor::Apex5400BillAcceptor(int a, int b, int c, int d){
	pin_enable_line = a;
	pinMode(pin_enable_line, OUTPUT);
	digitalWrite(pin_enable_line, LOW);
	
	pin_interrupt_line = b;						
	pinMode(pin_interrupt_line, INPUT);
	
	pin_send_line = c;
	pinMode(pin_send_line, OUTPUT);					
	
	pin_ttl_rx = d;
	pinMode(pin_ttl_rx, INPUT_PULLUP);
	mySerial = new ReceiveOnlySoftwareSerial(pin_ttl_rx);
	mySerial->begin(600);
}

int Apex5400BillAcceptor::checkForBill(){
	// if (digitalRead(pin_interrupt_line) == LOW){
    digitalWrite(pin_send_line, LOW);
    digitalWrite(pin_send_line, HIGH);  

    delay(5);
    
    if (mySerial->available()){
        int code = mySerial->read();					
        return code;
    }
	//}
	return 0;
}

char* Apex5400BillAcceptor::getDescription(int codeFromBillAcceptor){
	for(int i=0; i < sizeof(codes)/sizeof(codes[0]); i++){
		if (codes[i].code == codeFromBillAcceptor){
			return codes[i].description;
		}
	}
	return "(code undefined)";
}

void Apex5400BillAcceptor::enable(){
	digitalWrite(pin_enable_line, LOW);
}

void Apex5400BillAcceptor::disable(){
	digitalWrite(pin_enable_line, HIGH);
}

void Apex5400BillAcceptor::toggle(){
	digitalWrite(pin_enable_line, !digitalRead(pin_enable_line));
}