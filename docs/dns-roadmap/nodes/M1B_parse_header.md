### What You Are Building

A function that takes the raw bytes received in M1A and extracts the 6 fields of the DNS header: Transaction ID, Flags, Question Count, Answer Count, Authority Count, Additional Count. The output is a structured object or dictionary, not raw bytes.

### How This Fits Into The Project

```
[ M1A — UDP Socket ] → raw bytes
>>> [ M1B — Header Parser ] <<<
        ↓  structured header fields
[ M1C — Question Parser ]
        ↓
[ Logger ]
```

The DNS header is the first 12 bytes of every DNS packet. It tells you what kind of packet this is, how many questions are in it, and how many answers. Without parsing this, you cannot know where the question section starts or what kind of response to build.

### What You Need To Know

- The DNS header is always exactly 12 bytes, fixed structure
- Python's `struct` module unpacks binary data into Python values using format strings
- The format string `!6H` means: big-endian (`!`), six unsigned short integers (`H`), each 2 bytes — total 12 bytes
- The six fields in order: Transaction ID, Flags, QDCOUNT (questions), ANCOUNT (answers), NSCOUNT (authority), ARCOUNT (additional)
- `struct.unpack('!6H', data[:12])` returns a tuple of 6 integers

That is all. Do not parse flags in detail yet — just extract the raw integer. Flag breakdown comes later when you need it.

### What To Study

Search exactly these. Time cap: 10 minutes.

- `python struct unpack big endian example`
- `DNS header format fields`

### Practice Exercise

Outside the project folder, create `scratch_struct.py`. Write a function that takes any 12 bytes and returns a dictionary with keys `transaction_id`, `flags`, `qdcount`, `ancount`, `nscount`, `arcount`. Test it with hardcoded bytes: `b'\x12\x34\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'`. Confirm `transaction_id` is `0x1234` (4660 decimal). Delete the scratch file when done.

### Implementation — What To Build

File to create: `dns_server/parser.py`

Write a function that:

- Accepts raw bytes as input (the full packet received from the socket)
- Reads exactly the first 12 bytes
- Unpacks those 12 bytes into 6 unsigned 16-bit integers using the struct module
- Returns a dictionary or dataclass with the six header field names and their integer values
- Does not crash if given fewer than 12 bytes — it should raise a clear, descriptive error in that case

Integrate this into `dns_server/server.py` so that after receiving each packet, the header is parsed and the structured fields are printed alongside the raw hex. You should see both the hex dump and human-readable field values for each incoming packet.

### Checklist

- [ ] `parser.py` contains a header parsing function
- [ ] The function returns all six header fields by name
- [ ] The server now prints structured header fields for every received packet
- [ ] Sending a dig query shows Transaction ID, Flags, and QDCOUNT = 1 in the output
- [ ] The function raises a meaningful error on malformed input (less than 12 bytes)

### Test Cases

**Test 1 — Known bytes**
Write a unit test in `tests/test_parser.py`. Hardcode the bytes `b'\xab\xcd\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'` and assert that your function returns `transaction_id = 0xabcd` (43981), `qdcount = 1`, `ancount = 0`. Run with `python -m pytest tests/`.

**Test 2 — Live packet**
Run the server. Fire `dig @127.0.0.1 -p 5353 google.com`. Your server should now print something like: `Transaction ID: 12345 | Flags: 256 | Questions: 1 | Answers: 0`. The Questions count should always be 1 for a standard dig query.

**Test 3 — Error handling**
In a Python shell, call your parse function with `b'\x00\x01'` (only 2 bytes). It should raise an error with a message that makes it clear the input is too short — not an unreadable struct error.

### Re-entry Note

What you built: DNS header parser using struct.unpack.
What it does NOT do: parse the question section (the domain name itself).
Next node: M1C — parse the question section, which contains the actual domain name being queried.
If returning after a break: run `python -m pytest tests/` — if tests pass, parser still works.

---