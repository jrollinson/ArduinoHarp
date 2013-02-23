###calibration.py
###Created by Joseph Rollinson, JTRollinson@gmail.com
###Last Modified: 12/07/11
###Collects the calibration information through a window.
###Also has function to collect zero value data


import arduino, files
from Tkinter import *

def calibrate(i,firstHeight,secondHeight,com,speed):
    '''run this to run a calibration window for sensor index i'''
    root = Tk()
    window = calibrationWindow(i,firstHeight,secondHeight,com,speed,root)
    window.master.title("Calibration")
    root.mainloop()
    try: root.destroy()
    except: pass
    return window.getCalibration()

class calibrationWindow(Frame):
    '''the window used for calibrating a sensor'''
    def __init__(self,nSensor,firstHeight,secondHeight,com,speed,master=None):
        Frame.__init__(self, master) #runs the master object's init function
        self.grid(sticky=N+S+E+W) #allows the app to change shape
        self.createWidgets() #creates all the pieces
        self.i = nSensor #which sensor to read
        self.firstHeight = firstHeight
        self.secondHeight = secondHeight
        self.firstReading = None
        self.secondReading = None
        self.kG = None
        self.kO = None
        self.arduino = arduino.arduino(com,speed)
        

    def createWidgets(self):
        '''creates all the parts of the gui'''
        self.message = Label(self,text='To calibrate press button')
        self.message.grid(row = 1, column = 0)
        self.mainButton = Button(self,
                               text = "Calibrate",
                               command = self.beginCalibrate)
        self.mainButton.grid(row = 2,
                           column = 0,
                           sticky = E+W)


    def beginCalibrate(self):
        '''called when calibrate button first pressed.  Sets  up everything for first reading'''
        self.mainButton.config(command = self.getFirstReading)
        self.message.config(text = "Please put your hand %dcm above the sensor and press OK" % (self.firstHeight))
    def getFirstReading(self):
        '''called on second calibrate button press.  Gets the first reading'''
        self.firstReading = self.arduino.getRawRange(self.i)
        self.mainButton.config(command = self.getSecondReading)
        self.message.config(text = "Now please put your hand %dcm above the sensor and press OK" % (self.secondHeight))
    def getSecondReading(self):
        '''called on the last calibrate button press.  Collects data'''
        self.secondReading = self.arduino.getRawRange(self.i)

        x1 = self.firstReading
        x2 = self.secondReading
        d1 = self.firstHeight
        d2 = self.secondHeight
        #these formulas come from this website
        #http://www.barello.net/Papers/GP2D02
        #Ko = (D'X' - DX)/(D' - D)
        self.kO = 1.0*(d2*x2 - d1*x1)/(d2-d1)
        #Kg = (X'-X) D'D/(D-D')
        self.kG = 1.0*(x2-x1)*(d2*d1)/(d1-d2)
        
        self.mainButton.config(command = self.quitButton)
        self.mainButton.config(text = "Quit")
        self.message.config(text = "kG=%d and kO=%d  Please press quit" % (self.kG,self.kO))

    def quitButton(self):
        '''last button press, quits program'''
        '''closes the arduino port and quits the mainloop'''
        self.arduino.close()
        self.quit()
        
    def getCalibration(self):
        '''returns the floats (kG, kO) where the correct reading in cm is
        D = kG/(x-kO)'''
        return self.kG,self.kO


def zeroValues(com,speed):
    '''opens a window and gets the values that will zero the sensors'''
    root = Tk()
    window = zeroWindow(com,speed,root)
    root.mainloop()
    return window.getZeroes()

class zeroWindow(Frame):
    '''window for collecting zero data'''
    def __init__(self,com,speed,master=None):
        Frame.__init__(self, master) #runs the master object's init function
        self.grid(sticky=N+S+E+W) #allows the app to change shape
        self.ard = arduino.arduino(com,speed)
        self.master = master
        self.master.title("Zeroing")
        self.createWidgets()
        self.zeroes = []
    def createWidgets(self):
        '''creates the parts of the gui'''
        self.instructions = Label(self,text='Please remove everything in the way\nof the sensor and press continue')
        self.instructions.grid(row=0,column=0)
        self.continueButton = Button(self,
                                     text='Continue',
                                     command=self.pressContinue)
        self.continueButton.grid(row=1,column=0)
        
    def pressContinue(self):
        '''what happens when continue is pressed.  Gets ranges and closes program'''
        self.zeroes = self.ard.getRawRanges()
        self.ard.close()
        self.master.destroy()
        self.quit()
    def getZeroes(self):
        '''returns the zero values'''
        return self.zeroes
