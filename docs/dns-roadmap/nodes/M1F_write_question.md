### What You Are Building

A function that encodes a domain name string back into DNS wire format (length-prefixed labels) and appends the QTYPE and QCLASS bytes. This is the inverse of the question parser from M1C.

### How This Fits Into The Project

```
[ M1C — Parse Question ] → domain string
>>> [ M1F — Write Question ] <<<
        ↓  wire-format question bytes
[ M1G — Write Answer Section ]
        ↓
[ complete response packet ]
```

DNS responses echo the question section back to the client. You need to encode the domain name back into wire format to include it in your response. This is also the format used when generating synthetic tunneling queries in M4B.

### What You Need To Know

- Encoding is the reverse of decoding: split the domain by dots, for each label write its length as one byte then the label bytes, then write a zero byte to terminate
- `"google.com"` becomes `\x06google\x03com\x00`
- After the encoded name, append 4 bytes: 2 bytes for QTYPE and 2 bytes for QCLASS using struct.pack
- QCLASS is almost always 1 (IN for internet)

### What To Study

No new searches needed — this is the direct inverse of M1C. Re-read your M1C notes if needed.

### Practice Exercise

Outside the project folder, write `encode_name("mail.google.com")` and confirm it returns `b'\x04mail\x06google\x03com\x00'`. Verify byte by byte. Delete when done.

### Implementation — What To Build

Add to `dns_server/parser.py`:

Write a function that:

- Accepts a domain name string and a QTYPE integer
- Splits the domain by dots
- Encodes each label as a length byte followed by the ASCII bytes of the label
- Appends a zero byte to terminate
- Appends QTYPE as a 2-byte big-endian unsigned short
- Appends QCLASS as 1 (IN) as a 2-byte big-endian unsigned short
- Returns all of this as a bytes object

### Checklist

- [ ] `encode_name("google.com")` returns `b'\x06google\x03com\x00'` before QTYPE/QCLASS
- [ ] Round-trip: encoding then decoding returns the original domain string
- [ ] QTYPE and QCLASS bytes are appended correctly

### Test Cases

**Test 1 — Encoding correctness**
Assert `encode_question("google.com", 1)` starts with `b'\x06google\x03com\x00'`.

**Test 2 — Round trip**
Encode `"fonts.googleapis.com"` with QTYPE=1. Pass the result to your question parser from M1C. Assert the decoded domain is `"fonts.googleapis.com"` and QTYPE is 1.

**Test 3 — Length**
Verify the encoded bytes for `"google.com"` are exactly 16 bytes: 1+6+1+3+1 (name) + 2 (QTYPE) + 2 (QCLASS) = 15. Wait — recalculate carefully. Write the assertion.

### Re-entry Note

What you built: DNS name encoder — the inverse of the M1C decoder.
Next node: M1G — write the answer section (the actual IP address or data being returned).
If returning after a break: run pytest.

---