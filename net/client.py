import json
import socket


class Client:
    def __init__(self):
        self.con = None
    def connect(self,address):
        self.con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con.connect((address.split(":")[0], int(address.split(":")[1])))
    def send_data(self,data):
        self.con.send(json.dumps(data).encode('utf-8'))
    def recv_data(self):
        data = self.con.recv(1024)
        return json.loads(data.decode('utf-8'))
    def ping(self):
        data = {
            "command":"ping"
        }
        self.send_data(data)
        if self.recv_data()["command"] == "pong":
            return True
        else:
            return False

    def create_txs(self,txs):
        data = {
            "command":"inv",
            "data":{
                "objects_type":"block",
                "objects":[i["txid"] for i in txs]
            }
        }
        self.send_data(data)
        return self.recv_data()

known_peers = ["127.0.0.1:5000"]

a = Client()
a.connect(known_peers[0])

print(a.ping())
tx = {
    "txid":"0x356b5a1d8d9d4b9e6f7c5f4e3c3b2a1d8d9d4b9e6f7c5f4",
    "inputs":[
        {
            "txid":"0x356b5a1d8d9d4b9e6f7c5f4e3c3b2a1d8d9d4b9e6f7c5f4",
            "vout":0
        }
    ],
    "outputs":[
        {
            "address":"0x356b5a1d8d9d4b9e6f7c5f4e3c3b2a1d8d9d4b9e6f7c5f4",
            "value":0
        }
    ]
}

print(a.create_txs([tx]))