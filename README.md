# TermText

## A terminal messaging application built for GrizzHacks5 at Oakland University

### Authors: Austin Daniell, Sal Trupiano

This project provides a terminal user interface for the popular Twilio messaging service. This project was created for GrizzHacks5 at Oakland University.

### Application Features:
- Terminal User Interface that populates a list with the user's Twilio SMS message conversations.
- Users can send, receive, and view their Twilio SMS messages.
- Users can add a new phone number to send a message to.
- Users can switch to different conversations using shortkeys/arrowkeys.
- Uses Twilio's API to read in and send SMS conversations.
- Users can use this application directly though their terminal, no Graphial User Interface required!

### Technologies/Frameworks Used:
- Python 3
- Twilio REST API (sending, reading messages & contacts)
- Ncurses Library for displaying information for user interaction
- Vim Text Editor for creating and editing the program.

### Inspiration
- We wanted to be able to send SMS text messages from the command line, using a VoIP backed solution.

### How we built it
- We used critical thinking and problem solving skills. We used python as the language and Twilio as the backend API. Vim was the text editor used.

### Challenges we ran into
- We had a bug of duplicating messages in the conversation window. It was fixed after talking with a mentor. We also ran into some layout issues, that were fixed after looking at our working examples.

### Accomplishments that we're proud of
- We created a working application. We can now send and receive SMS text messages from the terminal. Creating a viable ncurses interface.

### What we learned
- How to create ncurses environments for terminal applications.

### What's next for TermText
- We want to add the functionality to add number to the "phone book".
