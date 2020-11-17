import socket
import json
import time
import pyxinput

try:
    servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servSocket.bind((socket.gethostname(), 6088))
    servSocket.listen(1) # max 1 client
except socket.error as message:
    print("[ERROR] {}\n".format(message))


events_code = {
    "BTN_SOUTH": "BtnA",
    "BTN_EAST": "BtnB",
    "BTN_NORTH": "BtnX",
    "BTN_WEST": "BtnY",

    "ABS_X": "AxisLx", 
    "ABS_Y": "AxisLy",
    
    "ABS_RX": "AxisRx",
    "ABS_RY": "AxisRy",

    "ABS_HAT0X": "PAD",
    "ABS_HAT0Y": "PAD",
    
    "ABS_Z": "TriggerL",
    "ABS_RZ": "TriggerR",
    "BTN_TL": "BtnShoulderL",
    "BTN_TR": "BtnShoulderR",

    "BTN_SELECT": "BtnBack",
    "BTN_START": "BtnStart",
        
    "BTN_THUMBL": "BtnThumbL",
    "BTN_THUMBR": "BtnThumbR",

}

(socket, addr) = servSocket.accept()
print("Client connesso, {addr}")
virtualController = pyxinput.vController() # initialize virtual controller
dataJson = True
while(dataJson):
    dataJson = socket.recv(200)
    socket.send("1".encode())
    data = json.loads(dataJson)
    decoded_code = events_code[data["event_code"]]
    virtualController.set_value(decoded_code, data["event_state"])

    print("Ping pacchetto precedente: {}".format(data["previous_ping"]))
else:
    raise RuntimeError("Connessione col raspy interrotta.")