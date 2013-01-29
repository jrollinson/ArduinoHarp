/*
  GP2D02.h - library for the Sharp GP2D02 infrared sensor
  Created by Joseph Rollinson, 4 November 2011
  Public Domain
*/

#ifndef GP2D02_h
#define GP2D02_h

#include "WProgram.h"


class GP2D02
{
  public:
    GP2D02(int pinVin, int pinVout);
    byte getRawRange();
    float getLinearRange();
    //getCm(); 
    float getInches();
  private:
    int _pinVin;
    int _pinVout;
};

class nGP2D02
{
	public:
		nGP2D02(int pinVins[], int pinVouts[],int nSensors);
		void getRawRanges(byte* ranges);
		byte getRawRange(int nSensor);
	private:
		int _pinVins[6]; //max length due to size of arduino
		int _pinVouts[6];
		int _nSensors;
             

};
#endif
