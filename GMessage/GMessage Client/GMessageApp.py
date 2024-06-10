from tkinter import *

from Frames.IMessageFrame import *
from Frames.OMessageFrame import *
from Network import *

class GMessageApp(Tk):
    def __init__(self):
        super().__init__()

        self.title("GMessage")
        self.geometry("600x400")
        self.resizable(False, False)

        self.net = Network()
        self.inFrame = IMessageFrame(self)
        self.outFrame = OMessageFrame(self)

        self.mainloop()

x = GMessageApp()
