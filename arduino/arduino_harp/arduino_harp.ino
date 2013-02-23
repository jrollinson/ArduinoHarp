#include <GP2D02.h>;
int vIn[] = {2,3,4,5,6,13};
int vOut[] = {8,9,10,11,12,7};
int nSensors = 6;
nGP2D02 sensors(vIn,vOut,nSensors);


void setup()
{
  Serial.begin(9600);
};

void loop()
{
  byte ranges[nSensors];
  sensors.getRawRanges(&ranges[0]);
  for (int i = 0; i < nSensors; i++) 
  {
    Serial.print(ranges[i]);
  }
  Serial.println();
};
