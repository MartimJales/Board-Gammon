//D13      D12
//3v       D11
//REE3     D10
//A0       D9
//A1       D8
//A2       D7
//A3       D6
//A4       D5
//A5       D4
//A6       D3
//A7       D2
//         GND
//REC      RST
//GND      RXB
//5v       TX1

#include <WiFiNINA.h>

int detect(int ddp)
{
  if (ddp >= 100 && ddp <= 300)
  {
    Serial.println("Temos pedra!");
  }
  else
  {
    Serial.println("---");
  }
  return 0;
}

void setup()
{
  Serial.begin(9600);

  pinMode(A0,INPUT);
}

void loop()
{
  //float in = analogRead(A7) * 5/1023;

  detect(analogRead(A0));
}
