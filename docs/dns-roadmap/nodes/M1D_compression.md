### What You Are Building

An extension to your name parser that handles DNS pointer compression. When you see a label length byte whose top two bits are `11`, it is not a label — it is a 2-byte pointer to an earlier offset in the packet where the rest of the name already appears. Your parser must follow that pointer and resume reading from there.

### How This Fits Into The Project

```
[ M1C — Label Parser ] — works for uncompressed names
>>> [ M1D — Compression Handler ] <<<
        ↓  now handles ALL real-world DNS packets
[ M1E — Write Header ]
[ M1F — Write Question ]
```

Real DNS packets use compression extensively in responses — especially multi-answer responses. Tunneling tools also manipulate compression bytes to confuse naive parsers. Without handling compression your forwarder will receive responses from 8.8.8.8 that your parser cannot read correctly.

### What You Need To Know

- If a length byte has its top two bits set to `11` (i.e., `byte & 0xC0 == 0xC0`), it is a pointer
- A pointer is 2 bytes total. The lower 6 bits of the first byte and all 8 bits of the second byte combine to form a 14-bit offset into the packet
- You extract the offset as: `offset = ((byte1 & 0x3F) << 8) | byte2`
- You then jump to that offset in the original packet and continue reading labels from there
- Pointers can chain — the target of a pointer might itself contain a pointer — so your function must handle this recursively or iteratively
- After following a pointer, your parser should return to the position just after the 2-byte pointer in the original stream (not the pointer's target) as the "next read position"

### What To Study

Search exactly these. Time cap: 10 minutes.

- `DNS name compression pointer format`
- `DNS packet compression offset bits`

### Practice Exercise

Outside the project folder, write a minimal function that checks whether a byte is a pointer byte using the bitmask check above. Then write a second function that takes a packet (as bytes) and an offset, and returns the full decoded name following any pointers. Test it with a manually constructed packet where you hardcode a name at one offset and a pointer to it at another. Delete when done.

### Implementation — What To Build

Modify the name-parsing function in `dns_server/parser.py`:

- Before treating a length byte as a label length, first check if it is a pointer using the bitmask `byte & 0xC0 == 0xC0`
- If it is a pointer, extract the 14-bit target offset from the 2-byte sequence
- Continue reading the name from the target offset instead
- Track the position to return to in the original packet (the byte immediately after the 2-byte pointer sequence)
- Handle chains — if following a pointer leads to another pointer, follow that one too
- Do not loop infinitely — add a depth counter or visited-offsets check to prevent infinite loops on malformed packets

The function signature and return values should remain the same as M1C. Only the internals change.

### Checklist

- [ ] Pointer bytes are correctly identified using the bitmask check
- [ ] The 14-bit offset is correctly extracted from pointer bytes
- [ ] Following a pointer produces the correct name
- [ ] The parser returns the correct "next read position" after a pointer (just past the 2-byte pointer, not the target)
- [ ] Chains of pointers work correctly
- [ ] Malformed circular pointers do not cause infinite loops

### Test Cases

**Test 1 — Constructed packet with pointer**
Write a unit test where you manually construct a byte sequence: put `\x06google\x03com\x00` at offset 12, then at offset 24 put a pointer `\xc0\x0c` (pointing back to offset 12). Call your parser starting at offset 24. Assert it returns `"google.com"` and that the returned next-offset is 26 (just past the 2-byte pointer).

**Test 2 — Real forwarded response**
In M2A (forwarder) you will see full DNS responses from 8.8.8.8. Those responses contain compressed names. Run your server with forwarding enabled (after completing M2A) and fire a dig query. Parse the response packet. If the name in the answer section is correctly decoded, compression handling works.

**Test 3 — Depth guard**
Write a test where a pointer points to itself (offset pointing back to its own position). Confirm your parser raises an error or returns an empty result rather than looping forever.

### Re-entry Note

What you built: compression-aware DNS name parser.
What comes next: building the response side — writing header and answer bytes back to the client.
Next node: M1E — write a DNS response header.
If returning after a break: run your unit tests with `python -m pytest tests/`. All previous tests should still pass.

---