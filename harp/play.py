###play.py
###Created by Joseph Rollinson, JTRollinson@gmail.com
###Last Modified: 12/07/11
###The comnnecting module between sound, the arduino and the gui.
###The main is the music server that plays notes when the arduino is hit.

import music,winsound
import time
import arduino
import threading
import Queue

def main(noteValueEntries,sensorEntries,closeEvent,isWinSound,com,speed,zeros,debug=False):
    '''the main show.  This is run in parallel to the gui when the start button
    is pressed.  This thread has control of multiple threads (one per sensor).
    When the gui sends a signal through event, it ends this thread'''
    
    numberSensors = len(sensorEntries)    
    taskDoneEvents =  []
    distanceQueues = []
    noteThreads = [] #the thread on which the note waits for the event
    for i in xrange(numberSensors): #creates all the threads and events
        taskDoneEvents.append(threading.Event())
        distanceQueues.append(Queue.Queue())
        taskDoneEvents[i].set() #must start set
        newThread = threading.Thread(target=playNote, args=(sensorEntries[i],
                                                            noteValueEntries,
                                                            distanceQueues[i],
                                                            taskDoneEvents[i],
                                                            isWinSound,
                                                            debug))
        noteThreads.append(newThread)
    for thread in noteThreads: thread.start() #starts each thread
    ard = arduino.arduino(com,speed)
    while not closeEvent.isSet(): #this runs as long as the event is not set
                             #the event comes from the thread that started this
                             #thread.
##        if debug: print 'getting ranges...',
        sensorReading = ard.getRawRanges()
        #calibration
        for i in xrange(len(sensorReading)):
            sensorReading[i] = sensorReading[i] - zeros[i]
##        if debug: print 'got'
        #runs for every sensor
##        if debug: print 'sending...',
        for i in xrange(numberSensors):
            if sensorReading[i] > 50: #if it picks up a reading between 0 and 40
##                if debug: print 'sensor',i,sensorReading[i]
                if taskDoneEvents[i].isSet(): #checks to see if the thread has finished playing the last note
                    taskDoneEvents[i].clear() #says that the thread is busy
                    distanceQueues[i].put(sensorReading[i]) #sends the distance data through the queue to the thread
##        if debug: print 'sent'
                    
    ard.close()

def playNote(freq,entries, distanceQueue, taskDoneEvent,isWinSound,debug=False):
    '''Used by main().  It is what is threaded over and over'''
    attack,decay,sustain,release,dur,mul = entries
    if not isWinSound:
        note = music.note(freq,attack,decay,sustain,release,dur,mul)
    while True:
        if not distanceQueue.empty(): #if there is a distance available
            print 'getting data...',
            data = distanceQueue.get() #gets the data from the queue
            print 'got',data
            data = int(data/10)
            if isWinSound:
                winsound.Beep(freq,int(dur*1000))
                if debug: print 'played'
            else:
                if debug: print 'pyo...',
                if debug: print 'data',data,
                note.play(data) #plays a note
                if debug: print 'played'
                time.sleep(dur) #waits for it to finish
            taskDoneEvent.set() #lets the upper thread know that the thread is finished
            

def testNote(freq,noteValueEntries,isWinSound,debug=False):
    #plays a note once, given the valueEntries and frequency of the note to play
    if debug: print freq
    attack,decay,sustain,release,dur,mul = noteValueEntries
    #plays using winSound if isWinSound
    if isWinSound:
        winsound.Beep(freq,int(dur*1000))
    #otherwise, uses pyo
    else: 
        note = music.note(freq,attack,decay,sustain,release,dur,mul)
        note.play()
        time.sleep(dur)
