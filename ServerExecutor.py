import pyxinput
from PropertiesReader import PropertiesReader
from threading import Thread
import json

class ServerExecutor(Thread):

    prop_reader = PropertiesReader("prop.json")
    PACKET_LENGTH = 170 # in bytes

    def __init__(self, socket, id_controller):
        super().__init__()
        self.socket = socket
        self.id_controller = id_controller
        self.events_code = ServerExecutor.prop_reader.props()
    def __str__(self):
        return self.socket.getsockname()

    def run(self):
        virtualController = pyxinput.vController() # initialize virtual controller

        dataJson = self.socket.recv(ServerExecutor.PACKET_LENGTH)
        self.socket.send("1".encode())
        while(dataJson):
            data = json.loads(dataJson)
            decoded_code = self.events_code[data["event_code"]]
            virtualController.set_value(decoded_code, data["event_state"])
            
            print("[Controller-ID #{}] Ping precedent packet: {} milliseconds".format(self.id_controller, data["previous_ping"]))
            dataJson = self.socket.recv(ServerExecutor.PACKET_LENGTH)
            self.socket.send("1".encode())
        else:
            print("[INFO] Connection with {} interrupted.".format(self.id_controller))