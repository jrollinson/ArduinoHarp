###helpWindow.py
###Created by Joseph Rollinson, JTRollinson@gmail.com
###Last Modified: 12/07/11
###Runs a window that displays the text in the help file


from Tkinter import *
import os

def main(helpPath,length):
    root = Tk()
    helpText = getHelpDoc(helpPath,length)
    window = helpWindow(helpText,root)
    root.mainloop()


def getHelpDoc(path,length):
    '''Get's the help doc from the path'''
    if not os.path.isfile(path): raise
    #reads the file into text
    with open(path) as f:
        text = f.read()

    #adds newlines
    i = length
    while i < len(text):
        while (text[i] != ' ') and (text[i] != '\n') and i >= 0:
            i -= 1
        if text[i] == '\n' or i == 0:
            i += length
        text = text[:i] + '\n' + text[i:]
        i += length
    return text
        
            
            

class helpWindow(Frame):
    def __init__(self,helpText,master=None,):
        Frame.__init__(self, master) #runs the master object's init function
        self.grid(sticky=N+S+E+W) #allows the app to change shape
        master.title('Help')
        self.master = master
        self.createWidgets(helpText)

    def createWidgets(self,helpText):
        helpLabel = Label(self,text=helpText,justify=LEFT)
        helpLabel.grid(row=0,column=0)
        quitButton = Button(self,text='Close',command=self.quitButton)
        quitButton.grid(row=1,column=0)

    def quitButton(self):
        self.master.destroy()
        
        
        
    
