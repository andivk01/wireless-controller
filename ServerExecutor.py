import pyxinput
from PropertiesReader import PropertiesReader
from threading import Thread
import json

class ServerExecutor(Thread):

    def __init__(self, socket, id_controller):
        self.socket = socket
        self.id_controller = id_controller
        self.events_code = PropertiesReader.props("prop.json")
    def __str__(self):
        return self.socket.getsockname()

    def run(self):
        virtualController = pyxinput.vController() # initialize virtual controller
        dataJson = True
        while(dataJson):
            dataJson = self.socket.recv(200)
            self.socket.send("1".encode())
            data = json.loads(dataJson)
            decoded_code = self.events_code[data["event_code"]]
            virtualController.set_value(decoded_code, data["event_state"])
            
            print("[{}]Ping pacchetto precedente: {}".format(self.id_controller, data["previous_ping"]))
        else:
            raise RuntimeError("Connessione col raspy interrotta.")