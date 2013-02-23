###sensorDisplay.py
###Created by Joseph Rollinson, JTRollinson@gmail.com
###Last Modified: 12/07/11
###Requires: Tkinter,arduino
###Has the functions necessary to display the results of the sensors from the arduino.

from Tkinter import *
import arduino


def rawRange(com,speed):
    '''runs a window that displays the raw range of an ardiuno at com'''
    root = Tk()
    window = rangeWindow(False,com,speed,None,root)
    window.master.title("Raw Range")
    window.timerFired()
    root.mainloop()

def calibratedRange(com,speed,calibratedPath):
    '''runs a window that displays the calibrated range of an ardiuno at com'''
    root = Tk()
    window = rangeWindow(True,com,speed,calibratedPath,root)
    window.master.title("Calibrated Range")
    window.timerFired()
    root.mainloop()

class rangeWindow(Frame):
    '''A window for dislaying the range or calibrated range of the interface'''
    def __init__(self,isCalibrated,com,speed,calibratedPath=None,master=None):
        Frame.__init__(self, master) #runs the master object's init function
        self.grid(sticky=N+S+E+W) #allows the app to change shape
        self.isCalibrated = isCalibrated
        self.calibratedPath = calibratedPath
        self.ard = arduino.arduino(com,speed,calibratedPath)
        self.nSensors = self.ard.nSensors()
        self.isQuit = False 
        self.createWidgets() #creates all the pieces
        
    def createWidgets(self):
        self.sensorData = []
        self.sensorLabels = []
        for i in xrange(self.nSensors):
            labelText = 'Sensor ' + str(i)
            self.sensorLabels.append(Label(self,text=labelText))
            self.sensorLabels[-1].grid(row=1,column=i)
            self.sensorData.append(Label(self,text=''))
            self.sensorData[-1].grid(row=2,column=i)
        self.button = Button(self,text='Quit',command=self.quitButton)
        self.button.grid(row=3,column=0)
        
    def timerFired(self):
        '''updates the values displayed for each sensor'''
        if not self.isQuit:
            if self.isCalibrated:
                ranges = self.ard.getCalibratedRanges()
            else:
                ranges = self.ard.getRawRanges()
            for i in xrange(self.nSensors):
                result = ranges[i]
                if result != None: result = (1.0*int(result*10000)/10000)
                self.sensorData[i].config(text=result)
            self.after(100, self.timerFired)
        else:
            self.ard.close()
            self.master.destroy()
            
    def quitButton(self):
        '''Runs when quit is hit'''
        #uses the timeFired program to close the program quietly.
        self.isQuit = True
