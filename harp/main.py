###main.py
###Created by Joseph Rollinson, JTRollinson@gmail.com
###Last Modified: 12/07/11
###The top level code for the program

import music,gui,Tkinter


def main():
    '''begins the music server and starts the gui'''
    s = music.musicServer()
    music.startServer(s)
    root = Tkinter.Tk()
    app = gui.Application(root)
    root.mainloop()
    
main()
