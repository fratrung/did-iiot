# DID-IIoT: Decentralized Identifier Method for Industrial IoT

DID-IIoT is a **Decentralized Identifier (DID) method** specifically designed for **Industrial Internet of Things (IIoT)** environments. Tailored for **private and internal networks**, this method ensures flexibility and independence from the underlying ledger technology, allowing the use of various registries such as Distributed Hash Tables (DHT), blockchain, web servers, or centralized registries.

> **Note**: This method is still under active development and open to modifications. Contributions and feedback are highly encouraged to refine and enhance the DID-IIoT standard.

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

## Introduction

The **DID-IIoT** method provides a flexible framework for generating and managing **Decentralized Identifiers** in industrial IoT networks. By leveraging **UUID version 4** for unique identifier generation and adhering to the **W3C DID Core specification**, DID-IIoT aims to deliver secure, scalable, and interoperable identity management. 

This method is still **in progress**, and its design and features may evolve to better address the needs of Industrial IoT applications. Your feedback and contributions are essential to shaping this method.

## Features

- **Ledger Agnostic**: Compatible with various ledger types, including DHT, blockchain, web servers, and centralized registries.
- **W3C Compliance**: Adheres to the W3C DID Core specification for interoperability.
- **Security**: Supports public keys, service endpoints, and digital signatures for secure updates and key rotations.
- **Scalability**: Designed to handle large-scale industrial deployments with numerous devices.
- **Flexibility**: Suitable for internal and private network environments, independent of external infrastructures.

## How It Works

### Create DID

The DID-IIoT method autonomously generates a **DID URI** and its corresponding **DID Document**. This process involves:


1. **Generating a UUID Version 4**: Each DID is created using a UUID version 4 to ensure uniqueness.
2. **Specifying the Network Namespace (optionally)**: The network namespace categorizes the DID within the industrial IoT environment.
3. **Constructing the DID URI**: The DID URI follows the format:

    ```
    
    did:iiot:93865a36-e510-4d21-a09a-8575057a883f
    ```

    **Example with network namespace :**

    ```
    did:iiot:internal.network:93865a36-e510-4d21-a09a-8575057a883f
    ```

### DID Document

The **DID Document** complies with the **W3C DID Core specification** and includes:

- **Public Keys**: For authentication and verification.
- **Service Endpoints**: To facilitate interactions and service discovery.
- **Metadata**: Optional information to enhance functionality.

These components enable secure authentication, efficient service discovery, and compatibility with decentralized identity standards.

### DID Resolution

The **DID resolution** process depends on the network's configuration. It retrieves the DID Document from the chosen registry (DHT, blockchain, web server, etc.) to resolve the DID to its associated metadata and service endpoints.

### Update DID

Updating a DID Document involves:

1. **Overwriting the Existing Document**: Replacing the current document with an updated version.
2. **Digital Signature**: Each update must be digitally signed using the entity's private key to ensure authenticity and integrity.
3. **Signature Verification**: The update is verified by checking the signature against the public key (`k0`) in the existing DID Document.

### Key Rotation

Key rotation is managed through the DID Document update mechanism:

1. **Replace the Existing Key**: Update the old public key (`k0`) with a new one.
2. **Sign the Update**: Use the private key corresponding to the previous public key to sign the update.
3. **Prevent Replay Attacks**: Implement safeguards like version counters, timestamps, unique nonces, or hashes of the previous state to ensure updates are secure and verifiable.

In immutable registries like blockchain, the registry's inherent properties enhance the key rotation process.

### Revoke DID

Revoking a DID ensures it is no longer usable. Depending on the registry's capabilities, this can be done in one of two ways:

1. **Permanent Removal**: If the registry supports it, the DID Document is completely removed, rendering the DID inaccessible and unusable.

2. **Deactivation**: If removal is not supported, the DID Document is replaced with a version marked as `'Deactivated'`. This ensures the DID remains inactive while preserving its existence in the registry.

This method provides flexibility, allowing for revocation in environments with either mutable or immutable registries.

## Installation

To integrate DID-IIoT into your Industrial IoT environment, follow these steps:

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/did-iiot.git
    ```

2. **Navigate to the Project Directory**

    ```bash
    cd did-iiot
    ```

3. **Install Dependencies**

    Ensure you have Python 3.6+ installed, then install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Creating a DID

Use the provided Python module to generate a new DID:

```python
from did_iiot import DIDIndustrialIoT

# Create a new DID with a specified network namespace
did = DIDIndustrialIoT.generate_did_uri()

print("Generated did:iiot uri: ", did)
```
### Example: Create DID and DID Document with Ed25519

```python
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
import base64
from did_iiot.did_iiot import DIDIndustrialIoT
from did_iiot.did_document import DIDDocument, VerificationMethod
from did_iiot.publicjwk import Ed25519PubliJwkey

# Generate a new Ed25519 private key and corresponding public key
private_key = ed25519.Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# Serialize the private key in PEM format
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

# Serialize the public key in Raw format
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)

# Convert the public key to base64url for use in a JWK
public_key_base64url = base64.urlsafe_b64encode(public_key_bytes).decode('utf-8').rstrip("=")

# Create a public JWK from the base64url encoded public key
pub_key = Ed25519PubliJwkey(public_key_base64url)

# Create a VerificationMethod using the public key
ver_method = VerificationMethod("k0", "JsonWebKey2020", pub_key)

# List of verification methods (could be extended with multiple methods)
verification_methods = []
verification_methods.append(ver_method)

# Generate a DID URI using the DIDIndustrialIoT method
did = DIDIndustrialIoT.generate_did_uri()

# Create the DID Document
did_document = DIDDocument(did, verification_methods)

# Print the DID Document in JSON format
print(did_document.to_json())
```
### Update DID Example
```python

from did_iiot.did_document import Service, ServiceType
service = Service(id=f"{did}#service-1",type=ServiceType.DecentralizedWebNode,service_endpoint="127.0.0.1:8080")

did_document.add_service(service)

print(did_document.to_json())

```