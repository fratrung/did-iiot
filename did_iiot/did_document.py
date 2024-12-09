import json
from enum import Enum
from abc import ABC , abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Union

class ServiceType(Enum):
    LinkedDomains = "LinkedDomanis"
    DecentralizedWebNode = "DecentralizedWebNode"
    

class DIDDocumentProperty(ABC):
    @abstractmethod
    def get_dict(self) -> dict:
        """This method should be implemented by subclasses."""
        pass


class PublicJwKey(DIDDocumentProperty):
    def get_public_key(self) -> str:
        """This method should be implemented by subclasses."""
        pass

class VerificationMethod(DIDDocumentProperty):
    
    def __init__(
            self,
            id: str,
            type: str,
            public_jwkey: PublicJwKey,
            controller: Optional[str] = None
            ):
        self.id = id
        self.type = type
        self.controller = controller
        self.public_jwkey = public_jwkey
    
    
    def get_dict(self):
        method = {
            "id": self.id,
            "type": self.type,
            "publicKeyJwk": self.public_jwkey.get_dict(),
        }
        if self.controller:
            method["controller"] = self.controller
        return method



        
class Service(DIDDocumentProperty):
    
    def __init__(self,id: str,type:ServiceType, service_endpoint: str):
            self.id = id
            self.type = type
            self.service_endpoint = service_endpoint
    
    def get_dict(self):
        return {
            "id": self.id,
            "type":self.type.value,
            "serviceEndpoint": self.service_endpoint
        }
    

class DIDDocument():
    
    def __init__(self,
                id: str,
                verification_methods: List[VerificationMethod],
                authentication: Optional[List[Union[str, VerificationMethod]]] = None,
                assertion_method: Optional[List[Union[str, VerificationMethod]]] = None,
                service: Optional[List[Service]] = None,):
        self.id = id
        self.verification_methods = verification_methods
        self.authentication = authentication or [verification_methods[0].id]
        self.assertion_method = assertion_method or [verification_methods[0].id]
        self.service = service or []
        
    
    def add_service(self,service: Service):
        self.service.append(service)
    
    def add_verification_method(self, method: VerificationMethod):
        self.verification_methods.append(method)
    
    
    def get_verification_method(self, id: str) -> Optional[VerificationMethod]:
        """Retrieve a verification method by its id."""
        for vm in self.verification_methods:
            if vm.id == id:
                return vm
        return None  

    def remove_verification_method(self, id: str):
        """Remove a verification method by its id."""
        method_to_remove = self.get_verification_method(id)
        if method_to_remove:
            self.verification_methods.remove(method_to_remove)
            return True
        return False  

    def get_service(self, id: str) -> Optional[dict]:
        """Retrieve a service by its id."""
        for service in self.service:
            if service["id"] == id:
                return service
        return None  

    def remove_service(self, id: str) -> bool:
        """Remove a service by its id."""
        service_to_remove = None
        for service in self.service:
            if service["id"] == id:
                service_to_remove = service
                break
        if service_to_remove:
            self.service.remove(service_to_remove)
            return True
        return False  

    def remove_service(self, id: str):
        self.service = [s for s in self.service if s.id != id]

    def add_authentication(self, method: Union[str, VerificationMethod]):
        """Add an authentication method, which can be either a string or VerificationMethod."""
        if isinstance(method, VerificationMethod):
            self.authentication.append(method)
        elif isinstance(method, str):
            self.authentication.append(method)
        else:
            raise TypeError("Authentication must be either a string or a VerificationMethod object.")

    def remove_authentication(self, id: str) -> bool:
        """Remove an authentication method by its id."""
        for auth_method in self.authentication:
            if isinstance(auth_method, VerificationMethod) and auth_method.id == id:
                self.authentication.remove(auth_method)
                return True
            elif isinstance(auth_method, str) and auth_method == id:
                self.authentication.remove(auth_method)
                return True
        return False  

    def add_assertion_method(self, method: Union[str, VerificationMethod]):
        """Add an assertion method, which can be either a string or VerificationMethod."""
        if isinstance(method, VerificationMethod):
            self.assertion_method.append(method)
        elif isinstance(method, str):
            self.assertion_method.append(method)
        else:
            raise TypeError("Assertion method must be either a string or a VerificationMethod object.")

    def remove_assertion_method(self, id: str) -> bool:
        """Remove an assertion method by its id."""
        for assertion_method in self.assertion_method:
            if isinstance(assertion_method, VerificationMethod) and assertion_method.id == id:
                self.assertion_method.remove(assertion_method)
                return True
            elif isinstance(assertion_method, str) and assertion_method == id:
                self.assertion_method.remove(assertion_method)
                return True
        return False  
    
    def get_dict(self) -> dict:
        return {
            "id": self.id,
            "verificationMethod": [vm.get_dict() for vm in self.verification_methods],
            "service": [s.get_dict() for s in self.service],
            "authentication": self.authentication,
            "assertionMethod": self.assertion_method,
            
        }
        
    def to_json(self) -> str:
        return json.dumps(self.get_dict(), indent=4)