### What You Are Building

A function that constructs a DNS answer record in wire format — encoding the name, record type, class, TTL, and resource data (RDATA). For an A record this means encoding an IPv4 address as 4 bytes. This is the final piece needed to send a complete, valid DNS response.

### How This Fits Into The Project

```
[ M1E — Response Header ]
[ M1F — Question Section ]
>>> [ M1G — Answer Section ] <<<
        ↓  all three concatenated = complete response packet
[ M2A — Forwarder sends real responses ]
[ M2B — Logger captures everything ]
```

Once you can write a complete response packet (header + question + answer), your server can respond to queries. This makes it a functional DNS resolver — the position in a real network where you would deploy the detection layer.

### What You Need To Know

- A DNS answer record (resource record) has this structure: Name, Type (2 bytes), Class (2 bytes), TTL (4 bytes), RDLENGTH (2 bytes), RDATA (variable)
- For an A record (type 1): RDATA is exactly 4 bytes representing the IPv4 address (one byte per octet)
- `socket.inet_aton("1.2.3.4")` converts an IP string to 4 bytes
- The Name field in the answer can use a pointer back to the question section name to save space — the pointer `\xc0\x0c` points to offset 12 (where the question name starts in every standard packet)
- TTL is how long the response can be cached — use 60 (seconds) for testing
- RDLENGTH for an A record is always 4

### What To Study

Search exactly these. Time cap: 10 minutes.

- `DNS resource record format wire format`
- `python socket inet_aton`

### Practice Exercise

Outside the project folder, manually construct the bytes for an A record answer for `"1.2.3.4"` with TTL 60, using a pointer `\xc0\x0c` for the name. Write out each field by hand in hex and confirm the total is 16 bytes: 2 (pointer) + 2 (type) + 2 (class) + 4 (TTL) + 2 (RDLENGTH) + 4 (RDATA) = 16. Delete when done.

### Implementation — What To Build

Add to `dns_server/parser.py`:

Write a function that:

- Accepts: an IP address string, a TTL integer, and optionally a name offset for compression
- Uses a pointer (`\xc0\x0c`) for the name field (pointing to offset 12 in the packet)
- Packs Type=1 (A), Class=1 (IN), TTL, RDLENGTH=4 using struct.pack
- Converts the IP string to 4 bytes using socket.inet_aton
- Returns all fields concatenated as bytes

Then, in `server.py`, assemble a complete response for any query by:
- Writing the response header (M1E)
- Echoing the question section (M1F)
- Appending a hardcoded answer (M1G) — use `"127.0.0.1"` as the answer IP for now
- Sending the assembled bytes back to the client using `sendto`

### Checklist

- [ ] A complete response packet is assembled from header + question + answer bytes
- [ ] The response is sent back to the querying client using sendto
- [ ] Running `dig @127.0.0.1 -p 5353 anything.com` returns an IP address (127.0.0.1)
- [ ] `dig` no longer hangs — it receives and displays the response

### Test Cases

**Test 1 — dig responds**
Run your server. Fire `dig @127.0.0.1 -p 5353 google.com`. The `dig` command should complete (not hang) and show an answer section with IP `127.0.0.1`. This is the first time your server responds to a query.

**Test 2 — Answer bytes length**
In a unit test, assert that your write_answer function returns exactly 16 bytes for an A record.

**Test 3 — Packet sanity**
Capture the full response packet your server sends (print it as hex). Parse it with your own header parser. Assert the ANCOUNT field equals 1. This proves your response has exactly one answer.

Screenshot `dig` returning a result and save to `demo/screenshots/M1G_first_response.png`.

### Re-entry Note

What you built: complete DNS response construction. Your server now speaks DNS.
What it does NOT do yet: forward to real resolvers — it returns a fake IP for everything.
Next node: M2A — forward queries to 8.8.8.8 and return real responses.
If returning after a break: run dig and check that it gets a response.

---