###defaultValues.py
###Created by Joseph Rollinson, JTRollinson@gmail.com
###Last Modified: 12/07/11
###This contains the constant values for the program.

debug = False


notes = ['C3','D3','E3','F3','G3','A3','B3',
         'C4','D4','E4','F4','G4','A4','B4',
         'C5','D5','E5','F5','G5','A5','B5','C6']
notesStartIndex = 7

freqs = [131,147,165,175,196,220,247,
         262,294,330,349,392,440,494,
         523,587,659,689,784,880,988,1047]

noteToFreq = {}
for i in xrange(len(notes)):
    noteToFreq[notes[i]] = freqs[i]

numberSensors = 6
sensors = ['Sensor %d' % i for i in xrange(numberSensors)]
noteValues = ['Attack','Decay','Sustain','Release','Duration','Mul']
defaultNoteValues = [.01,.2,.5,.1,1,.5]

firstHeight = 10
secondHeight = 30

com = 'COM5'
speed = 9600

calibrationPath = 'calibrations.dat'
helpPath = 'helpText.txt'
helpLength = 50
