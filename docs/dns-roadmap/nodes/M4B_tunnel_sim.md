### What You Are Building

A Python script that simulates a DNS tunneling attack by encoding data in Base64, splitting it into chunks, and sending each chunk as a subdomain query to your DNS server. Running this script while the server and scorer are active generates realistic attack traffic in your database.

### How This Fits Into The Project

```
[ M2A — DNS Server accepting queries ]
>>> [ M4B — Tunnel Simulator generates attack traffic ] <<<
        ↓  high-entropy DNS queries hit the server
[ M2B — Logger stores them ]
[ M4A — Scorer extracts features ]
[ M5/M6/M7 — Models classify them as tunneled ]
[ M8 — Dashboard flags them red ]
```

You need attack traffic to test your detector. Without this, your database only contains normal forwarded queries. This script gives you labelled attack traffic in your live pipeline and demonstrates the attacker mindset: you built the attack before building the defense.

### What You Need To Know

- `base64.b64encode(data.encode()).decode()` converts a string to Base64
- Split the Base64 string into chunks of 30 characters each
- Send each chunk as a DNS query: `chunk.evil.test` — the chunk becomes the subdomain
- You send a DNS query by constructing a minimal DNS packet and sending it to your server via UDP
- Use `socket.SOCK_DGRAM` and `sendto` on port 5353 — the same socket type your server uses
- A minimal DNS query packet: 12-byte header (transaction ID, flags=0x0100, QDCOUNT=1, rest zeros) + question section for your domain + QTYPE=1 + QCLASS=1

### What To Study

Search exactly these. Time cap: 10 minutes.

- `python base64 encode string`
- `python send DNS query UDP manually`

### Practice Exercise

Outside the project folder, write a script that encodes "Hello World" in Base64 and splits it into chunks of 5 characters. Print each chunk as `chunk.evil.test`. Confirm the output looks like DNS subdomain queries. Delete when done.

### Implementation — What To Build

Create `attack_sim/tunnel_sim.py`:

Write a script that:

- Accepts a payload string (default: a paragraph of Lorem Ipsum or any sample text)
- Encodes the payload in Base64
- Splits the encoded string into 30-character chunks
- For each chunk, constructs a valid DNS query packet for the domain `{chunk}.evil.test`
- Sends each query to `127.0.0.1:5353` using a UDP socket
- Waits 0.1 seconds between queries (to avoid flooding)
- Prints each query name as it is sent

The script should be runnable standalone: `python attack_sim/tunnel_sim.py`

### Checklist

- [ ] Running the script while the server is active causes new rows to appear in the database
- [ ] The new rows have subdomain lengths above 20 characters
- [ ] The new rows have entropy values above 5.0 when scored by M4A
- [ ] The script sends multiple queries (at least 5) for any non-trivial payload
- [ ] The script does not crash if the server is not running (timeout gracefully)

### Test Cases

**Test 1 — Database rows**
Start the server and scorer. Run the tunnel simulator. After it completes, query the database: `SELECT query_name FROM queries WHERE length(query_name) > 30;` — you should see the Base64 subdomain queries.

**Test 2 — Entropy check**
After the scorer processes the tunneled rows, their entropy values should be above 5.0. Compare to normal dig query rows which should be below 4.0.

**Test 3 — Visual separation**
In your notebook, plot entropy distribution for rows added by dig (normal) vs rows added by the tunnel simulator (tunneled). They should form two clearly separated peaks. Save this plot to `demo/shap_plots/entropy_separation.png`.

### Re-entry Note

What you built: the attack simulator. You now have both normal and tunneled traffic in your live pipeline.
What comes next: ML models. M5A trains the first classifier on the dataset.
Next node: M5A — Random Forest classifier.
If returning after a break: run the simulator and check the database for Base64-looking query names.

---