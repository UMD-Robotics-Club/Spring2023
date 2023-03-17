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

print(process_message("!gyro,10,5,18.3;"))
print(process_message("!gyro,10,5,18.3akjsdgh;"))
print(process_message("gyro,10,5,18.3;"))
print(process_message("!gyro,10,5,18.3"))


