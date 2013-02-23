###gui.py
###Created by Joseph Rollinson, JTRollinson@gmail.com
###Last Modified: 12/07/11
###The main gui of the program.  It is the hub of the program

import play,calibration,sensorDisplay,arduino,helpWindow,stolenCode
import threading,time
from defaultValues import *
from Tkinter import *       
import tkMessageBox

class Application(Frame):
    #This is the framework for the application
    def __init__(self,master=None):
        #creates a list of defaults for entries
        #set to the empty string if nothing there
        Frame.__init__(self, master) #runs the master object's init function
        self.grid(sticky=N+S+E+W) #allows the app to change shape
        master.title("Musical Instrument")
        self.isWinSound = False
        error = self.createWidgets() #creates all the pieces
        self.isRunning = False #whether the instrument program is running or not
        #makes sure it is connected to the serial
        self.checkArduino(error)
        

    def checkArduino(self,error=False):
        '''tries to open an arduino, if error=False,
        it skips this step, shows the error message step and quits'''
        if (error == True) or (not arduino.checkSerial(self.getCom())):
            answer = tkMessageBox.showwarning("COM connection",
                                              "Please connect your arduino")
            self.master.destroy()
            
    def createWidgets(self):
        '''called in the init, creates all widgets'''
        #this set of functions 
        def createLabel(text,row,col):
            '''Creates a label with text at row,col in the application's grid'''
            newLabel = Label(self,text=text)
            newLabel.grid(row=row,column=col)
            return newLabel
        def createEntry(defaultText,row,col):
            '''Creates an entry with a starting text'''
            newEntry = Entry(self,width=10)
            newEntry.grid(row=row,column=col,columnspan=1)
            if defaultText != None: #adds default values to the entry box
                newEntry.insert(0,str(defaultText))
            return newEntry
        def createButton(text,command,row,column):
            '''Creates a button with text and goes to a command function'''
            newButton = Button(self,text=text,command=command)
            newButton.grid(row=row,column=column,sticky=E+W)
            return newButton
        def createRadioButton(text,command,row,col,variable,value):
            '''creates a radio button, connected to function command'''
            newButton = Radiobutton(self,
                                    command = command,
                                    text=text,
                                    variable = variable,
                                    value = value)
            newButton.grid(row=row,column=col)
            return newButton
        def createSpinbox(values,row,col,width=20):
            '''creates a spin box connected to values.  Returns the spin box'''
            newSpinBox = Spinbox(self,values=tuple(values),width=width)
            newSpinBox.grid(row=row,column=col)
            return newSpinBox
        def createDropdown(values,row,col):
            '''creates a dropbox menu with values'''
            newStringVar = StringVar()
            if len(values) > 0:
                newStringVar.set(values[0])
            newDropdown = OptionMenu(self,newStringVar, *values)
            newDropdown.grid(row=row,column=col)
            return newDropdown,newStringVar

	#creates the top level and weights everything
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)            
        top.columnconfigure(0, weight=1)         
        self.rowconfigure(0, weight=1)           
        self.columnconfigure(0, weight=1)

        #creates the default entry boxes in a dict with their identifiers
        #creates each row at the same time
        self.noteValueEntries = dict()
        #creates the entries
        for i in xrange(len(noteValues)):
            createLabel(noteValues[i],i+1,0)
            
            newEntry = createEntry(defaultNoteValues[i],i+1,1)
            self.noteValueEntries[noteValues[i]] = newEntry

        #create note pickers
        self.sensorEntries = []
        self.sensorButtons = []
        self.calibrationButtons = []
        for i in xrange(len(sensors)):
            createLabel(sensors[i],i+1,2)
            newSpinbox = createSpinbox(notes,row=i+1,col=3,width=5)
            for j in xrange(i+notesStartIndex):
                newSpinbox.invoke('buttonup')
            self.sensorEntries.append(newSpinbox)
        f = self.playButton 
        self.sensorButtons.append(createButton("Play",lambda: f(0),1,4))
        self.sensorButtons.append(createButton("Play",lambda: f(1),2,4))
        self.sensorButtons.append(createButton("Play",lambda: f(2),3,4))
        self.sensorButtons.append(createButton("Play",lambda: f(3),4,4))
        self.sensorButtons.append(createButton("Play",lambda: f(4),5,4))
        self.sensorButtons.append(createButton("Play",lambda: f(5),6,4))

        #creates the radio buttons for winSound or Pyo
        self.buttonInfo = IntVar()
        self.winSoundButton = createRadioButton('WinSound',
                                                self.radioButtonPress,
                                                7,
                                                0,
                                                self.buttonInfo,
                                                1)
        self.winSoundButton.deselect()
        self.pyoButton = createRadioButton('Pyo (beta)',
                                           self.radioButtonPress,
                                           7,
                                           1,
                                           self.buttonInfo,
                                           0)
        self.pyoButton.select()
        
        #creates the buttons on the row beneath the entries
        #the i+2 makes the row the one beneath the entries above
        try:
            values = tuple(list(stolenCode.enumerate_serial_ports()))
        except:
            return True
        if len(values) == 0:
            #ends program early because it is not connected to any com port
            return True #this value will be sent to check arduino
        self.comValue = createDropdown(values,8,0)[1] #just need the string var
        self.startButton = createButton('Start',self.start,8,1) 
        self.stopButton = createButton('Stop',self.stop,8,2)
        self.stopButton.config(state=DISABLED) #the stop button can't be used
        rawRangeF = lambda: sensorDisplay.rawRange(com,speed)
        createButton('Raw Range',rawRangeF,8,3)
        helpF = lambda: helpWindow.main(helpPath,helpLength)
        createButton('Help',helpF,8,4)
        return False

    def radioButtonPress(self):
        '''runs if a radio button is pressed'''
        if self.buttonInfo.get() == 0:
            self.isWinSound = False
            for entry in self.noteValueEntries:
                self.noteValueEntries[entry].config(state=NORMAL)
        elif self.buttonInfo.get() == 1:
            self.isWinSound = True
            for entry in self.noteValueEntries:
                if entry != 'Duration':
                    self.noteValueEntries[entry].config(state=DISABLED)
        else: raise

    def getCom(self):
        return self.comValue.get()
        
    def getNoteValueEntry(self,identifier):
        '''gets the entry in the field connected to identifier'''
        return self.noteValueEntries[identifier].get()

    def getAllNoteValueEntries(self):
        '''gets all the entries in the app'''
        f = lambda noteValueName: float(self.getNoteValueEntry(noteValueName))
        return map(f,noteValues)

    def getAllSensorEntries(self):
        '''get entries for sensor data'''
        entryData = map(lambda entry: entry.get(),self.sensorEntries)
        result = []
        for item in entryData:
            try:
                result.append(int(item))
            except:
                result.append(noteToFreq[item])
        return result
                
            
    def validateEntries(self):
        '''validates all entries and produces error message box if not valid'''
        #checks if note values are good
        try:
            for noteValueName in noteValues:
                float(self.getNoteValueEntry(noteValueName))
        except:
            #the message box
            tkMessageBox.showwarning("Error","Invalid Value Inputs")
            return False

        #checks if sensor values are good
        for entry in [entry.get() for entry in self.sensorEntries]:
            try:
                int(entry) #tries to make it into an int
            except:
                if not entry in notes: #make sure that the entry is a note
                    if debug: print entry
                    tkMessageBox.showwarning("Error","Invalid Note Inputs")
                    return False                
        return True

    def playButton(self,i):
        '''runs when any play button is pressed'''
        if self.validateEntries():
            freq = self.getAllSensorEntries()[i]
            if self.isRunning: return
            play.testNote(freq,
                          self.getAllNoteValueEntries(),
                          self.isWinSound,
                          debug=debug)

#not used in this version
##    def calibrateButton(self,i):
##        '''opens a new window that calibrates sensor number i.
##        It saves the calibration in file.'''
##        calibration.calibrate(i,
##                              firstHeight,
##                              secondHeight,
##                              self.getCom(),
##                              speed,
##                              calibrationPath)
        
    def start(self):
        '''runs when start button is hit'''
        self.checkArduino()
        self.isRunning = True
        if self.validateEntries() == False: return
        #changes all the buttons to their right state
        self.startButton.config(state = DISABLED)
        self.stopButton.config(state = NORMAL)
        if debug: print self.getCom(), type(self.getCom())
        zeros = calibration.zeroValues(self.getCom(),speed) #zeros the values.
        #creates a thread
        #this Event object allows this class
        #to send information to the other thread
        self.subPEvent = threading.Event() 
        if debug:print 'started thread'
        #creates a new thread to run music
        self.subP = threading.Thread(target=play.main,
                                     args=(self.getAllNoteValueEntries(),
                                           self.getAllSensorEntries(),
                                           self.subPEvent,
                                           self.isWinSound,
                                           self.getCom(),
                                           speed,
                                           zeros,
                                           debug))
        self.subP.start() #starts the new thread
            
    def stop(self):
        '''runs when stop button is hit'''
        self.isRunning = False
        #sets all the buttons
        self.startButton.config(state = NORMAL)
        self.stopButton.config(state = DISABLED)
        self.subPEvent.set() #sends a signal to the thread to stop
        self.subP.join() #joins the two threads


