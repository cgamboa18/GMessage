from tkinter import *

ENTRY_LIMIT = 45

class OMessageFrame(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        #initilization setup
        self.grid(row=0, column=1, rowspan=10, sticky="nwse")
        self.configure(bg="dark gray", width=200, height=400)
        self.grid_propagate(False)

        # Labels
        self.limitWarning = Label(text=f"{ENTRY_LIMIT} char lim.", bg="dark gray", fg="black", font=("Arial", 7))

        #Box and Button widgets
        self.entryText = StringVar()
        self.messageTextBox = Entry(width=30, textvariable=self.entryText)
        self.entryText.trace_add("write", lambda *args: self.charLimit())

        self.submitMessageText = Button(text="Send", command= lambda: self.sendMessage(parent.net))

        #Formatting GUI
        self.limitWarning.grid(row=2, column=1, sticky="nw", padx=5, pady=0)
        self.messageTextBox.grid(row=1, column=1, sticky="w", padx=5)
        self.submitMessageText.grid(row=0, column=1, sticky="w", padx=5)

    def charLimit(self):
        #Limits amount of chars that can be typed into the entry field
        if (len(self.entryText.get()) > ENTRY_LIMIT):
            self.messageTextBox.delete(ENTRY_LIMIT, END)

    def sendMessage(self, net):
        #Sends message text to servers database and other clients and recives response
        messageData = ": " + str(self.messageTextBox.get())
        
        if(messageData == ": "):
            reply = "No entry"
        else:
            reply = net.send(messageData)
        
        self.messageTextBox.delete(0, END)

        return reply