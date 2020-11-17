import sys
import socket
import json
import datetime
from inputs import get_gamepad

PACKET_LENGTH = 170 # in bytes

def real_status(evt) :
    new_state = evt.state
    if(evt.code.startswith("ABS")):
        new_state = evt.state/32768
        if(evt.code.endswith("Y")):
            new_state *= -1
    return new_state

socketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) > 1:
    server_ip = str(sys.argv[1])
else: 
    server_ip = "192.168.1.6"

if len(sys.argv) > 2:
    server_port = int(sys.argv[2])
else: 
    server_port = 6088

server_ip = "192.168.1.6"
server_port = 6088

socketConn.connect((server_ip, server_port))

prev_ping = 0
while 1:
    events = get_gamepad()
    for event in events:
        event_state = real_status(event)
        if event.code.startswith("ABS_HAT"): continue # TODO
        if(event.ev_type != "Sync"):

            try:
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

            if len(dataJson) < PACKET_LENGTH:
                quantity_of_spaces = PACKET_LENGTH - len(dataJson)
                dataJson = dataJson + (" " * quantity_of_spaces)
            dataJson = dataJson.encode()
            sending_time = datetime.datetime.now()
            
            try:
                socketConn.sendall(dataJson)
                socketConn.recv(1)
            except:
                print("[ERR] Error while sending data to server... trying reconnection...")
                socketConn.close()
                socketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socketConn.connect((server_ip, server_port))

            packet_ping = (datetime.datetime.now() - sending_time).microseconds/1000

