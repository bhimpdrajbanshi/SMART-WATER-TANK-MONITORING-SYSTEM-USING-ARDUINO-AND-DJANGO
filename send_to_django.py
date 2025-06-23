import serial
import requests
import time

SERIAL_PORT = 'COM3'  # Change this to your correct COM port
BAUD_RATE = 9600
DJANGO_URL = 'http://127.0.0.1:8000/upload/'

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Give Arduino time to boot

while True:
    try:
        line = ser.readline().decode().strip()
        if line:
            print("Sending:", line)
            requests.post(DJANGO_URL, data={'level_cm': line})
    except Exception as e:
        print("Error:", e)
