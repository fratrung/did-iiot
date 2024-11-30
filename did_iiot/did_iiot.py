import hashlib
import uuid
from typing import List
from abc import ABC, abstractmethod

class DIDIndustrialIoT:

    @staticmethod         
    def generate_did_uri(enviroment=None):
        uuid_v4 = uuid.uuid4()
        did = f"did:iiot:{uuid_v4}"
        if enviroment:
            did = f"did:net:{enviroment}:{uuid_v4}" 
        return did
    
    @staticmethod    
    def generate_did_uri_hashed():
        did_uri = DIDIndustrialIoT.generate_did_uri().split(":")
        did_uri[2] = hashlib.sha256(did_uri[-1].encode('utf-8')).hexdigest()
        return ":".join(did_uri)
    
    
 