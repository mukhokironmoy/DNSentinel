### What You Are Building

A function that reads the question section of a DNS packet — which starts at byte 12, immediately after the header — and extracts the domain name being queried and the record type (A, TXT, CNAME, etc.). The output is a human-readable domain string like `google.com` and an integer record type.

### How This Fits Into The Project

```
[ M1B — Header Parser ] → fields including QDCOUNT
>>> [ M1C — Question Parser ] <<<
        ↓  domain name string + record type
[ M1D — Compression Handler ]
        ↓
[ M1E — Write Header ]
        ↓
[ Logger — stores domain name in SQLite ]
```

The domain name in the question section is the core data you will later analyse for tunneling. This is where `SGVsbG8gV29ybGQ=.c2tunnel.com` appears. Without parsing this, you have no feature to feed to ML models.

### What You Need To Know

- DNS encodes domain names as a sequence of length-prefixed labels
- Each label starts with one byte that gives the length of that label, followed by that many ASCII characters
- The sequence ends with a zero byte (`\x00`)
- Example: `google.com` is encoded as `\x06google\x03com\x00` — the `\x06` means "next 6 bytes are a label", `\x03` means "next 3 bytes are a label", `\x00` means end
- After the name, there are 2 bytes for QTYPE (record type: 1=A, 28=AAAA, 5=CNAME, 16=TXT) and 2 bytes for QCLASS (almost always 1=IN for internet)
- You read the name byte by byte, accumulating labels until you hit a zero byte

Do not handle pointer compression yet — that is M1D. Assume all names are uncompressed in this node.

### What To Study

Search exactly these. Time cap: 15 minutes.

- `DNS question section format labels`
- `DNS name encoding length prefixed labels`

### Practice Exercise

Outside the project folder, write a function that decodes DNS label encoding. Test it with the hardcoded bytes for `google.com`: `b'\x06google\x03com\x00'`. It should return the string `"google.com"`. Then test with `b'\x04mail\x06google\x03com\x00'` and confirm it returns `"mail.google.com"`. Delete when done.

### Implementation — What To Build

Add to `dns_server/parser.py`:

Write a function that:

- Accepts the full raw packet bytes and a starting offset (which will be 12, right after the header)
- Reads labels one by one — first reading the length byte, then reading that many character bytes, appending to a list
- Stops when it reads a zero-length byte
- Joins the labels with dots to form the domain string
- Continues reading 4 more bytes after the name to extract QTYPE and QCLASS using struct
- Returns the domain name string, the QTYPE integer, the QCLASS integer, and the offset at which the question section ended (so the caller knows where to continue reading)

Integrate into `server.py` so that every received packet now prints the human-readable domain name being queried.

### Checklist

- [ ] The question parser correctly extracts domain names from real dig queries
- [ ] `dig @127.0.0.1 -p 5353 google.com` causes your server to print `google.com`
- [ ] `dig @127.0.0.1 -p 5353 mail.google.com` causes your server to print `mail.google.com`
- [ ] QTYPE is extracted and printed (should be 1 for A record queries from dig)
- [ ] The function returns the end offset so future parsers know where to continue

### Test Cases

**Test 1 — Known bytes unit test**
Add to `tests/test_parser.py`. Hardcode a minimal DNS packet bytes literal that encodes a query for `google.com` (you can capture one from Wireshark or construct it manually using the label format). Assert that your function returns `"google.com"` as the domain and `1` as the QTYPE.

**Test 2 — Multi-label domain**
Fire `dig @127.0.0.1 -p 5353 fonts.googleapis.com`. Server should print `fonts.googleapis.com`. This tests three-label parsing.

**Test 3 — Different record type**
Fire `dig @127.0.0.1 -p 5353 google.com TXT`. Server should print QTYPE = 16 (TXT). This confirms QTYPE extraction works.

Run `python -m pytest tests/` and confirm all tests pass.

### Re-entry Note

What you built: DNS label decoder that turns wire-format names into human-readable strings.
What it does NOT handle: compressed names with pointer bytes (names that start with `\xc0`).
Next node: M1D — handle DNS name compression (pointer bytes).
If returning after a break: run `dig @127.0.0.1 -p 5353 google.com` and check that your server prints the domain name.

---