###files.py
###Created by Joseph Rollinson, JTRollinson@gmail.com
###Last Modified: 12/07/11
###Has modules for stored calibration data into a file.  

import os,pickle

def createCalibrationFile(path,numberSensors):
    '''Creates the calibration file as [(None,None)]*numberOfSensors'''
    with open(path,'w') as f:
        pickle.dump([(None,None)]*numberSensors,f)
    
        
def getCalibrationData(path):
    '''returns a list of length 2 tuples that were pickled in file at path'''
    #creates the file if it does not exist
    if not os.path.isfile(path):
        createCalibrationFile(path)
    with open(path) as f: #opens file
        try: #tries to read it
            res = pickle.load(f)
            return res
        except:
            #if it can't read it properly, it recreates the file
            #and tries again
            createCalibrationFile(path)
            return getCalibrationData(path)

def updateCalibration(path,newData,i):
    '''updates the calibration data for sensor i'''
    #gets the calibration data from the file
    data = getCalibrationData(path)
    data[i] = newData #updates it
    with open(path,'w') as f: #repickles the data into the file
        pickle.dump(data,f)

def getUncalibratedSensors(path):
    '''returns which sensors are uncalibrated'''
    data = getCalibrationData(path)
    return [i for i in xrange(numberSensors) if data[i]==(None,None)]
