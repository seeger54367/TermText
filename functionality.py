#!/usr/bin/python3
from twilio import twiml
from twilio.rest import Client
from datetime import datetime
from curses.textpad import Textbox, rectangle
import curses
import time

#Twilio info
with open('/home/user/Projects/twilioAccountID.txt', 'r') as my_file:
        account_sid = my_file.read().rstrip()
with open('/home/user/Projects/twilioAuth.txt', 'r') as my_file:
        auth_token = my_file.read().rstrip()
myNumber = "+12487205123"
fromNumber = "+12487205123"
toNumber = "+12489189172"
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
messageString = ""
editHeight = 0
editWidth = 0

client = Client(account_sid, auth_token)

def setRecipient():
    toNumber = input("Recieving phone number: ")

def setFromNumber(num):
    global fromNumber
    fromNumber = unique_from_numbers[num]

def getFromNumber():
    return fromNumber

def setToNumber(num):
    global toNumber
    toNumber = unique_from_numbers[num]


def sendMessage(messageBody):
    message = client.messages.create(
        to= str(toNumber),
        from_= str(myNumber),
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
        #if x in phoneBook:
        #    unique_from_numbers.append(phoneBook[x])
        #else:    
        #    unique_from_numbers.append(x)
        unique_from_numbers.append(x)

def getConvoNumbers():
    global recieved_from_numbers
    recieved_from_number = []
    unique_from_number = []
    for sms in client.messages.list():
        recieved_from_numbers.append(sms.from_)
        recieved_from_numbers.append(sms.to)
    unique(recieved_from_numbers)
    unique_from_numbers.remove(myNumber)

def getMessages():
    global contact_messages
    contact_messages = []
    for sms in client.messages.list():
        if (sms.to == toNumber) | (sms.from_ == toNumber):
            sender = sms.from_
            target = sms.to
            message = sms.body
            timestamp = sms.date_sent
            contact_messages.append((timestamp.strftime("%m/%d/%Y, %H:%M:%S"), sender, target, message))

def newContactMessage(myscreen):
    global toNumber
    global editHeight
    global editWidth
    #Send new message to new number
    myscreen.clear()
    myscreen.addstr(0, 0, "Enter newPhoneNumber: EX. +1XXXXXXXXXX (hit Ctrl-G to draft message)")

    addNumberScreen = curses.newwin(editHeight , editWidth, 2,1)
    rectangle(myscreen, 1,0, 1+editHeight+1, 1+editWidth+1)
    #myscreen.refresh()
    newNumBox = Textbox(addNumberScreen)

    ## Let the user edit until Ctrl-G is struck.
    newNumBox.edit()

    ## Get resulting contents
    newNumber = newNumBox.gather()
    toNumber = newNumber

def composeMessage(myscreen):
    global editHeight
    global editWidth
    myscreen.clear()
    myscreen.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

    editwin = curses.newwin(editHeight , editWidth, 2,1)
    rectangle(myscreen, 1,0, 1+editHeight+1, 1+editWidth+1)
    #myscreen.refresh()

    box = Textbox(editwin)

    # Let the user edit until Ctrl-G is struck.
    box.edit()

    # Get resulting contents
    message = box.gather()
    sendMessage(message)

def convoWindow(myscreen, selected_contact):
    convoWindow = curses.newwin(convoHeight, convoWidth, 1, contactWidth + 1)
    convoWindow.clear()
    convoWindow.border(0)
    x = 0
    y = 0
    for idx, current_message in enumerate(reversed(contact_messages)):
        x = 2
        y = 1 + idx
        if y >= convoHeight:
            y = convoHeight - 1
            convoWindow.clear()
            convoWindow.refresh()
        timestamp = current_message[0]
        if current_message[1] in phoneBook:
            sender = phoneBook[current_message[1]]
        else:
            sender = current_message[1]
        target = current_message[2]
        message = current_message[3]
        formated_message = timestamp +" | "+sender+ ":" + message
        try:
            convoWindow.addstr(y,x,formated_message)
        except:
            convoWindow.clear()
            continue
    if toNumber in phoneBook:
        contactHeader = phoneBook[toNumber]
    else:
        contactHeader = toNumber
    convoWindow.addstr(0,convoWidth//2-len(contactHeader),contactHeader)
    myscreen.refresh()
    convoWindow.refresh()

def messageWindow(myscreen, selected_contact):
    messageWindow = curses.newwin(messageHeight, messageWidth, convoHeight +1, contactWidth + 1)
    messageWindow.border(0)
    messageContent = "Select next contact 'J' or DOWN. Select Previous Contact 'K' or UP. Send message to select contact ENTER. quit 'q'."
    messageWindow.addstr(1,1, messageContent)
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
        if number in phoneBook:
            number = phoneBook[number]
        if idx == selected_contact:
            contactsWindow.attron(curses.color_pair(1))
            contactsWindow.addstr(y,x,number)
            contactsWindow.attroff(curses.color_pair(1))
        else:
            contactsWindow.addstr(y,x,number)
    myscreen.refresh()
    contactsWindow.refresh()

def mainDisplay(myscreen):
    global fromNumber
    global MessageWindow
    global recieved_from_numbers
    global messageWidth
    global messageHeight
    global convoHeight
    global convoWidth
    global contactHeight
    global contactWidth
    global current_contact_index
    curses.use_default_colors()
    editWidth = curses.COLS - 5
    editHeight = curses.LINES - 5
    contactHeight = curses.LINES - 2
    contactWidth = 15
    messageWidth = curses.COLS - contactWidth - 2 
    messageHeight = 5
    convoHeight = curses.LINES - messageHeight - 3
    convoWidth = curses.COLS - contactWidth - 2
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    myscreen.keypad(True)
    myscreen.border(0)
    current_contact_idx = 0
    contactsWindow(myscreen, current_contact_idx)
    messageWindow(myscreen, current_contact_idx)
    convoWindow(myscreen, current_contact_idx)
    curses.napms(2000)
    while 1:
        key = myscreen.getch()
        myscreen.clear()
        if key == curses.KEY_ENTER or key in [10,13]:
            #Send new message
            FromNumber=myNumber
            setToNumber(current_contact_idx)
            myscreen.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")
            editwin = curses.newwin(editHeight , editWidth, 2,1)
            rectangle(myscreen, 1,0, 1+editHeight+1, 1+editWidth+1)
            myscreen.refresh()
            composeMessage(myscreen)

        if key == ord('a'):
            #Add new number
            FromNumber=myNumber
            myscreen.addstr(0, 0, "Enter newPhoneNumber: EX. +1XXXXXXXXXX (hit Ctrl-G to draft message)")
            addNumberScreen = curses.newwin(editHeight , editWidth, 2,1)
            rectangle(myscreen, 1,0, 1+editHeight+1, 1+editWidth+1)
            myscreen.refresh()
            newContactMessage(myscreen)

            #Send new message to new number
            myscreen.clear()
            myscreen.refresh()
            myscreen.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")
            editwin = curses.newwin(editHeight , editWidth, 2,1)
            rectangle(myscreen, 1,0, 1+editHeight+1, 1+editWidth+1)
            myscreen.refresh()
            composeMessage(myscreen)
            getConvoNumbers()
        elif key == curses.KEY_UP and current_contact_idx > 0:
            current_contact_idx -=1
            setToNumber(current_contact_idx)
            getMessages()
        elif key == ord('K') and current_contact_idx > 0:
            current_contact_idx -=1
            setToNumber(current_contact_idx)
            getMessages()
        elif key == ord('J') and current_contact_idx < len(unique_from_numbers)-1:
            current_contact_idx +=1
            setToNumber(current_contact_idx)
            getMessages()
        elif key == curses.KEY_DOWN and current_contact_idx < len(unique_from_numbers)-1:
            current_contact_idx +=1
            setToNumber(current_contact_idx)
            getMessages()
        elif key == ord('q'):
            break

        myscreen.refresh()
        convoWindow(myscreen, current_contact_idx)
        contactsWindow(myscreen, current_contact_idx)
        messageWindow(myscreen, current_contact_idx)

def callDisplay():
    curses.wrapper(mainDisplay)

def main():
    getConvoNumbers()
    setToNumber(current_contact_idx)
    getMessages()
    callDisplay()

main()
