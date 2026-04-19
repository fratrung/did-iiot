# Decentralized Identifier Method for Industrial IoT (did:iiot)

A **Decentralized Identifier (DID) method** specifically designed for **Industrial Internet of Things (IIoT)** environments. Tailored for private and internal networks, `did:iiot` is ledger-agnostic and can be deployed over Distributed Hash Tables (DHT), blockchain, web servers, or centralized registries.

> **Note**: This method is under active development. Contributions and feedback are welcome and encouraged.

-----

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [How It Works](#how-it-works)
  - [Create DID](#create-did)
  - [DID Document](#did-document)
  - [DID Resolution](#did-resolution)
  - [Update DID](#update-did)
  - [Key Rotation](#key-rotation)
  - [Revoke DID](#revoke-did)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

-----

## Introduction

`did:iiot` provides a flexible framework for generating and managing Decentralized Identifiers in industrial IoT networks. By leveraging **UUID v4** for unique identifier generation and adhering to the **W3C DID Core specification**, this method delivers secure, scalable, and interoperable identity management for constrained and distributed industrial environments.

-----

## Features

- **Ledger Agnostic** — compatible with DHT, blockchain, web servers, and centralized registries
- **W3C DID Core Compliant** — fully aligned with the W3C specification for broad interoperability
- **Post-Quantum Cryptography** — native support for Dilithium (signatures) and Kyber (key encapsulation)
- **Secure Identity Lifecycle** — supports creation, resolution, update, key rotation, and revocation
- **Industrial Scale** — designed to handle large deployments with many concurrent devices

-----

## How It Works

### Create DID

The `did:iiot` method autonomously generates a DID URI and its corresponding DID Document through the following steps:

1. **UUID v4 Generation** — each DID is derived from a UUID v4 to guarantee global uniqueness
1. **Optional Network Namespace** — a namespace can be specified to categorize the DID within a specific industrial network segment
1. **DID URI Construction** — the resulting URI follows this format:

```
did:iiot:93865a36-e510-4d21-a09a-8575057a883f
```

With an optional network namespace:

```
did:iiot:internal.network:93865a36-e510-4d21-a09a-8575057a883f
```

-----

### DID Document

The DID Document is W3C DID Core compliant and includes:

- **Verification Methods** — public keys for authentication and signature verification
- **Service Endpoints** — for service discovery and device interaction
- **Metadata** — optional fields to extend functionality

-----

### DID Resolution

Resolution retrieves the DID Document from the configured registry (DHT, blockchain, web server, etc.) and returns the associated metadata and service endpoints. The resolution process is registry-dependent and can be adapted to the network’s infrastructure.

-----

### Update DID

Updating a DID Document involves:

1. Replacing the existing document with an updated version
1. Signing the update with the entity’s private key
1. Verifying the signature against the public key (`k0`) stored in the current DID Document

-----

### Key Rotation

Key rotation is handled through the update mechanism:

1. Replace the existing public key (`k0`) with a new one
1. Sign the update using the private key corresponding to the previous public key
1. Protect against replay attacks using version counters, timestamps, nonces, or a hash of the previous state

In immutable registries such as blockchain, the registry’s inherent ordering and immutability properties provide additional protection.

-----

### Revoke DID

Revocation behavior depends on the registry’s capabilities:

- **Permanent Removal** — if the registry supports deletion, the DID Document is removed entirely, rendering the DID inaccessible
- **Deactivation** — if deletion is not supported, the DID Document is replaced with a version explicitly marked as `Deactivated`, preserving its existence while preventing further use

This dual approach ensures revocation is possible in both mutable and immutable registry environments.

-----

## Installation

```bash
git clone https://github.com/fratrung/did-iiot.git
cd did-iiot
pip install -r requirements.txt
```

Requires Python 3.6 or later.

-----

## Usage

### Generate a DID URI

```python
from did_iiot import DIDIndustrialIoT

did = DIDIndustrialIoT.generate_did_uri()
print("Generated DID:", did)
```

-----

### Create a DID and DID Document with Ed25519

```python
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import base64

from did_iiot.did_iiot import DIDIndustrialIoT
from did_iiot.did_document import DIDDocument, VerificationMethod
from did_iiot.publicjwk import Ed25519PubliJwkey

# Generate Ed25519 key pair
private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# Serialize keys
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)

# Encode public key as base64url for JWK
public_key_base64url = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8').rstrip("=")

# Build the verification method
pub_jwk = Ed25519PubliJwkey(public_key_base64url)
ver_method = VerificationMethod("k0", "JsonWebKey2020", pub_jwk)

# Generate DID and create the DID Document
did = DIDIndustrialIoT.generate_did_uri()
did_document = DIDDocument(did, [ver_method])

print(did_document.to_json())
```

-----

### Add a Service Endpoint

```python
from did_iiot.did_document import Service, ServiceType

service = Service(
    id=f"{did}#service-1",
    type=ServiceType.DecentralizedWebNode,
    service_endpoint="127.0.0.1:8080"
)

did_document.add_service(service)
print(did_document.to_json())
```

-----

## Related Projects

- [did-iiot-dht](https://github.com/fratrung/did-iiot-dht) — framework for building post-quantum SSI systems using `did:iiot` and a custom DHT
- [AuthKademlia](https://github.com/fratrung/AuthKademlia) — custom DHT acting as a Verifiable Data Registry for DID Documents
- [ICS_Cyber_Range](https://github.com/fratrung/ICS_Cyber_Range) — proof-of-concept IIoT deployment integrating `did:iiot`