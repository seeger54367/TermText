#!/usr/bin/python3
from twilio import twiml
from twilio.rest import Client
import curses

#Twilio info
with open('/home/user/Projects/twilioAccountID.txt', 'r') as my_file:
        account_sid = my_file.read().rstrip()
with open('/home/user/Projects/twilioAuth.txt', 'r') as my_file:
        auth_token = my_file.read().rstrip()
toNumber = "+12487205123"
fromNumber = "+12489189172"
phoneBook = {"+12489189172": "Sal", "+12487205123": "Austin"}
recieved_from_numbers = []
unique_from_numbers = []
contact_messages = []

#Window dimensions
contactHeight = 0
contactWidth = 0
convoHeight = 0
messageWidth = 0
messageHeight = 0
current_contact_idx = 0

client = Client(account_sid, auth_token)

def setRecipient():
    toNumber = input("Recieving phone number: ")

def setFromNumber(num):
    fromNumber = unique_from_numbers[num];

def getFromNumber():
    return fromNumber

def composeMessage():
    messageBody=input("Message to send: ")

def sendMessage():
    message = client.messages.create(
        to=toNumber, 
        from_= fromNumber,
        body=messageBody)
    print(message.sid)

#from https://www.geeksforgeeks.org/python-get-unique-values-list/
def unique(list1): 
    # insert the list to the set 
    list_set = set(list1) 
    # convert the set to the list 
    unique_list = (list(list_set)) 
    for x in unique_list: 
        #print(x), 
        if x in phoneBook:
            unique_from_numbers.append(phoneBook[x])
        else:    
            unique_from_numbers.append(x)


def getConvoNumbers():
    global recieved_from_numbers
    for sms in client.messages.list():
        recieved_from_numbers.append(sms.from_)
        recieved_from_numbers.append(sms.to)
    unique(recieved_from_numbers)
    #for number in unique(recieved_from_numbers)
    #for i in range(len(recieved_from_numbers)):
    #    print(recieved_from_numbers[i])



def getMessages():
    global contact_messages
    for sms in client.messages.list():
        if (sms.to == toNumber) | (sms.from_ == toNumber):
            sender = sms.from_
            target = sms.to
            message = sms.body
            timestamp = sms.date_sent
            contact_messages.append((timestamp, sender, target, message))

def convoWindow(myscreen, selected_contact):
    convoWindow = curses.newwin(convoHeight, convoWidth, 1, contactWidth + 1)
    convoWindow.clear()
    convoWindow.border(0)
    for idx, current_message in enumerate(contact_messages):
        x = 1
        y = 1 + idx
        sender = current_message[0]
        target = current_message[1]
        #timestamp = current_message[2]
        message = current_message[3]
        #formated_message = " | "+sender+ ":" + message
        convoWindow.addstr(y,x,message)
    #contactHeader = unique_from_numbers[selected_contact]
    contactHeader = fromNumber
    convoWindow.addstr(0,0,contactHeader)
    myscreen.refresh()
    convoWindow.refresh()

def messageWindow(myscreen):
    messageWindow = curses.newwin(messageHeight, messageWidth, convoHeight +1, contactWidth + 1)
    messageWindow.border(0)
    messageWindow.addstr(1,1, "Plese type your message")
    myscreen.refresh()
    messageWindow.refresh()

def contactsWindow(myscreen, selected_contact):
    contactsWindow = curses.newwin(contactHeight, contactWidth, 1, 1)
    contactsWindow.clear()
    #contactsWindow.immedok(True)
    contactsWindow.border(0)
    myscreen.attron(curses.color_pair(1))
    #contactMid = contactWidth/0.25
    contactsWindow.addstr(0,3,"Contacts")
    for idx, number in enumerate(unique_from_numbers):
        x = contactWidth//2 - len(number)//2
        y = 1 + idx
        if idx == selected_contact:
            contactsWindow.attron(curses.color_pair(1))
            contactsWindow.addstr(y,x,number)
            contactsWindow.attroff(curses.color_pair(1))
        else:
            contactsWindow.addstr(y,x,number)
    myscreen.refresh()
    contactsWindow.refresh()

def mainDisplay(myscreen):
    global recieved_from_numbers
    global messageWidth
    global messageHeight
    global convoHeight
    global convoWidth
    global contactHeight
    global contactWidth
    global current_contact_index
    contactHeight = curses.LINES - 2
    contactWidth = 15
    messageWidth = curses.COLS - contactWidth - 2 
    messageHeight = 5
    convoHeight = curses.LINES - messageHeight - 2
    convoWidth = curses.COLS - contactWidth - 2
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    myscreen.keypad(True)
    myscreen.border(0)
    current_contact_idx = 0
    contactsWindow(myscreen, current_contact_idx)
    messageWindow(myscreen)
    convoWindow(myscreen, current_contact_idx)
    #Contacts Window
    #contactsWindow.addstr(1,1,"Test")
    #myscreen.refresh()
    #contactsWindow.refresh()
    #myscreen.attroff(curses.color_pair(1))
    curses.napms(2000)
    while 1:
        key = myscreen.getch()
        myscreen.clear()
        if key == curses.KEY_UP and current_contact_idx > 0:
            current_contact_idx -=1
            setFromNumber(current_contact_idx)
            getMessages()
        elif key == curses.KEY_DOWN and current_contact_idx < len(unique_from_numbers):
            current_contact_idx +=1
            setFromNumber(current_contact_idx)
            getMessages()

        contactsWindow(myscreen, current_contact_idx)
        messageWindow(myscreen)
        convoWindow(myscreen, current_contact_idx)
        myscreen.refresh()
        curses.napms(2000)

    
def callDisplay():
    curses.wrapper(mainDisplay)


def main():
    #print(getConvoNumbers())
    getConvoNumbers()
    #callDisplay()
    #for idx, number in enumerate(unique_from_numbers):
    #        print(unique_from_numbers[idx])
    current_contact_idx = 0
    print(current_contact_idx)
    print(getFromNumber())
    current_contact_idx = 1
    print(current_contact_idx)
    setFromNumber(current_contact_idx)
    print(getFromNumber())

main()
