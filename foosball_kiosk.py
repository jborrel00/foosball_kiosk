"""foosball_game.py 
this program will be run on the raspberry pi while the foosball game is going on. it will read the two card IDs of the players
as well as the sides the players are playing on. this program is designed to work with a modified version of the arduino 
program NFC-Card-Trigger.ino, justhex, which will only write 1 card's ID to the serial.

additionally, this program will, once the player and side information has been input, keep track of goals and, at the
game's conclusion, update the necessary mysql tables."""

import RPi.GPIO as GPIO
import serial
import MySQLdb as mdb
from time import sleep
import glob

GPIO.setwarnings = False
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5,GPIO.OUT)

GPIO.output(5,0)
sleep(.1)
GPIO.output(5,1)

if '/dev/ttyACM1' in glob.glob('/dev/tty*'):
  ser = serial.Serial('/dev/ttyACM1',115200)
else:
	ser = serial.Serial('/dev/ttyACM0',115200)

r = ser.readline()
r = r.rstrip().rstrip('.').replace(" ","")
int(r,16)
print r #debugging

con = mdb.connect('localhost','root','foosball','foosball')
with con:
	cur = con.cursor()
	cur.execute("update current_card set current_ID = "+r)
