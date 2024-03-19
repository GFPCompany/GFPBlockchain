import hashlib
import json

def TO_HEX(data,length=-1):
    if type(data)==str:
        data = data.encode('utf-8').hex()
        if length!=-1:
            return "00"*(length-int(len(data)//2)) + data
        else:
            return data
    elif type(data)==bytes:
        if length!=-1:
            return "00"*(length-int(len(data)//2)) + data.hex()
        else:
            return data.hex()
    elif type(data)==int:
        data = hex(data)[2:]
        if len(data)%2!=0:
            data = "0"+data
        if length!=-1:
            return "00"*(length-int(len(data)//2)) + data
        else:
            return data

def md5(data):
    if type(data)==str:
        return hashlib.md5(data.encode('utf-8')).hexdigest()
    elif type(data)==bytes:
        return hashlib.md5(data).hexdigest()
    elif type(data)==int:
        return hashlib.md5(bytes.fromhex(TO_HEX(data))).hexdigest()
def sha256(data):
    if type(data)==str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    elif type(data)==bytes:
        return hashlib.sha256(data).hexdigest()
    elif type(data)==int:
        return hashlib.sha256(bytes.fromhex(TO_HEX(data))).hexdigest()
def sha512(data):
    if type(data)==str:
        return hashlib.sha512(data.encode('utf-8')).hexdigest()
    elif type(data)==bytes:
        return hashlib.sha512(data).hexdigest()
    elif type(data)==int:
        return hashlib.sha512(bytes.fromhex(TO_HEX(data))).hexdigest()