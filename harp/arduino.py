###arduino.py
###Created by Joseph Rollinson, JTRollinson@gmail.com
###Last Modified: 12/07/11
###Requires: pySerial
###This allows communication between the arduino interface and python

import serial
import threading, Queue
import files

class arduino(object):
    '''this connects to the arduino in a six sensor interface.  It runs a thread
    constantly collecting results from the arduino.  It returns the most recent
    reading from the sensor'''
    def __init__(self,com,speed,path=None):
        self.s = serial.Serial(com,speed)
        self.isRunning = False
        self.start()
        if path == None:
            self.isCalibrated = True
        else:
            self.calibrationData = files.getCalibrationData(path)
            self.isCalibrated = False
    def start(self):
        '''begins a new thread that obtains the data from serial connection'''
        def arduinoConnection(serialconn,queue,closingEvent,callingEvent):
            '''the thread that is run'''
            while not closingEvent.isSet(): #runs only when closingEvent isn't set
                result = serialconn.readline()[:-2]
                #result gets rid of the  closing chars
                result = [ord(char) for char in result]
                if callingEvent.isSet(): #if this is set, puts data in stream
                    queue.put(result) #puts the data in
                    callingEvent.clear()#clears the event

        if self.isRunning: raise
        self.isRunning = True
        self.sensorStream = Queue.Queue(1) #where the new thread puts data
        self.closingEvent = threading.Event() #closes the stream when set
        self.callingEvent = threading.Event() #tells thread to put data in stream
        self.subP = threading.Thread(target = arduinoConnection,
                                     args = (self.s,
                                             self.sensorStream,
                                             self.closingEvent,
                                             self.callingEvent))
        self.subP.start()
    def nSensors(self):
        '''returns the number of sensors sending data to the computer'''
        return len(self.getRawRanges())
    def getRawRanges(self):
        '''returns a list of the raw ranges of the sensors'''
        if self.isRunning == False: raise Exception
        #tells the arduino to put the data into the queue
        self.callingEvent.set()
        #returns and clears the data in the queue
        return self.sensorStream.get()
    def getRawRange(self,i):
        '''returns an int of the raw range of one sensor'''
        return self.getRawRanges()[i]
    def getCalibratedRanges(self):
        '''returns a list of the calibrated ranges of the sensors'''
        if self.isRunning == False: raise Exception
        if self.isCalibrated == False: raise Exception
        rawRange = self.getRawRanges()
        calibratedRange = []
        data = self.calibrationData
        #function: D = kG/(x-kO)
        for i in xrange(len(rawRange)):
            #if there is no data for a sensor, it returns a none value for that sensor
            if data[i] == (None,None):
                calibratedRange.append(None)
            #otherwise, calculates the calibratedRanges
            else:
                # data : (kG,kO)
                # D = Kg/(X - Ko)
                if rawRange[i] - data[i][1] == 0: result = 0
                else:
                    result = data[i][0]/(rawRange[i] - data[i][1])
                if result < 0: result = 0  #distance must be >= 0
                calibratedRange.append( result )
        return calibratedRange
    def getCalibratedRange(self,i):
        '''returns the float value for the calibrated range of sensor index i'''
        return self.getCalibratedRanges[i]
    
    def close(self):
        '''closes down the stream and the sensor'''
        if self.isRunning == False: raise Exception
        self.closingEvent.set()
        self.subP.join()
        self.s.close()
    
    
        
        

def checkSerial(com):
    '''returns True if the serial connection is open and ready for business'''
    try:
        s = serial.Serial(com)
        s.close()
    except:
        return False
    return True
