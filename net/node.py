import json
import socket
import sqlite3
from threading import *
from queue import Queue

import base58

from db.db_lib import *
from libs.beauti_cli import *
from libs.gfp_library_0 import sha256
from objects.block import Block

CONFIG = {
    "software_version": "0.0.1",
    "token": base58.b58encode(sha256("TEST NODE")).decode('utf-8'),
    "minimal_version": "0.0.1"
}
def translate_version(version):
    return int("".join([str(int(i)) for i in version.split(".")]))
def check_message_keys(data,keys):
    for key in keys:
        if key not in data:
            return False
    return True

mempool = Queue()
def read_mempool():
    out = []
    for i in range(mempool.qsize()):
        d = mempool.get()
        out.append(d)
        mempool.put(d)
    return out
class Node:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))

    def run(self):
        self.socket.listen(5)
        while True:
            client_socket, address = self.socket.accept()
            printInfo("PEER CONNECTED: " + address[0] + ":" + str(address[1]),light=True)
            t = Thread(target=self.handle, args=(client_socket, address),daemon=True)
            t.start()
    def handle(self,connection,address):
        while True:
            data = connection.recv(1024)
            if data==b"":
                continue
            data = json.loads(data.decode('utf-8'))

            if "command" not in data:
                connection.send(json.dumps({"command": "error no command specified"}).encode('utf-8'))

            if data["command"] == "ping":
                printBasic("RECEIVED PING PACKET FROM PEER '"+str(address[0])+":"+str(address[1])+"'",light=True)
                connection.send(json.dumps({"command": "pong"}).encode('utf-8'))
            if data["command"] == "version":
                if not check_message_keys(data,["data","command"]):
                    connection.send(json.dumps({"command": "error","message":"no data specified"}).encode('utf-8'))
                    printWarning("RECEIVED INVALID 'version' PACKET FROM PEER '"+str(address[0])+":"+str(address[1])+"'")
                    break
                if not check_message_keys(data["data"],["ip","port","version","height","token"]):
                    connection.send(json.dumps({"command": "error","message":"no data specified"}).encode('utf-8'))
                    printWarning("RECEIVED INVALID 'version' PACKET FROM PEER '"+str(address[0])+":"+str(address[1])+"'")
                    break
                printOk("RECEIVED VERSION PACKET FROM PEER '"+str(address[0])+":"+str(address[1])+"'",light=True)

                if translate_version(data["data"]["version"]) <= translate_version(CONFIG["minimal_version"]):
                    connection.send(json.dumps({"command": "error","message":"node version too old"}).encode('utf-8'))
                    printWarning("NODE '"+str(address[0])+":"+str(address[1])+"' VERSION TOO OLD")
                    break
                NODE_DATA = data
                data = {
                    "command": "verack"
                }
                connection.send(json.dumps(data).encode('utf-8'))

                data = {
                    "command": "version",
                    "data": {
                        "ip": address[0],
                        "port": address[1],
                        "version": CONFIG["software_version"],
                        "height": 0,
                        "token": CONFIG["token"]
                    }
                }
                connection.send(json.dumps(data).encode('utf-8'))
                data = json.loads(connection.recv(1024).decode('utf-8'))
                if data["command"] == "verack":
                    printOk("RECEIVED VERACK PACKET FROM PEER '"+str(address[0])+":"+str(address[1])+"'",light=True)
                    is_exists = db_select("SELECT `id` FROM peers WHERE `token` = '" + NODE_DATA['data']['token'] + "'")
                    print(is_exists)
                    if is_exists == ():
                        db_insert(f"INSERT INTO peers(address,port,version,height,token) VALUES ('{NODE_DATA['data']['ip']}',{NODE_DATA['data']['port']},'{NODE_DATA['data']['version']}',{NODE_DATA['data']['height']},'{NODE_DATA['data']['token']}')")
                        printInfo("|DB|: PEER ADDED TO DATABASE: " + address[0] + ":" + str(address[1]),light=True)
                    else:
                        printWarning("|DB|: PEER ALREADY EXISTS IN DATABASE: " + address[0] + ":" + str(address[1]),light=True)
                else:
                    printWarning("VERSION OF THIS PEER IS TOO OLD")
                printOk("END OF 'version' SESSION WITH PEER '"+str(address[0])+":"+str(address[1])+"'",light=True)
            if data["command"] == "inv":
                if "data" not in data:
                    connection.send(json.dumps({"command": "error","message":"no data specified"}).encode('utf-8'))
                    printWarning("RECEIVED INVALID 'version' PACKET FROM PEER '"+str(address[0])+":"+str(address[1])+"'")
                else:
                    required_keys = ["objects_type","objects"]

                    for key in required_keys:
                        if key not in data["data"]:
                            connection.send(json.dumps({"command": "error","message":"missing key"}).encode('utf-8'))
                            printWarning("RECEIVED INVALID 'inv' PACKET FROM PEER '"+str(address[0])+":"+str(address[1])+"'")
                            break

                    printOk("RECEIVED INV, TYPE '"+data["data"]["objects_type"]+ "' FROM PEER '"+str(address[0])+":"+str(address[1])+"'")
                    if data["data"]["objects_type"] == "block":
                        self_blocks = db_select("SELECT hash FROM blocks")
                        self_blocks = [i["hash"] for i in self_blocks]
                        required_blocks_hashes = []
                        for block in data["data"]["objects"]:
                            if block not in self_blocks:
                                required_blocks_hashes.append(block)
                        printOk("MISSING BLOCKS IN LOCAL COPY: `"+json.dumps(required_blocks_hashes)+"` ASKING 'get_data' FROM PEER `"+str(address[0])+":"+str(address[1])+"`")
                        packet = {
                            "command":"get_data",
                            "data":{
                                "objects_type":"block",
                                "objects":required_blocks_hashes
                            }
                        }
                        connection.send(json.dumps(packet).encode('utf-8'))
                        data = connection.recv(1024)
                        printOk("BLOCKS RECEIVED FROM PEER "+str(address[0])+":"+str(address[1]))
                        data = json.loads(data.decode('utf-8'))
                        for i in data["data"]:
                            b = Block()
                            b.from_json(i)
                            b.write_to_db()
                    elif data["data"]["objects_type"] == "tx":
                        q_data = []
                        for i in range(mempool.qsize()):
                            q_data.append(mempool.get())

                        for i in q_data:
                            mempool.put(i)
                            print(i)
                        print("Q_DATA_0:",q_data)
                        self_txs_txids = [i["txid"] for i in q_data]
                        required_txs_txids = []
                        for tx in data["data"]["objects"]:
                            if tx not in self_txs_txids:
                                required_txs_txids.append(tx)
                        print(required_txs_txids)
                        packet = {
                            "command":"get_data",
                            "data":{
                                "objects_type":"tx",
                                "objects":required_txs_txids
                            }
                        }
                        print("waiting for txs")
                        connection.send(json.dumps(packet).encode('utf-8'))
                        data = connection.recv(1024)
                        print("txs received")
                        data = json.loads(data.decode('utf-8'))
                        for i in data["data"]["objects"]:
                            if i["txid"] not in self_txs_txids:
                                mempool.put(i)
                        q_data = []
                        for i in range(mempool.qsize()):
                            q_data.append(mempool.get())
                        for i in q_data:
                            mempool.put(i)
                            print(i)

            if data["command"] == "tx":
                if not check_message_keys(data,["data"]):
                    connection.send(json.dumps({"command": "error","message":"no data specified"}).encode('utf-8'))
                    printWarning("RECEIVED INVALID 'tx' PACKET FROM PEER '"+str(address[0])+":"+str(address[1])+"'")
                printInfo("RECEIVED 'tx' PACKET FROM PEER '"+str(address[0])+":"+str(address[1])+"' WITH '"+str(len(data["data"]))+"' TRANSACTIONS",light=True)
                txs_to_mempool = []
                mempool_txids = [i["txid"] for i in read_mempool()]
                c=0
                for i in data["data"]:
                    if not check_message_keys(i,["txid","timestamp","inputs","outputs"]):
                        connection.send(json.dumps({"command": "error","message":"no txid or tx specified"}).encode('utf-8'))
                        printWarning("RECEIVED INVALID 'tx' PACKET FROM PEER '"+str(address[0])+":"+str(address[1])+"'")
                        break

                    if i["txid"] not in mempool_txids:
                        mempool.put(i)
                        c+=1
                printOk("'"+str(c)+"' TRANSACTIONS ADDED TO MEMPOOL")

a = Node("127.0.0.1", 5000)
a.run()


















































