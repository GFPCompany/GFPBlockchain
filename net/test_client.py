import json
import os
import socket
import time

import base58

from libs.gfp_library_0 import *
from libs.beauti_cli import *

CONFIG = {
    "software_version": "0.0.2",
    "token":base58.b58encode(sha256("TEST CLIENT")).decode('utf-8'),
    "minimal_version": "0.0.1"
}
def translate_version(version):
    return int("".join([str(int(i)) for i in version.split(".")]))

class Client:
    def __init__(self):
        self.ip = None
        self.port = None
    def connect(self, address,timeout=2):
        self.ip = address.split(":")[0]
        self.port = int(address.split(":")[1])
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.settimeout(timeout)
            self.socket.connect((address.split(":")[0], int(address.split(":")[1])))
            printOk("CONNECTED TO NODE '" + self.ip + ":" + str(self.port) + "'",light=True)
            return True
        except:
            printError("CANT CONNECT TO NODE '" + self.ip + ":" + str(self.port) + "' REASON -> TIMED OUT")
            exit(10)


    def send_data(self, data):
        try:
            self.socket.send(json.dumps(data).encode('utf-8'))
        except:
            printError("CANT SEND DATA TO NODE '" + self.ip + ":" + str(self.port) + "' REASON -> TIMED OUT")
            exit(10)

    def recv_data(self,timeout=2):
        self.socket.settimeout(timeout)
        data = self.socket.recv(1024)
        return json.loads(data.decode('utf-8'))

    def ping(self,timeout=2):
        if timeout!=2:
            printBasic("TRYING TO PING NODE '" + self.ip + ":" + str(self.port) + "' WITH TIMEOUT `" + str(timeout) + "` SEC",light=True)
        else:
            printBasic("TRYING TO PING NODE '" + self.ip + ":" + str(self.port)+"' WITH DEFAULT TIMEOUT '2' SEC",light=True)
        st = time.time()
        data = {
            "command": "ping"
        }
        self.send_data(data)
        if self.recv_data(timeout)["command"] == "pong":
            printBasic("PONG RECEIVED, NODE '" + self.ip + ":" + str(self.port) + "' ANSWERED IN " + str(round((time.time() - st)*1000,3)) + " MS",light=True)
            return True
        else:
            return False

    def inv(self, blocks):
        data = {
            "command": "inv",
            "data": {
                "objects_type": "block",
                "objects": [i["hash"] for i in blocks]
            }
        }
        self.send_data(data)
        data = self.recv_data()
        if data["command"]=="get_data":
            data = {
                "command": "block",
                "data": {
                    "objects_type": "block",
                    "objects": [i for i in blocks]
                }
            }
            self.send_data(data)
            return True
        else:
            return False
    def version(self):
        printBasic("SENDING VERSION REQUEST TO NODE '" + self.ip + ":" + str(self.port) + "'",light=True)
        data = {
            "command": "version",
            "data": {
                "ip": self.socket.getpeername()[0],
                "port": self.socket.getpeername()[1],
                "version": CONFIG["software_version"],
                "height": 0,
                "token": CONFIG["token"]
            }
        }
        self.send_data(data)
        data = self.recv_data()

        if data["command"] == "error":
            printWarning("VERSION OF THIS NODE IS TOO OLD, NODE '" + self.ip + ":" + str(self.port) + "' ANSWERED -> " + data["message"],light=True)
            return False

        if data["command"] == "verack":
            printOk("'verack' PACKET RECEIVED FROM NODE '" + self.ip + ":" + str(self.port) + "'",light=True)
        data = self.recv_data()

        if data["command"] == "version":
            text = "VERSION PACKET RECEIVED FROM NODE '" + self.ip + ":" + str(self.port) + "'\n"
            text += "NODE INFO:\n"
            text += "\tIP: " + data["data"]["ip"] + "\n"
            text += "\tPORT: " + str(data["data"]["port"]) + "\n"
            text += "\tVERSION: " + data["data"]["version"] + "\n"
            text += "\tHEIGHT: " + str(data["data"]["height"]) + "\n"
            text += "\tTOKEN: " + data["data"]["token"] + "\n"
            printBasic(text,light=True)
            NODE_VERSION = translate_version(data["data"]["version"])
            if NODE_VERSION < translate_version(CONFIG["minimal_version"]):
                printWarning("PEER '"+self.ip+":"+str(self.port)+"' NODE VERSION TOO OLD")
                data = {
                    "command": "error",
                    "message": "node version too old"
                }
                self.send_data(data)
                return False
            else:
                data = {
                    "command":"verack"
                }
                self.send_data(data)
                printBasic("SENT 'verack' PACKET TO NODE '" + self.ip + ":" + str(self.port) + "'",light=True)
                print("wait for 'verack' packet from peer")
                printOk("NODE '" + self.ip + ":" + str(self.port) + "' ACCEPTED 'verack' PACKET",light=True)
                printOk("END OF 'version' SESSION WITH NODE '" + self.ip + ":" + str(self.port) + "'",light=True)
                return True
        else:
            return False
    def tx(self,txs):
        printBasic("SENDING 'TX' PACKET TO NODE '" + self.ip + ":" + str(self.port) + "'",light=True)
        data = {
            "command": "tx",
            "data": txs
        }
        self.send_data(data)
        printOk("END OF 'tx' SESSION WITH NODE '" + self.ip + ":" + str(self.port) + "'",light=True)
a = Client()
a.connect("127.0.0.1:5000")

txs = [
    {
        "txid": "0000000000000000000000000000000000000000000000000000000000000000",
        "inputs": [
            {
                "txid": "0000000000000000000000000000000000000000000000000000000000000000",
                "vout": 0
            }
        ],
        "outputs": [
            {
                "address": "0000000000000000000000000000000000000000000000000000000000000000",
                "value": 0
            }
        ],
        "timestamp": 0
    }
]

a.tx(txs)