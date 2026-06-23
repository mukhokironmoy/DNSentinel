### What You Are Building

A function that constructs the 12-byte DNS response header as raw bytes, mirroring the transaction ID of the incoming query and setting the correct flags to indicate this is a response.

### How This Fits Into The Project

```
[ M1B — Parse Header ] → incoming transaction ID and flags
>>> [ M1E — Write Response Header ] <<<
        ↓  12 bytes of response header
[ M1F — Write Question Section ]
        ↓
[ M1G — Write Answer Section ]
        ↓
[ complete response packet sent back to client ]
```

A DNS server that only reads packets is a dead end. To be a functional resolver — and to be the component that tunneling traffic passes through — you must be able to construct valid response packets. The header is the first 12 bytes of every response.

### What You Need To Know

- A DNS response has the same 6-field header structure as a query
- The key difference is in the Flags field: bit 15 (QR bit) must be set to 1 to indicate this is a response
- For a basic valid response, set flags to `0x8180`: QR=1 (response), AA=0, TC=0, RD=1 (recursion desired, mirrored from query), RA=1 (recursion available)
- The Transaction ID in the response must exactly match the Transaction ID from the query — this is how the client matches responses to requests
- Use `struct.pack('!6H', ...)` to construct the 12 bytes — the inverse of unpack

### What To Study

Search exactly these. Time cap: 10 minutes.

- `python struct pack big endian`
- `DNS response header flags QR bit`

### Practice Exercise

Outside the project folder, write a function that accepts a transaction ID integer and returns 12 bytes representing a minimal valid DNS response header for a single-question, single-answer response. Verify the output bytes have the correct transaction ID in positions 0-1 and `\x81\x80` in positions 2-3 (the flags). Delete when done.

### Implementation — What To Build

Add to `dns_server/parser.py`:

Write a function that:

- Accepts: transaction ID (integer), question count (integer), answer count (integer)
- Sets the flags field to a value appropriate for a standard recursive response
- Packs all six header fields into 12 bytes using struct.pack in big-endian format
- Returns those 12 bytes

This function is the inverse of the header parser from M1B. Test it by parsing its own output — `parse_header(write_header(...))` should return the same values you passed in.

### Checklist

- [ ] Function returns exactly 12 bytes
- [ ] The QR bit (bit 15 of flags) is set to 1 in the output
- [ ] The transaction ID in the output matches the input
- [ ] Round-trip test passes: parsing the output of write_header returns the same field values

### Test Cases

**Test 1 — Round trip**
In `tests/test_parser.py`, call `write_header(transaction_id=0x1234, qdcount=1, ancount=1)`, then pass the result to `parse_header()`. Assert that `transaction_id == 0x1234`, `qdcount == 1`, `ancount == 1`.

**Test 2 — QR bit check**
Take the 12 bytes returned by `write_header`. Extract bytes 2-3 as a big-endian unsigned short. Assert that `flags & 0x8000 == 0x8000` (QR bit is set).

**Test 3 — Length check**
Assert `len(write_header(0xabcd, 1, 1)) == 12`.

### Re-entry Note

What you built: response header constructor.
Next node: M1F — write the question section bytes for the response.
If returning after a break: run pytest. All tests should pass.

---