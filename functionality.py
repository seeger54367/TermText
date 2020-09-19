#!/usr/bin/python3
from twilio import twiml
from twilio.rest import Client
import curses



with open('/home/user/Projects/twilioAccountID.txt', 'r') as my_file:
        account_sid = my_file.read().rstrip()
with open('/home/user/Projects/twilioAuth.txt', 'r') as my_file:
        auth_token = my_file.read().rstrip()
fromNumber = "+12487205123"
toNumber = "+12489189172"
phoneBook = {"+12489189172": "Sal", "+12487205123": "Austin"}

recieved_from_numbers = []

client = Client(account_sid, auth_token)

def setRecipient():
    toNumber = input("Recieving phone number: ")


def composeMessage():
    messageBody=input("Message to send: ")

def sendMessage():
    message = client.messages.create(
        to=toNumber, 
        from_= fromNumber,
        body=messageBody)
    
    print(message.sid)

def getMessages():
    for sms in client.messages.list():
        if (sms.to == toNumber) | (sms.from_ == toNumber):
            print(sms.date_sent,phoneBook[sms.from_],"|",sms.body)
    

def display():
    myscreen = curses.initscr()
    
    myscreen.border(0)
    myscreen.addstr(12, 25, "Python curses in action!")
    myscreen.refresh()
    myscreen.getch()
    
    curses.endwin()






def main():
    getMessages()

main()
