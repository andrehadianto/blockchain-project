import hashlib
import random
import time
import math
import json
import cbor
import base64
from ecdsa import SigningKey, VerifyingKey , NIST384p

class Transaction(object):
    
    def __init__(self,sender,receiver,amount,comment):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.comment = comment
        self.signature = None
        
    def __eq__(self,transaction):
        if self.sender == transaction.sender and self.receiver==transaction.receiver and self.amount==transaction.amount:
            return True
        return False
        
    @classmethod
    def new(self,sender,receiver,amount,comment):
        t1 = Transaction(sender,receiver,amount,comment)
        return t1
        
    
    def serialize(self):
        props = {}
        props["receiver"] = self.receiver
        props["sender"] =  self.sender
        props["amount"] = self.amount
        props["comment"] = self.comment
        return cbor.dumps(props)
    
    @classmethod
    def deserialize(self,js_string):
        obj = json.loads(js_string)
        obj['sender'] = obj['sender'].encode('ascii')
        obj['receiver'] = obj['receiver'].encode('ascii')
        result = Transaction(VerifyingKey.from_string(base64.decodebytes(obj['sender']),curve=NIST384p),VerifyingKey.from_string(base64.decodebytes(obj['receiver']),curve=NIST384p),obj['amount'],obj['comment'])
        return result 
        
    def sign(self,priv_key):
        s = self.serialize().encode()
        print(s)
        sig = priv_key.sign(s)
        print('finished signing')
        self.signature = sig
        return sig
    
    def validate(self):
        assert self.sender.verify(self.signature, self.serialize().encode()),"validation failed" ## self.serialize.encode is the transaction
        print('finished validating')
        return