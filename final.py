import SimpleMFRC522
import RPi.GPIO as GPIO
import time, datetime
import telegram
from picamera import PiCamera
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#For setting up Pi camera
camera = PiCamera()

def cap():
    camera.rotation = 180
    camera.resolution = (2592, 1944)
    camera.framerate = 15
    sleep(1)
    camera.capture('/home/pi/Desktop/image.jpg')

#For setting up motor
coil_A_1_pin = 27 # pink
coil_A_2_pin = 22 # orange
coil_B_1_pin = 5 # blue
coil_B_2_pin = 6 # yellow

# adjust if different
StepCount = 8
Seq = range(0, StepCount)
Seq[0] = [1,0,0,0]
Seq[1] = [1,1,0,0]
Seq[2] = [0,1,0,0]
Seq[3] = [0,1,1,0]
Seq[4] = [0,0,1,0]
Seq[5] = [0,0,1,1]
Seq[6] = [0,0,0,1]
Seq[7] = [1,0,0,1]

#GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

#GPIO.output(enable_pin, 1)
def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_B_2_pin, w4)

def forward(delay, steps):
    for i in range(steps):
        for j in range(StepCount):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)

def backwards(delay, steps):
    for i in range(steps):
        for j in reversed(range(StepCount)):
            setStep(Seq[j][0], Seq[j][1], Seq[j][2], Seq[j][3])
            time.sleep(delay)

#Setting up RFID functions
reader=SimpleMFRC522.SimpleMFRC522()

GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.OUT)

def rfid():

    id,text=reader.read()
    chat_id=669801266
    now= datetime.datetime.now()
    bot = telegram.Bot(token='Your telegram token here') #Enter your token here.
    print (bot.getMe())

    if id==626081541925:
        print "Card is Valid"
        print "Welcome"
        print(text)
        print 'Authentication Successfull'

        bot.sendMessage (chat_id=chat_id, text= "Some activity detected")

        if __name__ == '__main__':
            delay = 3
            while True:
                steps = 128
                forward(int(delay) / 1000.0, int(steps))
                steps = 128
                backwards(int(delay) / 1000.0, int(steps))
                break

        time.sleep(2.5)
        bot.sendPhoto (chat_id=chat_id, photo=open('/home/pi/Desktop/image.jpg'))

    elif id!=626081541925:
        print "Card is invalid"
        GPIO.output(17, True)
        time.sleep(0.5)
        GPIO.output(17, False)
        print(text)
        print 'Intruder!!!!!'
        bot.sendMessage (chat_id=chat_id, text= "Intruder at the door!!! \nInvalid card entry")
        time.sleep(2.5)
        bot.sendPhoto (chat_id=chat_id, photo=open('/home/pi/Desktop/image.jpg'))

current_state=0

try:
    while True:
        time.sleep(0.1)
        current_state = GPIO.input(4)

        if current_state == 1:
            print "Motion Detected"
            cap()
            rfid()
            time.sleep(5)
        else:
            print "No motion"

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
