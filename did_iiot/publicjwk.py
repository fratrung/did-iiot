from did_iiot.did_document import PublicJwKey


KYBER_LAT = [
    "Kyber-1024",
    "Kyber-768",
    "Kyber-512"
]

DILITHIUM_SECUIRTY_LEVEL = {
    2:"CRYD2",
    3:"CRYD3",
    5:"CRYD5"   
}

class Ed25519PubliJwkey(PublicJwKey):
    def __init__(self,x,kid=None,alg=None,use=None):
        self.x = x
        self.kty = "OKP"
        self.crv = "Ed25519"
        self.kid = kid
        self.alg = alg
        self.use = use
        
    def get_public_key(self) -> str:
        return self.x

    def get_dict(self) -> dict:
        d = {
            "kty": self.kty,
            "crv": self.crv,
            "x": self.x,
        }
        
        if self.alg:
            d["alg"] = self.alg
        if self.use:
            d["use"] = self.use
        if self.kid:
            d["kid"] = self.kid
            
        return d

class RSAPublicJwkey(PublicJwKey):
    def __ini__(self,n,e,kid=None,alg=None,use=None):
        self.n = n
        self.e = e
        self.kid = kid
        self.alg = alg
        self.use = use
        self.kty = "RSA"
        
    def get_public_key(self) -> tuple:
        return (self.n, self.e)
    
    def get_dict(self) -> dict:
        d = {
            "kty": self.kty,
            "n": self.n,
            "e":self.e,
        }
        
        if self.alg:
            d["alg"] = self.alg
        if self.use:
            d["use"] = self.use
        if self.kid:
            d["kid"] = self.kid
            
        return d

class DilithiumPublicJwkey(PublicJwKey):
    
    def __init__(self,key_id,security_level,x):
        alg = self._validate_security_level(security_level)
        if not alg:
            raise ValueError(f"Invalid security level: {security_level}")
        self.alg = alg
        self.key_id = key_id
        self.x = x
        self.kty = "MLWE"
        
    def _validate_security_level(self,security_level):
        if int(security_level) in DILITHIUM_SECUIRTY_LEVEL.keys():
            return DILITHIUM_SECUIRTY_LEVEL[security_level]
        else:
           return None
    
    def get_public_key(self) -> str:
        return self.x
       
    def get_dict(self) -> dict:
        return {
            "kid":self.key_id,
            "alg": self.alg,
            "kty": self.kty,
            "x": self.x
        }
        
class KyberPublicJwkey(PublicJwKey):
    def __init__(self,lat,x):
        is_valid = self._validate_lat(lat)
        if not is_valid:
            raise ValueError(f"Invalid lat: {lat}")
        self.kty = "OKP"
        self.lat = lat
        self.x = x
                    
    def _validate_lat(lat):
        if lat in KYBER_LAT:
            return True
        return False
    
    def get_public_key(self):
        return self.x
    
    def get_dict(self):
        return {
            "kty": self.kty,
            "lat": self.lat,
            "x": self.x
        }