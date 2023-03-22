import serial

def process_message(message):
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

ser = serial.Serial('COM4', 9600)

while True:
    message = ser.readline()
    message = message.decode().strip()
    header, parsed_data = process_message(message)
    print(header, parsed_data)





