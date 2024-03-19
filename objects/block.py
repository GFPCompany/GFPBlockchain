import pymysql

from db.db_lib import db_insert
from libs.beauti_cli import *

class Block:
    def __init__(self):
        self.height = None
        self.nonce = None
        self.timestamp = None
        self.previous_hash = None
        self.hash = None
    def from_json(self,data):
        required_keys = ["hash","previous_hash","timestamp","nonce","height"]

        for key in required_keys:
            if key not in data:
                raise Exception(f"Missing key {key} in block")

        self.hash = data["hash"]
        self.previous_hash = data["previous_hash"]
        self.timestamp = data["timestamp"]
        self.nonce = data["nonce"]
        self.height = data["height"]

    def to_json(self):
        return {
            "hash":self.hash,
            "previous_hash":self.previous_hash,
            "timestamp":self.timestamp,
            "nonce":self.nonce,
            "height":self.height
    }
    def write_to_db(self):
        try:
            db_insert(
                f"INSERT INTO blocks(id,hash,previous_hash,timestamp,nonce) VALUES ({self.height},'{self.hash}','{self.previous_hash}',{self.timestamp},{self.nonce})")
        except pymysql.err.IntegrityError as e:
            printError("MYSQL ERROR: " + str(e))
