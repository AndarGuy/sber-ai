import serial
import time

check = serial.Serial('COM3')

check.write(b"F9")
time.sleep(5)
check.write(b'R5')
time.sleep(5)
check.write(b'L5')
