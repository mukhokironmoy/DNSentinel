### What You Are Building

A module that, when your server receives a query it cannot answer from a local record, forwards the raw query packet to `8.8.8.8:53`, waits for the real response, and relays that response back to the original client. Your server becomes a functional recursive resolver.

### How This Fits Into The Project

```
[ Client — dig / browser ]
        ↓  query
[ M1A–M1G — DNS Server ]
        ↓  query forwarded
>>> [ M2A — Forwarder → 8.8.8.8 ] <<<
        ↓  real response relayed back
[ Client receives correct answer ]
        ↓
[ M2B — Logger captures every forwarded query ]
```

This is the position in a real network where your detector sits. Every query that goes through your server — including tunneling queries — passes through the forwarder. The logger (M2B) taps into this stream. This is also what makes your server a realistic simulation of corporate DNS infrastructure.

### What You Need To Know

- You open a second UDP socket to talk to 8.8.8.8, separate from the one listening on 5353
- Send the raw query bytes you received unchanged to `8.8.8.8:53`
- Use `socket.settimeout(5)` to avoid hanging if 8.8.8.8 does not respond
- Receive the response from 8.8.8.8 and send those raw bytes back to the original client address
- You are acting as a transparent proxy — you do not need to parse the upstream response at all. Just relay bytes.

### What To Study

Search exactly these. Time cap: 10 minutes.

- `python udp socket sendto recvfrom timeout`
- `DNS recursive resolver forwarding`

### Practice Exercise

Outside the project folder, write a minimal UDP client that sends the string "hello" to `8.8.8.8:53` and tries to receive a response (it will get garbage or timeout — that is fine). Confirm you can open a second socket, send to an external address, and receive back within a timeout. Delete when done.

### Implementation — What To Build

Create `dns_server/forwarder.py`:

Write a function that:

- Accepts the raw query bytes and the upstream resolver address (default `8.8.8.8`, port `53`)
- Opens a new UDP socket
- Sets a 5-second timeout on that socket
- Sends the raw query bytes to the upstream resolver
- Receives the response (use a buffer of 4096 bytes for responses, which can be larger than queries)
- Returns the raw response bytes
- Raises or returns None on timeout — do not crash the main server loop

Integrate into `server.py`: after parsing the incoming query, call the forwarder, then relay the response bytes back to the original client using the main socket's `sendto`. Remove the hardcoded `127.0.0.1` answer from M1G — now you return real responses.

### Checklist

- [ ] `dig @127.0.0.1 -p 5353 google.com` returns Google's real IP address (not 127.0.0.1)
- [ ] `dig @127.0.0.1 -p 5353 github.com` returns GitHub's real IP address
- [ ] The forwarder has a timeout and does not hang the server on upstream failure
- [ ] The main server loop continues after a forwarding timeout without crashing

### Test Cases

**Test 1 — Real resolution**
Run your server. Fire `dig @127.0.0.1 -p 5353 google.com`. Compare the returned IP to `dig google.com` (using your normal resolver). They should match or both be valid Google IPs.

**Test 2 — Multiple queries**
Fire three consecutive dig queries for different domains. All three should resolve correctly without restarting the server.

**Test 3 — Timeout resilience**
Temporarily change the upstream address to `1.2.3.4:53` (a non-existent resolver). Fire a dig query. Your server should timeout gracefully and log an error, but NOT crash. Restore `8.8.8.8` after testing.

Screenshot your terminal showing a real IP returned for `google.com` and save to `demo/screenshots/M2A_forwarding.png`.

### Re-entry Note

What you built: a functioning recursive DNS resolver that forwards queries to 8.8.8.8.
What comes next: logging every query to SQLite so the ML pipeline has data to read.
Next node: M2B — SQLite query logger.
If returning after a break: run a dig query and confirm you get a real IP back.

---