import json

class PropertiesReader:

    dict_prop = {}

    def __init__(self, filename):
        try:
            file = open(filename, "r")
            self.dict_prop = json.loads(file.read())
            file.close()
        except IOError:
            print("[ERR] Cannot found file {}".format(filename))
    
    def props(self):
        return self.dict_prop
    