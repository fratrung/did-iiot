'''
Used for easy import 
'''

import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from did_iiot.did_iiot.did_iiot import DIDIndustrialIoT
from did_iiot.did_iiot.did_document import DIDDocument, Service, VerificationMethod
from did_iiot.did_iiot.publicjwk import PublicJwKey, KyberPublicJwkey, DilithiumPublicJwkey, RSAPublicJwkey, Ed25519PubliJwkey