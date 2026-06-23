### What You Are Building

A Python script that opens a UDP socket on port 5353, listens for incoming packets in a loop, and prints the raw bytes of whatever arrives. No parsing yet. Just receive and print.

### How This Fits Into The Project

```
[ Attack Simulator ]
        ↓  UDP packets over port 5353
>>> [ M1A — UDP Socket ] <<<
        ↓  raw bytes
[ M1B — Header Parser ]
        ↓
[ M1C — Question Parser ]
        ↓
[ Logger → Feature Extraction → ML Models ]
```

Every DNS query that will later be parsed, logged, scored, and classified first arrives here as raw bytes. This is the entry point to the entire system. Nothing works without this.

### What You Need To Know

- DNS uses UDP, not TCP. UDP is connectionless — a packet arrives, you read it, done. No handshake.
- `socket.SOCK_DGRAM` is the constant for UDP sockets
- `recvfrom(buffer_size)` blocks until a packet arrives and returns `(data, address)` — data is raw bytes, address is `(ip, port)` of the sender
- Port 5353 does not require root privileges. Port 53 does. Use 5353 during development.
- DNS packets over UDP are capped at 512 bytes by the original spec

That is all. Do not read about DNS packet structure yet — that is M1B.

### What To Study

Search exactly these. Time cap: 10 minutes.

- `python socket SOCK_DGRAM recvfrom example`
- `python udp server minimal example`

### Practice Exercise

Outside the project folder, create `scratch_udp.py`. Write a UDP receiver that prints "Received [N] bytes from [address]" for every packet. In a second terminal, send a test packet with:

```
echo "hello" | nc -u 127.0.0.1 5353
```

Confirm your script prints the arrival message. Then delete the scratch file.

### Implementation — What To Build

File to create: `dns_server/server.py`

Your script should do the following:

- Create a UDP socket bound to `127.0.0.1` on port `5353`
- Print a startup message confirming the server is listening
- Enter an infinite loop
- On each iteration, receive one UDP packet using a 512-byte buffer
- Print the source address of the packet
- Print the raw bytes of the packet as a hex string
- Continue waiting for the next packet

The script should be runnable directly with `python dns_server/server.py`. It should not crash on receiving a packet — it should print and loop.

### Checklist

- [ ] Running the script prints a listening confirmation message
- [ ] The script does not exit — it keeps running and waiting
- [ ] Sending a test packet causes a hex dump to appear in the terminal
- [ ] The hex dump shows the raw bytes, not decoded text
- [ ] The source address of the sender is printed alongside the dump

### Test Cases

**Test 1 — Basic receive**
Run the server. In a second terminal run: `echo "hello" | nc -u 127.0.0.1 5353`
Expected: hex dump appears in server terminal. The hex should contain `68656c6c6f` (ASCII for "hello").

**Test 2 — Real DNS packet**
Run the server. In a second terminal run: `dig @127.0.0.1 -p 5353 google.com`
Expected: a longer hex dump appears. The `dig` command will hang waiting for a response — that is correct, you are not responding yet. Ctrl+C the dig. The hex dump should be at least 20 bytes long.

**Test 3 — Transaction ID check**
Look at the first 4 hex characters of the dump from Test 2. They should not be `00000000` — this is the DNS transaction ID, which `dig` sets to a random non-zero value. Seeing a non-zero value proves you received a real DNS packet.

Screenshot your terminal showing the hex dump from Test 2 and save it to `demo/screenshots/M1A_udp_receive.png`.

### Re-entry Note

What you built: a UDP listener that prints raw DNS bytes.
What it does NOT do: parse, respond, or log.
Next node: M1B — parse the 12-byte DNS header out of those raw bytes.
If returning after a break: run the server and fire a dig command. If hex appears, everything works.

---