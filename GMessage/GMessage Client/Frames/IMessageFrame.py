from tkinter import *
from _thread import *

class IMessageFrame(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        #initilazation setup
        self.grid(row=0, column=0, rowspan=10, sticky="nwse")
        self.configure(bg="light gray",width=400, height=400)
        self.grid_propagate(False)

        #initialize array for last 10 messages
        self.messageList = []
        for i in range(10):
            self.messageList.append(Label(text="", bg="dark gray", font=("Arial", 8), anchor="w", height=1, width=35))
            self.messageList[i].grid(row=i, column=0, sticky="we", padx=2)

        #display array onto the screen
        start_new_thread(self.threadedUpdate, (parent.net, ))

    def threadedUpdate(self, net):
        while True:
            self.updateMessageFeed(net)
            

    def updateMessageFeed(self, net):
        #This will add last 10 messages to the frame and format GUI
        self.populateMessageList(net)

        for i in range(10):
            if(self.messageList[i].cget("text") == ""):
                self.messageList[i].config(text="", bg="light gray", fg="black")

            elif(self.messageList[i].cget("text").split(":")[0] == "SERVER"):
                self.messageList[i].config(bg="dark gray", fg="midnight blue")

            else:
                self.messageList[i].config(bg="dark gray", fg="black")

    def populateMessageList(self, net):
        #This will be where network is called to get messages from the database
        messagesData = self.requestMessages(net)

        for i in range(10):
            if(messagesData[i] != "NO_NEW_DATA"):
                self.messageList[i].config(text=self.parseData(messagesData[i])) 
            else:
                break

    def requestMessages(self, net):
        #Sends request to servers database recives message data for past 10 messages
        messageReplies = []
        for i in range(10):
            messageReplies.append(net.send(f"LOAD_DATA_REQ:{i}"))
            if(messageReplies[i] == ": "):
                messageReplies[i] = ""
            elif(messageReplies[i] == "NO_NEW_DATA"):
                break

        return messageReplies
    
    @staticmethod
    def parseData(data):
        try:
            return data
        except:
            return ""