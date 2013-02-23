###music.py
###Created by Joseph Rollinson, JTRollinson@gmail.com
###Last Modified: 12/07/11
###Requires: pyo
###Turns pyo into a note class that is very easy to run.
###Also contains functions to run pyo music server.

import pyo

class note(object):
    '''creates a note that can be played'''
    def __init__(self,frequency=440, attack=.01, decay=.2, sustain=.5, release=.1, duration=1, mul=1):
        #some of this might not need to be saved later, for space saving.
        self.frequency = frequency
        self.attack    = attack
        self.decay     = decay
        self.sustain   = sustain
        self.release   = release
        self.duration  = duration
        self.mul       = mul
        self.envelope  = pyo.Adsr(attack   = attack,
                                  decay    = decay,
                                  sustain  = sustain,
                                  release  = release,
                                  dur      = duration,
                                  mul      = mul)
        self.mod       = pyo.Sine(freq = 0, mul = 25)
        self.wave      = pyo.Sine(freq = self.frequency + self.mod, mul = self.envelope)
        self.wave.out()
    def play(self,modulation=0):
        '''plays the note'''
        self.mod.setFreq(modulation)
        self.wave.setFreq(self.frequency+self.mod)
        self.envelope.play()
    def setFrequency(self,frequency):
        '''sets the frequency of the note'''
        self.frequncy = frequency
        

##def getNotes():
##    '''returns a list of notes from middle C to the next B'''
##    return map( lambda frequency: note(frequency), freqs)

def musicServer():
    '''Returns a music server'''
    s = pyo.Server().boot()
    return s

def startServer(server):
    server.start()

def stopServer(server):
    server.stop()
    server.shutdown()
    
def guiMusicServer(server):
    '''displays music server's gui'''
    server.gui(locals())
