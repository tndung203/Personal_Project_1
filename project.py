import RPi.GPIO as GPIO
import time
from picamera import PiCamera
import os
import yagmail

DATA_IN = 17
GPIO.setmode(GPIO.BCM)	# set pin use BCM numbering

GPIO.setup(DATA_IN, GPIO.IN)	#config pin 17 as an input to receive data

camera = PiCamera()	#initial class in picamera library
camera.resolution = (1280,720)	#The image resolution configuration is 1280 wide and 720 high
camera.rotation = 180	#Set the rotation
print("Initializing camera ....")
time.sleep(2)	#wait initialize camera
print("Successfully!")

time_curr = time.time()	#set a time current
last_time_photo_taken = 0	#set a time when capture image
file_log = "./photo_logs.txt"	#file store path of image when capture
path=""	#path to create image
username = "tndung922@gmail.com"	#user name to set SMTP
password = "itpogwplxttgouud"	#password to set SMTP
print("Initializing SMTP ....")
yag = yagmail.SMTP(username, password)	#initialize SMTP
print("Successfully!!!")

#check if file exists then remove file
if os.path.exists(file_log):
    os.remove(file_log)

#function to capture image
def take_photo(time_curr):
    global path
    path="/home/raspberrypi/Pictures/img_" + str(time_curr) + ".jpg"
    camera.capture(path)
    print("Done")

#function to log path to file
def log_path():
    with open(file_log, "a") as file:
        file.write(path)
        print("Write log file successfully")

#function to send photo via email
def send_mail_with_photo():
    yag.send("ntdung210903@gmail.com", 'New image', path)
    print("Send mail successfully")
    
while True:
    if time.time() - time_curr >= 3:
        if time.time() - last_time_photo_taken >= 20:
            if GPIO.input(17):
                take_photo(time_curr)
                log_path()
                send_mail_with_photo()
                last_time_photo_taken =  time.time()
        time_curr = time.time()
                
         

