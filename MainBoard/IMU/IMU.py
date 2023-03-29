import serial

# ser = serial.Serial('COM4', 9600)


# message = ser.readline()
# message = message.decode().strip()
# header, parsed_data = process_message(message)
# print(header, parsed_data)


class IMU:
    def __init__(self, ser : serial.Serial) -> None:
        '''
        Initializes the IMU class.
        args:
        - ser: An initalized serial object which can communicate with the IMU
        '''
        self.serial = ser
        self.time = [0, 0, 0]
        self.acc = [0, 0, 0]
        self.gyro = [0, 0, 0]
        self.angle = [0, 0, 0]
        self.mag = [0, 0, 0]
        self.pressure = [0, 0, 0]
        return
    

    def process_message(self, message : str):
        '''
        Sorts and parses data.
        args:
        - message: A string that stores header and parsed data.
        '''
        if(message[0] != '!'):
            return "", []
        if(message[len(message)-1] != ';'):
            return "", []
        parsed_data = []
        token = ""
        for letter in message[1:]:
            if letter == ';':
                parsed_data.append(token)
                break
            if letter == ',':
                parsed_data.append(token)
                token = ""
                continue
            token = token+letter
        header = parsed_data[0]
        parsed_data = parsed_data[1:]
        for i,num in enumerate(parsed_data):
            try:
                parsed_data[i] = float(num)
            except:
                pass
        
        return header, parsed_data

    def update(self):
        '''
        Parses serial into a header and list, then parsed_data is stored to the serial list.
        Meant to be called continuously
        '''
        # get a line of serial
        try:
            message = self.serial.readline().decode('UTF-8').strip()
        except UnicodeDecodeError:
            print("Bad shit happened")
            return
        # parse the serial into a header and list
        header, parsed_data = self.process_message(message)
        # use the header to figure out which internal list to store the serial list in
        if header == "TIME":
            self.time = parsed_data
        elif header == "ACC":
            self.acc = parsed_data
        elif header == "GYRO":
            self.gyro = parsed_data
        elif header == "ANGLE":
            self.angle = parsed_data
        elif header == "MAG":
            self.mag = parsed_data
        elif header == "PRESSURE":
            self.pressure = parsed_data
        return
