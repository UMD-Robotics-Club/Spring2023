import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

# continually read 100 bytes from the serial port
while True:
    data = ser.read_until(b'\n') # read until the byte \x
    data = data.hex() # convert the data to hex
    print(data)