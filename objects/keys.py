import base58
import ecdsa
from libs.beauti_cli import *
from libs.gfp_library_0 import *

CONFIG = {
    "PRIVATE_KEY_PREFIX" : "1567", # hex
    "PRIVATE_KEY_CHECKSUM_LENGTH" : 4,  # in bytes
    "PRIVATE_KEY_CHECKSUM_ALGO" : "md5"
}

ERRORS = {
    0x10 : "Private key not generated",
    0x11 : "Private key checksum algo not supported",
    0x12 : "Raw private key not valid",
    0x13 : "Private key prefix not valid",
    0x14 : "Private key checksum not valid",


    0xf0 : "Public key not generated",
    0xf1 : "Public key checksum algo not supported",
    0xf2 : "Raw public key not valid",
    0xf3 : "Public key prefix not valid",
    0xf4 : "Public key checksum not valid",
}

class GFP_PrivateKey:

    def __init__(self):
        self.key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.FLAG_GENERATED = False

    def generate(self):
        self.key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.FLAG_GENERATED = True
        return 1
    def to_raw(self):
        if self.FLAG_GENERATED == False:
            err_code = 0x10
            printError(f"{str(hex(err_code))}:"+ERRORS[err_code])
            exit(1)
        return self.key.to_string()
    def to_GFP(self):
        prefix = bytes.fromhex(CONFIG["PRIVATE_KEY_PREFIX"])
        key = self.to_raw()

        if CONFIG["PRIVATE_KEY_CHECKSUM_ALGO"] == "md5":
            checksum = md5(key)[:CONFIG["PRIVATE_KEY_CHECKSUM_LENGTH"]*2]
        elif CONFIG["PRIVATE_KEY_CHECKSUM_ALGO"] == "sha256":
            checksum = sha256(key)[:CONFIG["PRIVATE_KEY_CHECKSUM_LENGTH"]*2]
        else:
            err_code = 0x11
            printError(f"{str(hex(err_code))}:"+ERRORS[err_code])
            exit(1)
        checksum = bytes.fromhex(checksum)

        total = prefix + key + checksum
        total = base58.b58encode(total)

        return total
    def from_raw(self,raw):
        try:
            self.key = ecdsa.SigningKey.from_string(raw, curve=ecdsa.SECP256k1)
            self.FLAG_GENERATED = True
            return 1
        except:
            err_code = 0x12
            printError(f"{str(hex(err_code))}:"+ERRORS[err_code])
            exit(1)
    def from_GFP(self,key):
        key = base58.b58decode(key).hex()
        prefix = key[:len(CONFIG["PRIVATE_KEY_PREFIX"])]
        if prefix != CONFIG["PRIVATE_KEY_PREFIX"]:
            err_code = 0x13
            printError(f"{str(hex(err_code))}:"+ERRORS[err_code])
            exit(1)
        raw_key = key[len(CONFIG["PRIVATE_KEY_PREFIX"]):-CONFIG["PRIVATE_KEY_CHECKSUM_LENGTH"]*2]

        checksum = key[-CONFIG["PRIVATE_KEY_CHECKSUM_LENGTH"]*2:]

        if CONFIG["PRIVATE_KEY_CHECKSUM_ALGO"] == "md5":
            if checksum != md5(bytes.fromhex(raw_key))[:CONFIG["PRIVATE_KEY_CHECKSUM_LENGTH"]*2]:
                err_code = 0x14
                printError(f"{str(hex(err_code))}:"+ERRORS[err_code])
                exit(1)
        elif CONFIG["PRIVATE_KEY_CHECKSUM_ALGO"] == "sha256":
            if checksum != sha256(bytes.fromhex(raw_key))[:CONFIG["PRIVATE_KEY_CHECKSUM_LENGTH"]*2]:
                err_code = 0x14
                printError(f"{str(hex(err_code))}:"+ERRORS[err_code])
                exit(1)
        else:
            err_code = 0x11
            printError(f"{str(hex(err_code))}:"+ERRORS[err_code])
            exit(1)
        self.from_raw(bytes.fromhex(raw_key))
        return 1
    def sign(self,data:bytes):
        if self.FLAG_GENERATED == False:
            err_code = 0x10
            printError(f"{str(hex(err_code))}:"+ERRORS[err_code])
            exit(1)
        return self.key.sign(data,hashfunc=hashlib.sha256)

class GFP_PublicKey:
    def __init__(self):
        self.key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1).get_verifying_key()
        self.FLAG_GENERATED = False
    def generate(self,private_key):
        if type(private_key) == str:
            private_key = bytes.fromhex(private_key)
            self.key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1).get_verifying_key()
        elif type(private_key) == bytes:
            self.key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1).get_verifying_key()
        elif type(private_key) == GFP_PrivateKey:
            self.generate(private_key.to_raw())
    def to_GFP(self):
        if self.FLAG_GENERATED == False:
            err_code = 0xf0
            printError(f"{str(hex(err_code))}:"+ERRORS[err_code])
            exit(1)
        return self.key.to_string().hex()
    def from_raw(self,raw):
        try:
            self.key = ecdsa.VerifyingKey.from_string(raw, curve=ecdsa.SECP256k1)
            self.FLAG_GENERATED = True
            return 1
        except:
            err_code = 0xf2
            printError(f"{str(hex(err_code))}:"+ERRORS[err_code])
            exit(1)
    def from_GFP(self,key):
        try:
            self.key = ecdsa.VerifyingKey.from_string(bytes.fromhex(key), curve=ecdsa.SECP256k1)
            self.FLAG_GENERATED = True
            return 1
        except:
            err_code = 0x12
            printError(f"{str(hex(err_code))}:"+ERRORS[err_code])
            exit(1)
a = GFP_PrivateKey()
a.generate()
print(a.from_GFP(a.to_GFP()))
print(a.sign(b"hello world"))