# DNS Exfiltration Detection System

DNS Exfiltration Detection System is a cybersecurity and machine learning project that detects DNS tunneling activity in network traffic.

DNS tunneling is a covert channel technique where attackers encode stolen data inside DNS queries, usually by placing long, random-looking encoded payloads inside subdomains. This project is designed to identify such suspicious DNS behavior using protocol-level DNS parsing, feature engineering, classical machine learning, deep learning, and a live dashboard.

The project is being built from scratch in milestones. The current completed milestone is **M1A — UDP Socket and Raw Byte Receiver**.

---

## Current Status

| Milestone |   Status | Description                                                       |
| --------- | -------: | ----------------------------------------------------------------- |
| M0        | Complete | Repository structure, README, `.gitignore`, and placeholder files |
| M1A       | Complete | UDP socket listens locally and prints raw packet bytes as hex     |
| M1B       |     Next | Parse the 12-byte DNS header from received DNS packets            |

---

## Tech Stack

* Python
* Python `socket` module
* SQLite
* scikit-learn
* Keras
* Streamlit

Later milestones will add ML models, logging, feature extraction, and dashboard components.

---

## Repository Structure

```text
dns-exfil-detector/
├── dns_server/
│   ├── server.py
│   ├── parser.py
│   ├── forwarder.py
│   └── logger.py
├── pipeline/
│   ├── features.py
│   ├── dataset.py
│   └── scorer.py
├── models/
│   ├── phase1_classical.ipynb
│   ├── phase2_autoencoder.ipynb
│   └── phase3_lstm_cnn.ipynb
├── dashboard/
│   └── app.py
├── attack_sim/
│   └── tunnel_sim.py
├── tests/
│   └── test_parser.py
├── data/
│   └── download.sh
├── demo/
│   └── screenshots/
├── requirements.txt
└── README.md
```

---

## Environment Setup

### 1. Create a virtual environment

From the project root:

```bash
python -m venv .venv
```

On systems where `python` points to Python 2 or is unavailable, use:

```bash
python3 -m venv .venv
```

### 2. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

After activation, your terminal should show `(.venv)`.

### 3. Confirm Python works

```bash
python --version
```

### 4. Install dependencies

At the M1A stage, no third-party Python dependencies are required. The UDP server uses Python’s built-in `socket` module.

Later milestones will use:

```bash
pip install -r requirements.txt
```

---

## Development Port

The roadmap uses port `5353`, but this port may already be occupied on some systems by mDNS, Bonjour, or local discovery services.

For local development, this project currently uses:

```text
127.0.0.1:2053
```

So `dns_server/server.py` should contain:

```python
HOST = "127.0.0.1"
PORT = 2053
BUFFER_SIZE = 512
```

This still tests the same concept: a UDP socket bound to localhost on a non-privileged development port.

---

## M1A — UDP Socket and Raw Byte Receiver

### Goal

M1A builds the first entry point of the DNS server.

The server should:

* Open a UDP socket.
* Bind to `127.0.0.1:2053`.
* Wait for incoming packets.
* Print the sender address.
* Print the raw packet bytes as a hex string.
* Continue listening after each packet.

At this stage, the server does **not** parse DNS, respond to DNS queries, forward packets, or log to SQLite.

---

## Running the M1A Server

From the project root:

```bash
python dns_server/server.py
```

On Windows PowerShell, this also works:

```powershell
python .\dns_server\server.py
```

Expected output:

```text
DNS UDP server listening on 127.0.0.1:2053
```

Leave this terminal open while running tests from a second terminal.

---

## Installing Test Tools

M1A uses two kinds of tests:

1. A basic UDP packet test.
2. A real DNS query packet test.

The basic UDP test can be done with Python, so no extra tool is required.

For the real DNS packet test, install `dig`.

### Windows

Install BIND tools:

```powershell
winget install -e --id ISC.Bind
```

Check installation:

```powershell
dig -v
```

In PowerShell, commands using `@127.0.0.1` may need `--%` so PowerShell does not interpret `@` specially.

### Linux

Install DNS utilities.

On Debian/Ubuntu:

```bash
sudo apt update
sudo apt install dnsutils
```

Check installation:

```bash
dig -v
```

### macOS

`dig` is usually preinstalled.

Check:

```bash
dig -v
```

If unavailable, install BIND with Homebrew:

```bash
brew install bind
```

---

## M1A Test 1 — Basic UDP Packet

This test sends the raw bytes for `hello` to the UDP server.

### Terminal 1

Run the server:

```bash
python dns_server/server.py
```

### Terminal 2

Run:

```bash
python -c "import socket; s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.sendto(b'hello', ('127.0.0.1', 2053)); s.close()"
```

### Expected server output

```text
Received 5 bytes from ('127.0.0.1', some_port)
Raw hex: 68656c6c6f
```

Explanation:

```text
68 65 6c 6c 6f = hello
```

This proves the UDP socket can receive raw bytes.

---

## M1A Test 2 — Real DNS Packet with `dig`

This test sends a real DNS query to the UDP server.

### Terminal 1

Run the server:

```bash
python dns_server/server.py
```

### Terminal 2

On Linux/macOS:

```bash
dig @127.0.0.1 -p 2053 google.com
```

On Windows PowerShell:

```powershell
dig --% @127.0.0.1 -p 2053 google.com
```

### Expected server output

```text
Received 40+ bytes from ('127.0.0.1', some_port)
Raw hex: ...
```

A successful example may look like:

```text
Received 51 bytes from ('127.0.0.1', 51347)
Raw hex: 33650120000100000000000106676f6f676c6503636f6d000001000100002904d000000000000c000a000894b4469ab64243a9
```

Important observations:

```text
3365
```

This is the DNS transaction ID. It is non-zero, which confirms that a real DNS packet was received.

```text
06676f6f676c6503636f6d00
```

This is the DNS wire-format encoding of:

```text
google.com
```

Breakdown:

```text
06 = next label has 6 bytes
67 6f 6f 67 6c 65 = google
03 = next label has 3 bytes
63 6f 6d = com
00 = end of domain name
```

---

## Why `dig` Times Out in M1A

During M1A, the server only receives packets and prints them.

It does not send DNS responses yet.

So this output from `dig` is expected:

```text
connection timed out; no servers could be reached
```

This is not an error for M1A.

It means:

```text
dig sent a DNS query
the server received it
the server did not respond yet
dig retried and eventually timed out
```

Response generation comes in a later milestone.

---

## Common M1A Issues

### Error: `PermissionError: [WinError 10013]`

Example:

```text
PermissionError: [WinError 10013] An attempt was made to access a socket in a way forbidden by its access permissions
```

Possible causes:

* Another copy of the server is already running on the same port.
* The selected port is blocked or reserved by the operating system.
* Port `5353` is occupied by mDNS, Bonjour, or another local service.

Fix:

1. Stop any running server with `Ctrl + C`.
2. Use port `2053` instead of `5353`.
3. Restart the server.

### Error: `dig` not recognized

If `dig` is not recognized, confirm that BIND tools were installed correctly and that the BIND tools directory is available in your terminal PATH.

On Windows, close and reopen the terminal after installation. If needed, use the full path to `dig.exe` or add the BIND tools directory to PATH.

### Error: PowerShell rejects `@127.0.0.1`

If this command fails in PowerShell:

```powershell
dig @127.0.0.1 -p 2053 google.com
```

Use:

```powershell
dig --% @127.0.0.1 -p 2053 google.com
```

The `--%` tells PowerShell to stop parsing the rest of the command.

---

## M1A Completion Checklist

M1A is complete when:

* [x] `server.py` starts without crashing.
* [x] The server listens on `127.0.0.1:2053`.
* [x] Sending `hello` produces a raw hex dump.
* [x] The hex dump shows raw bytes, not decoded text.
* [x] The sender address is printed.
* [x] A real DNS query from `dig` produces a longer hex dump.
* [x] `dig` timing out is understood as expected behavior.

Save the screenshot of the DNS packet hex dump here:

```text
demo/screenshots/M1A_udp_receive.png
```

---

## Git Commit for M1A

After saving the screenshot:

```bash
git add dns_server/server.py README.md demo/screenshots/M1A_udp_receive.png
git commit -m "M1A: UDP socket receives raw DNS bytes"
```

---

## Demo

To be filled in after M8.

---

## Results

To be filled in after M7.

---

## Next Milestone

### M1B — Parse the DNS Header Section

The next milestone will parse the first 12 bytes of the received DNS packet.

The DNS header contains:

* Transaction ID
* Flags
* Question count
* Answer count
* Authority count
* Additional count

M1A proved that raw bytes are entering the program. M1B will start converting those bytes into structured DNS fields.
