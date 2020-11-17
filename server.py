import socket
import json
import time
import pyxinput
from ServerExecutor import ServerExecutor

try:
    servSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servSocket.bind((socket.gethostname(), 6088))
    servSocket.listen(5)
except socket.error as message:
    print("[ERROR] {}\n".format(message))

id_controller = 0
while(True):
    id_controller += 1
    (socket, addr) = servSocket.accept()
    print("Nuovo client connesso, {}".format(addr))
    ServerExecutor(socket, id_controller).start()