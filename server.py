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

while(True):
    (socket, addr) = servSocket.accept()
    print("Nuovo client connesso, {}".format(addr))
    ServerExecutor(socket, range(1, 1000)).start()