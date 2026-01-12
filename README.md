# Trojan-Delivery-Exfil-POC

![Project Status](https://img.shields.io/badge/Status-Educational_PoC-blue) ![Language](https://img.shields.io/badge/Language-Python_%7C_NSIS-green) ![Focus](https://img.shields.io/badge/Focus-Red_Team_Ops-red)

## Disclaimer
**This software is a Proof of Concept (PoC) developed strictly for educational purposes and security research.** It simulates a specific attack vector (installer bundling) to aid in understanding supply chain vulnerabilities and developing better detection heuristics. **Do not use this software on systems without explicit authorization.**

## Overview
**Trojan-Delivery-Exfil-POC** is a modular framework designed to simulate a "Trojanized" software delivery chain. It demonstrates how an attacker can bundle a malicious payload alongside a legitimate, signed application to evade user suspicion and basic heuristic detection.

The project was built to explore:
* **Installer Bundling:** Embedding user-land payloads within legitimate installers using NSIS.
* **Custom Exfiltration Protocols:** Implementing raw TCP socket communication with binary packing for data transfer.
* **Process Evasion:** Techniques for silent background execution and forensic cleanup.

## System Architecture

The framework consists of three primary components simulating the full attack lifecycle:

### 1. Delivery Mechanism (`installer.nsi`)
The core delivery vector is an NSIS (Nullsoft Scriptable Install System) script that compiles multiple binaries into a single setup executable.
* **Dropper Logic:** Extracts the payload, exfiltration client, and a decoy application ("SignedApp.exe") to `$LOCALAPPDATA\Updater`.
* **Silent Execution:** Utilizes `nsExec` to spawn the payload and client processes in the background without creating visible console windows.
* **User Deception:** Immediately launches the legitimate decoy application (optionally with elevated privileges via `runas`) to maintain the illusion of a successful install.
* **Forensic Cleanup:** Implements a sleep timer (120 seconds) to allow background processes to complete before attempting to wipe the payload artifacts from the disk.

### 2. Exfiltration Client (`client.py`)
A lightweight Python client responsible for securely transporting captured data to the C2 server.
* **Custom Binary Protocol:** Instead of using standard HTTP/FTP, this client uses a custom packed struct format to minimize overhead.
    * **Format:** `[Filename Length (4 bytes)]` + `[Filename (N bytes)]` + `[File Size (8 bytes)]` + `[Data Chunk]`
* **Efficiency:** Uses `struct.pack('>Q')` (unsigned long long) for file size headers, enabling the transfer of large files efficiently.
* **Hardcoded Targets:** Configured to target a specific listener IP.

### 3. C2 Listener (`server.py`)
A standalone server script that listens for incoming connections and reconstructs exfiltrated files.
* **Automated Organization:** Incoming files are automatically saved to a `loot` directory (configurable), prefixed with the victim's IP address for easy attribution.
* **Robust Handling:** Dynamically handles file streams based on the custom protocol headers to ensure data integrity.

## Usage & Configuration

### Prerequisites
* Python 3.x
* NSIS (Nullsoft Scriptable Install System) compiler

### 1. Configure the Client
Modify `client.py` to point to your listener's IP address and port:
```python
# client.py
KALI_IP = '192.168.1.101'  # Change to your listener IP
PORT = 5001                # Change to your listener port
```
### 2. Prepare the Bundle
Compile your payload and the client.py script into standalone executables (e.g., using PyInstaller). Place them in the project directory alongside a legitimate "decoy" installer (SignedApp.exe).

### 3. Build the Installer
Compile the installer.nsi script. This will generate Setup_Signed.exe:

```Bash

makensis installer.nsi
```
### 4. Start the Listener
Run the server on your listening machine:

```Bash

python3 server.py --port 5001 --dir ./loot
```
## Project Structure
```
.
├── installer.nsi       # NSIS script for bundling and deployment logic
├── client.py           # Exfiltration client (sends data via TCP)
├── server.py           # Listener (receives data and saves to disk)
├── SignedApp.exe       # (Placeholder) The legitimate decoy application
└── Payload.exe         # (Placeholder) The actual payload to be executed
```
## License
This project is open-source and available under the MIT License.
