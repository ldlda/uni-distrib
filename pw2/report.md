# RPC File Transfer Report

## Overview

This document describes the file transfer system upgraded to use Remote Procedure Calls (RPC). It utilizes Python's built-in `xmlrpc` library to abstract the network communication, simplifying the implementation compared to raw TCP sockets.

## System Design

The system follows a client-server architecture where the server exposes a method `write_file` via XML-RPC. The client invokes this method remotely to transfer files.

### Architecture Diagram

```mermaid
graph LR
    Client[Client Application]
    Server[Server Application]
    XMLRPC[XML-RPC Protocol]
    
    Client -- "write_file(name, content)" --> XMLRPC
    XMLRPC -- "HTTP POST" --> Server
    Server -- "Returns (path, size)" --> XMLRPC
    XMLRPC -- "Response" --> Client
```

## Implementation

### Server Implementation

The server uses `DocXMLRPCServer` to expose the `write_file` function. It handles binary data using `xmlrpc.client.Binary`.

```python
def write_file(name: str, content: bytes | xmlrpc.client.Binary) -> tuple[str, int]:
    # Handle XML-RPC Binary wrapper
    if isinstance(content, xmlrpc.client.Binary):
        content = content.data
        
    p = Path(os.path.normpath(name))
    siz = p.write_bytes(content)
    return p.as_posix(), siz
```

### Client Implementation

The client uses `ServerProxy` to call the remote method. It wraps file content in `xmlrpc.client.Binary` to ensure correct transmission of binary data over XML-RPC.

```python
client = xmlrpc.client.ServerProxy(f"http://{HOST}:{PORT}/")
with Path("file_to_send").open("rb") as f:
    b = f.read()
# Wrap binary data
client.write_file("destination_name", xmlrpc.client.Binary(b))
```

## Challenges and Fixes

### Binary Data Handling

**Issue**: Initially, the transfer failed with a `TypeError`. The XML-RPC protocol requires binary data to be wrapped in a specific `Binary` object, but `Path.write_bytes` expects a bytes-like object.

**Fix**:

1. **Client Side**: Updated the client to explicitly wrap the file content using `xmlrpc.client.Binary(b)`.
2. **Server Side**: Updated the server function to check for the `xmlrpc.client.Binary` type and extract the raw bytes using the `.data` attribute before writing to disk.

## Team

- **Implementation**: Gemini 3 Pro / Copilot & D. A. Luong
- **Report**: Gemini 3 Pro / Copilot
