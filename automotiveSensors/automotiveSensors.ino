/* Author: Grace Yoo, CpE
 * File Name: decodeSensorData.ino
 * Description: Software used to decode automative sensor data.
 * Team: Group 3, GOLD Team
 * Group Members: Cecilie Barreto, CpE
 *                Drew Curry, EE
 * Project: Florida Solar Beach Buggy Challenge
 * Sponsor: Duke Energy
 * School: University of Central Florida
 * Professors: Dr. Richie and Dr. Lei Wei
 * 
 * Notes to self: Sensor Data comes in in LSB complement order */

// Global Variables
unsigned long pulseLength;          // Stores the Pulse Width of PWM Signal
byte          bitValue;             // Temporary holds individual bit value
byte          sensorData[16];       // Full two bytes sent by the sensors 
byte          portAddress     = 0;  // Byte used for nibble (last 4 bits)
byte          distanceWhole   = 0;  // Byte used for nibble (last 4 bits)
byte          distanceDecimal = 0;  // Byte used for nibble (last 4 bits)
int           bitCount        = 0;  // Counts the number of bits processed

// Define used pins
const int  dataPin   =  4;
const int  ledPin    = 13;

// Port Addresses
const byte portJOne   = B1010;  // XXXX XXXX 1010 XXXX
const byte portJTwo   = B1110;  // XXXX XXXX 1110 XXXX
const byte portJThree = B0110;  // XXXX XXXX 0110 XXXX
const byte portJFour  = B0010;  // XXXX XXXX 0010 XXXX

// Set input and output pins
void setup()
{
  pinMode(dataPin, INPUT);   // Set data pin (4) as input
  pinMode(ledPin, OUTPUT);   // Set led pin (13) as output (Used to see active communication, not necessary)
  Serial.begin(9600);        // Set baud rate, can be changed if necessary

}

/////////////////////////////////////////////////////////////////////////
// Sensor data is sent in LSB order
// Data need to be reversed in order to be process
// LSBToMSB function reverses the order nibble (4 bits)
/////////////////////////////////////////////////////////////////////////
byte LSBToMSB(byte nibble)
{
  byte reversedNibble = 0;
  byte temp           = 0;

  for(int x = 0; x < 4; x++)
  {

    temp   = nibble & 0x01;                // Mask all bits except 8th bit
    nibble = nibble >> 1;                  // Shift right to move remove bit already used
    reversedNibble = reversedNibble << 1;  // Shift left ot the return nibble
    
    // If the bit was 1, add one to the return nibble
    if (temp == 1)                         
    {
      reversedNibble = reversedNibble + 1;
    }
  }

  return reversedNibble;                   // Return product nibble
}


/////////////////////////////////////////////////////////////////////////
// PrintDistance calls LSBToMSB to reverse the bits,
// then finds the complement of the nibbles, masks out the first 4 bits,
// and prints the distance to Serial.
/////////////////////////////////////////////////////////////////////////
void PrintDistance()
{
  // Reverse the nibble
  distanceWhole   = LSBToMSB(distanceWhole);
  distanceDecimal = LSBToMSB(distanceDecimal);

  // Get the complement of the nibble
  distanceWhole   = ~distanceWhole;
  distanceDecimal = ~distanceDecimal;

  // Mask out the first nibble
  distanceWhole   = distanceWhole   & 0x0F;
  distanceDecimal = distanceDecimal & 0x0F;

  // Print the distance found by the sensor to the screen in (meters)
  //Serial.print(distanceWhole, DEC);
  //Serial.print(".");
  //Serial.println(distanceDecimal,DEC);
  

  String distWhole = (String)distanceWhole;
  String distDecimal = (String)distanceDecimal;
  
  String distanceString = distWhole + distDecimal;
  Serial.println(distanceString);
}

// Arduino's version of main(), but looped, so like a forever for loop
void loop()
{ 

  // Look for the starting data pulse
  while(bitCount == 0 && pulseLength < 800)
  {
    pulseLength = pulseIn(dataPin, HIGH);  // Continue grabbing pulse width until starting signal is found
    distanceWhole   = 0;                   // Reset values for the next sensor reading
    distanceDecimal = 0;                   // Reset values for the next sensor reading
    portAddress     = 0;                   // Reset values for the next sensor reading
  }
  
  pulseLength = pulseIn(dataPin, HIGH);    // Grab the next signal

  //If pulse is less than 320 microsecounds, Bit = 0;
  if(pulseLength <= 320) 
  {
    bitValue = B0;
    digitalWrite(ledPin, LOW);             // Just to see if we are receiving data, not necessary
    sensorData[bitCount] = bitValue;       // Put bit value in sensorData array
    bitCount++;                            // Increase bit count
  }

  // If pulse is greater than 450 microsecounds, Bit = 1;
  if(pulseLength >= 450 )
  {
    bitValue = B1;
    digitalWrite(ledPin, HIGH);            // Just to see if we are receiving data, not necessary
    sensorData[bitCount] = bitValue;       // Put bit value in sensor data array
    bitCount++;                            // Increase bit count
  }

  // If we've reached the end of the PWM signal, process binary data
  if(bitCount == 16)
  {
    bitCount = 0;                          // Reset bit count for next sensor reading
    
    for (int i = 0; i < 16; i++)
    {
      bitValue = sensorData[i];            // Grab bit stored in sensor data array
      //Debug print that prints the two bytes sent by the sensor
      //Serial.print(sensorData[i], BIN);

      // 0000 XXXX XXXX XXXX
      if (i < 4)
      {
        distanceDecimal = distanceDecimal << 1;
        bitWrite(distanceDecimal, 0, bitValue);
      }

      // XXXX 0000 XXXX XXXX
      if (i > 3 && i < 8)
      {
        distanceWhole = distanceWhole << 1;
        bitWrite(distanceWhole, 0, bitValue);
      }

      // XXXX XXXX 0000 XXXX
      if (i > 7 && i < 12)
      {
        bitWrite(portAddress, 0, bitValue);
        portAddress = portAddress & 0X0F;

        // When you reach the end of the port address, determine the port and print distance
        if (i == 11)
        {
          switch(portAddress)
          {
            case portJOne:
              Serial.print("1010 ");
              PrintDistance();
              break;
            case portJTwo:
              Serial.print("1110 ");
              PrintDistance();
              break;
            case portJThree:
              Serial.print("0110 ");
              PrintDistance();
              break;
            case portJFour:
              Serial.print("0010 ");
              PrintDistance();
              break;
          }
        }
        // If you have not reached the end of the port address, shift left to make room but next bit of address
        portAddress = portAddress << 1;
      }
      
      // XXXX XXXX XXXX 0000
      // The last four digits of the sensor data has yet to be decoded for use
      // The distance and port address is all that is needed for our purposes
      if (i > 11 && i <16)
      {
        //Serial.println("Last Four Digits still need decoding.");
      }
    }
  }
}
