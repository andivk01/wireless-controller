import socket
import json
import datetime
from inputs import get_gamepad

def real_status(evt) :
    new_state = evt.state
    if(evt.code.startswith("ABS")):
        new_state = evt.state/32768
        if(evt.code.endswith("Y")):
            new_state *= -1
    return new_state

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket.connect(("192.168.1.6", 6088)) #TODO change ip and except

prev_ping = 0
while 1:
    events = get_gamepad()
    for event in events:
        event_state = real_status(event)
        if event.code.startswith("ABS_HAT"): continue # TODO
        if(event.ev_type != "Sync"):

            try: #controllo se la variabile e' definita
                packet_ping
            except NameError:
                packet_ping = 0

            data = {
                "event_type": event.ev_type,
                "event_code": event.code,
                "event_state": event_state,
                "previous_ping": packet_ping
            }
            dataJson = json.dumps(data)

            if len(dataJson) < 200:
                quantity_of_spaces = 200 - len(dataJson)
                dataJson = dataJson + (" " * quantity_of_spaces)
            dataJson = dataJson.encode()
            sending_time = datetime.datetime.now()
            socket.sendall(dataJson)
            socket.recv(1)
            packet_ping = (datetime.datetime.now() - sending_time).microseconds/1000

