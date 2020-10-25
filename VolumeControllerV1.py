
from tkinter import Tk
from tkinter import IntVar
from tkinter import Checkbutton
from tkinter import Button
import keyboard # for keylogs
import pythoncom
from threading import Semaphore
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
buttonList = []
volumeList = []
def makeSelection():
    global buttonList, volumeList
    bList = []
    root =Tk()
    root.title("VolumeController")


    #d = Button(root, text="Refresh", command=None)
    #d.pack()
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process:
            bList.append(session.Process.name())

    for i in range(0, len(bList)):
        bList[i] = bList[i].strip(".exe")

    for g in bList:
        if g not in buttonList:
            buttonList.append(g)

    def click_me():
        for i in checkList:
            if i[1].get() != 0 and volumeList.count(i[0]) == 0:
                volumeList.append(i[0])
            elif volumeList.count(i[0]) != 0 and i[1].get() == 0:
                try:
                    volumeList.remove(i[0])
                except:
                    pass

    def refresh():
        global checkList
        for check in checkList:
            check[2].delete()
        checkList = []
        buttonList = []
        b.delete()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process:
                buttonList.append(session.Process.name())


        for i in range(0, len(buttonList)):
            buttonList[i] = buttonList[i].strip(".exe")

        for i in range(0, len(buttonList)-1):
            if buttonList[i] == buttonList[i+1]:
                buttonList.pop(i)
        for i,j in enumerate(buttonList):
            var = IntVar()
            c = Checkbutton(root, text = j, variable=var)
            checkList.append([j, var, c])

        for check in checkList:
            check[2].pack()

        b.pack()
        #d.pack()



    i=IntVar()
    checkList = []
    for i,j in enumerate(buttonList):
        var = IntVar()
        c = Checkbutton(root, text = j, variable=var)
        checkList.append([j, var, c])

    for check in checkList:
        check[2].pack()

    b = Button(root,text="Apply",command=click_me)
    b.pack()







    root.geometry("350x200+120+120")

    root.mainloop()
class Keylogger:
    def __init__(self, interval):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        # this is the string variable that contains the log of all
        # the keystrokes within `self.interval`
        self.log = ""
        # for blocking after setting the on_release listener
        self.semaphore = Semaphore(0)

    def callback(self, event):
        pythoncom.CoInitialize()
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 0:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."

            elif name == "f9":
                    sessions = AudioUtilities.GetAllSessions()
                    for session in sessions:
                        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                        if session.Process and session.Process.name().strip(".exe") in volumeList:
                            mVol = volume.GetMasterVolume()
                            if mVol - .05 > 0:
                                volume.SetMasterVolume(mVol - .1, None)
                            else:
                                volume.SetMasterVolume(0, None)

            elif name == "f10":
                    sessions = AudioUtilities.GetAllSessions()
                    for session in sessions:
                        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                        if session.Process and session.Process.name().strip(".exe") in volumeList:
                            #print(session.Process.name() + " yuh")
                            mVol = volume.GetMasterVolume()
                            if mVol + .05 < 1:
                                volume.SetMasterVolume(mVol + .1, None)
                            else:
                                volume.SetMasterVolume(1.0, None)

            elif name == "f8":
                makeSelection()

            elif name == "esc":
                exit()

            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"


        self.log += name



    def start(self):
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        # block the current thread,
        # since on_release() doesn't block the current thread
        # if we don't block it, when we execute the program, nothing will happen
        # that is because on_release() will start the listener in a separate thread
        self.semaphore.acquire()

if __name__ == "__main__":
    keylogger = Keylogger(interval=123412414)
    makeSelection()
    keylogger.start()



