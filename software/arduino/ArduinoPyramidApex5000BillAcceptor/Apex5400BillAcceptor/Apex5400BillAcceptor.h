#include <ReceiveOnlySoftwareSerial.h> //http://gammon.com.au/Arduino/ReceiveOnlySoftwareSerial.zip
#include <Arduino.h>

#ifndef APEX5400BILLACCEPTOR_H
#define APEX5400BILLACCEPTOR_H

struct codeMap{
	int code;
	char description[12];
};

class Apex5400BillAcceptor{ 
	
	private:
		int pin_enable_line;
		int pin_interrupt_line;
		int pin_send_line;		
		int pin_ttl_rx;

		struct codeMap codes[13] = {
			{0x81, "$1 Credit"},
			{0x82, "Not Used"},
			{0x83, "$5 Credit"},
			{0x84, "$10 Credit"},  
			{0x85, "$20 Credit"},  
			{0x86, "$50 Credit"},  
			{0x87, "$100 Credit"},    
			{0x88, "Reserved"},      
			{0x89, "Vend"},      
			{0x8A, "Return"},      
			{0x8B, "Reject"},      
			{0x8C, "Failure"},      
			{0x8D, "Full or Jam"}
		};
		
	public:
		ReceiveOnlySoftwareSerial *mySerial;
		Apex5400BillAcceptor(int, int, int, int);
	
		int checkForBill();
		
		char* getDescription(int);
		
		void enable();
		
		void disable();
		
		void toggle();	
};
#endif