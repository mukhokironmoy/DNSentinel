# DNS Exfiltration Detection — Roadmap Planning Document

> This file is the single source of truth for generating the interactive roadmap.
> Each node section contains everything needed to render that node's detail page.
> The agent generating the HTML and node markdown files should parse this document mechanically.
> Every node has an explicit ID, file path, dependency list, and full detail page content.

---

## HOW TO PARSE THIS DOCUMENT (Instructions for the generating agent)

1. Each node begins with a `## NODE:` heading followed by the node ID
2. Every node has a metadata block listing: ID, Title, File Path, Dependencies, Category, Week, Estimated Time
3. Everything after the metadata block and before the next `## NODE:` heading is the content of that node's detail page markdown file
4. The `File Path` field tells you exactly where to write that node's markdown file
5. The `Dependencies` field lists node IDs that must be shown as upstream in the graph. `none` means it is a root node.
6. Categories map to visual groupings on the roadmap graph
7. The roadmap graph should be rendered as an interactive SVG or canvas-based dependency graph in `index.html`
8. Clicking a node opens its markdown file rendered as HTML in a detail panel or page
9. All markdown files go inside a `nodes/` folder
10. `index.html` goes at the root level alongside the `nodes/` folder

---

## GRAPH METADATA

Total nodes: 30
Categories and their colours (suggestion):
- SETUP → grey
- PILLAR 1 — DNS SERVER → blue
- PILLAR 2 — DATA PIPELINE → green
- PILLAR 2 — ML PHASE 1 → orange
- PILLAR 2 — ML PHASE 2 → red
- PILLAR 2 — ML PHASE 3 → purple
- INTEGRATION → gold

---

## NODE: M0

**ID:** M0
**Title:** Repository Setup
**File Path:** `nodes/M0_repo_setup.md`
**Dependencies:** none
**Category:** SETUP
**Week:** 1
**Estimated Time:** 45 minutes

---

### What You Are Building

A clean GitHub repository with the correct folder structure, a meaningful README placeholder, and a `.gitignore` that keeps datasets and checkpoints out of version control. This is the foundation everything else builds on.

### How This Fits Into The Project

```
>>> [ M0 — Repo Setup ] <<<
          ↓
[ DNS Server ] + [ Data Pipeline ]
          ↓
[ ML Models ]
          ↓
[ Dashboard ]
```

Every file you write for the next 4 weeks lives inside the structure you create today. A clean repo from day one means no cleanup debt later and a professional commit history that reviewers can read like a project log.

### What You Need To Know

- What a `.gitignore` is and why datasets should not be committed
- Basic git commands: `init`, `add`, `commit`, `push`
- What a `requirements.txt` is (you will not fill it yet — just create it empty)
- Nothing about DNS, ML, or Python beyond this

### What To Study

Search exactly these if you need a refresher. Time cap: 10 minutes total.

- `git init new project github`
- `python gitignore template`

### Practice Exercise

Do this outside the project folder. Create a throwaway directory, run `git init` inside it, create three empty files, write a `.gitignore` that ignores one of them, commit the other two, and confirm the ignored file does not appear in `git status`. Delete the directory when done.

### Implementation — What To Build

Create a public GitHub repository named `dns-exfil-detector`. Then set up the following locally:

- Clone the repo and create the full folder structure as described in the project architecture. Every folder should exist, even if empty. Add a `.gitkeep` file inside each empty folder so git tracks them.
- Folders to create: `dns_server/`, `pipeline/`, `models/`, `dashboard/`, `attack_sim/`, `tests/`, `data/`, `demo/`, `demo/screenshots/`, `demo/shap_plots/`
- Create a `README.md` at the root with: project title, one paragraph describing what the project does, a placeholder line for the demo video link, a placeholder for the results table, and a tech stack list
- Create a `.gitignore` that ignores: `data/`, `__pycache__/`, `.ipynb_checkpoints/`, `*.pyc`, `.env`, `*.db`
- Create an empty `requirements.txt`
- Create a `data/download.sh` placeholder file with a comment explaining datasets go here

### Checklist

- [ ] Repository exists on GitHub and is public
- [ ] All folders from the architecture exist locally and are visible on GitHub
- [ ] `.gitignore` correctly ignores `data/` and Python cache files
- [ ] `README.md` exists with title and placeholder sections
- [ ] First commit pushed with message: `M-0: Initial repository setup, folder structure, and README`

### Test Cases

**Test 1 — Folder structure check**
Run `find . -type d` from the repo root. Every folder listed in the architecture should appear in the output.

**Test 2 — Gitignore check**
Create a file called `test.db` in the root. Run `git status`. It should NOT appear in untracked files. Delete the file after confirming.

**Test 3 — Remote check**
Run `git log --oneline`. You should see exactly one commit. Run `git remote -v`. You should see your GitHub repo URL.

### Re-entry Note

What you built: folder skeleton and repo. Nothing runs yet.
Next node: M1A — open a UDP socket.
If returning after a break: just run `git log --oneline` to confirm where you are, then open the next node.

---

## NODE: M1A

**ID:** M1A
**Title:** Open a UDP Socket and Receive Raw Bytes
**File Path:** `nodes/M1A_udp_socket.md`
**Dependencies:** M0
**Category:** PILLAR 1 — DNS SERVER
**Week:** 1
**Estimated Time:** 60 minutes

---

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

## NODE: M1B

**ID:** M1B
**Title:** Parse the DNS Header Section
**File Path:** `nodes/M1B_parse_header.md`
**Dependencies:** M1A
**Category:** PILLAR 1 — DNS SERVER
**Week:** 1
**Estimated Time:** 75 minutes

---

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

## NODE: M1C

**ID:** M1C
**Title:** Parse the Question Section (Domain Name Labels)
**File Path:** `nodes/M1C_parse_question.md`
**Dependencies:** M1B
**Category:** PILLAR 1 — DNS SERVER
**Week:** 1
**Estimated Time:** 90 minutes

---

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

## NODE: M1D

**ID:** M1D
**Title:** Handle DNS Name Compression
**File Path:** `nodes/M1D_compression.md`
**Dependencies:** M1C
**Category:** PILLAR 1 — DNS SERVER
**Week:** 1
**Estimated Time:** 75 minutes

---

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

## NODE: M1E

**ID:** M1E
**Title:** Write the DNS Response Header
**File Path:** `nodes/M1E_write_header.md`
**Dependencies:** M1D
**Category:** PILLAR 1 — DNS SERVER
**Week:** 1
**Estimated Time:** 60 minutes

---

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

## NODE: M1F

**ID:** M1F
**Title:** Write the Question Section
**File Path:** `nodes/M1F_write_question.md`
**Dependencies:** M1E
**Category:** PILLAR 1 — DNS SERVER
**Week:** 1
**Estimated Time:** 60 minutes

---

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

## NODE: M1G

**ID:** M1G
**Title:** Write the Answer Section
**File Path:** `nodes/M1G_write_answer.md`
**Dependencies:** M1F
**Category:** PILLAR 1 — DNS SERVER
**Week:** 1
**Estimated Time:** 75 minutes

---

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

## NODE: M2A

**ID:** M2A
**Title:** Forwarding Server (Upstream Resolver)
**File Path:** `nodes/M2A_forwarder.md`
**Dependencies:** M1G
**Category:** PILLAR 1 — DNS SERVER
**Week:** 1
**Estimated Time:** 75 minutes

---

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

## NODE: M2B

**ID:** M2B
**Title:** SQLite Query Logger
**File Path:** `nodes/M2B_logger.md`
**Dependencies:** M2A
**Category:** PILLAR 1 — DNS SERVER
**Week:** 1
**Estimated Time:** 60 minutes

---

### What You Are Building

A module that, on every query received by the server, writes a structured row to a SQLite database. This database is the bridge between Pillar 1 (DNS server) and Pillar 2 (ML pipeline). The feature extraction and live scorer read from this database.

### How This Fits Into The Project

```
[ M2A — Forwarder ] → every query passes through here
>>> [ M2B — SQLite Logger ] <<<
        ↓  rows written to dns_queries.db
[ M3 — Feature Extraction reads this database ]
[ M4A — Live Scorer polls this database ]
[ M8 — Dashboard queries this database ]
```

The SQLite database is the single connection point between the two pillars. Without it, the ML pipeline has no live data. Every query your server handles — normal or tunneled — gets a row here.

### What You Need To Know

- Python's built-in `sqlite3` module handles everything — no external library needed
- `sqlite3.connect("path/to/file.db")` creates the database if it does not exist
- Use `cursor.execute()` for SQL statements and `connection.commit()` after inserts
- The database file should be at `data/dns_queries.db` — this path is gitignored already from M0
- Use `datetime.utcnow().isoformat()` for timestamps

### What To Study

Search exactly these. Time cap: 10 minutes.

- `python sqlite3 insert row example`
- `python sqlite3 create table if not exists`

### Practice Exercise

Outside the project folder, write a script that creates a SQLite database with one table called `test`, inserts 3 rows with a timestamp and a string value, then queries all rows and prints them. Confirm you can see the 3 rows. Delete when done.

### Implementation — What To Build

Create `dns_server/logger.py`:

Write a module with:

- An initialisation function that connects to `data/dns_queries.db` and creates the queries table if it does not exist. The table should have columns: `id` (autoincrement primary key), `timestamp` (text), `src_ip` (text), `src_port` (integer), `query_name` (text), `record_type` (text), `response_code` (text, default 'NOERROR')
- A log function that accepts the source address tuple, query name string, and record type integer, and inserts one row with the current UTC timestamp
- The connection should be reused across calls (module-level), not opened and closed per query

Integrate into `server.py`: after parsing each incoming query (and before or after forwarding), call the log function. Every query that hits your server should produce a row in the database.

### Checklist

- [ ] The database file is created automatically on first run at `data/dns_queries.db`
- [ ] Every incoming query produces exactly one new row in the database
- [ ] Rows contain correct timestamp, source IP, query name, and record type
- [ ] Running multiple queries accumulates multiple rows — old rows are not overwritten
- [ ] The logger does not crash the server if the database write fails (wrap in try/except)

### Test Cases

**Test 1 — Row count**
Start the server fresh (delete the .db file first). Fire 5 dig queries for different domains. Open the database with `sqlite3 data/dns_queries.db` and run `SELECT COUNT(*) FROM queries;`. Expect 5.

**Test 2 — Row contents**
Run `SELECT * FROM queries LIMIT 3;` in the sqlite3 shell. Confirm each row has a timestamp, the correct source IP (127.0.0.1), and a recognisable domain name.

**Test 3 — Persistence**
Stop the server. Restart it. Fire 3 more queries. Run `SELECT COUNT(*) FROM queries;`. Expect 8 (5 from before + 3 new). Old rows must persist across restarts.

Run `python -m pytest tests/` and confirm all previous tests still pass.

Pillar 1 is now complete. Screenshot the sqlite3 shell showing rows and save to `demo/screenshots/M2B_logger.png`.

### Re-entry Note

What you built: the full DNS server — listener, parser, forwarder, and logger. Pillar 1 is done.
What comes next: Pillar 2 begins. You shift from protocol engineering to data and ML.
Next node: M3A — download the dataset and explore it with pandas.
If returning after a break: run the server, fire a few dig queries, check the database for new rows.

---

## NODE: M3A

**ID:** M3A
**Title:** Dataset Download and Exploratory Data Analysis
**File Path:** `nodes/M3A_dataset_eda.md`
**Dependencies:** M2B
**Category:** PILLAR 2 — DATA PIPELINE
**Week:** 2
**Estimated Time:** 75 minutes

---

### What You Are Building

A Jupyter notebook that loads the CIRA-CIC-DoHBrute dataset, inspects its structure, checks class distribution, and produces 2-3 exploratory plots that show why the features you will engineer in M3B-M3C are useful. This is your ground truth data — the labelled DNS traffic you will train models on.

### How This Fits Into The Project

```
[ Pillar 1 — DNS Server — COMPLETE ]

>>> [ M3A — Dataset EDA ] <<<
        ↓  understood data structure and class balance
[ M3B — Shannon Entropy Feature ]
[ M3C — Remaining Features ]
        ↓
[ M3D — Time Window Features ]
        ↓
[ M3E — Preprocessing + Train/Test Split ]
        ↓
[ M5 / M6 / M7 — ML Models ]
```

You cannot engineer features without knowing what the raw data looks like. EDA tells you the column names, the label distribution, whether there is class imbalance to handle, and which features visually separate classes before any model is trained.

### What You Need To Know

- The CIRA-CIC-DoHBrute dataset contains labelled DNS/DoH traffic with a `label` column
- `df.head()`, `df.info()`, `df.describe()`, `df['label'].value_counts()` are your EDA tools
- Class imbalance (many more normal than tunneled samples) is common — check if it exists
- A histogram of query lengths split by label class is the single most informative plot at this stage

### What To Study

Search exactly these. Time cap: 10 minutes.

- `CIRA CIC DoHBrute dataset download`
- `pandas read_csv value_counts describe`

### Practice Exercise

None needed — EDA is inherently exploratory. Just start the notebook and follow the checklist below.

### Implementation — What To Build

Create a notebook at `models/phase1_classical.ipynb` (you will add models here in M5):

Start a new section at the top of the notebook titled "Dataset EDA":

- Download the dataset from `https://www.unb.ca/cic/datasets/` — look for the DoH traffic dataset. If unavailable, use UNSW-NB15 as the alternate.
- Load the CSV into a pandas DataFrame
- Print: number of rows, number of columns, column names, data types
- Print: class distribution using `value_counts()` and the percentage split
- Plot: histogram of a length-related column split by label — normal vs tunneled should look visually different
- Plot: boxplot or violin plot of entropy (if the dataset has it) or subdomain length, split by label
- Write 3-5 sentences of observations as a markdown cell: what did you notice? Is there class imbalance? Do the classes visually separate on length?

### Checklist

- [ ] Dataset is downloaded and loaded without errors
- [ ] Class distribution is printed and understood
- [ ] At least 2 plots are produced showing feature distributions split by label
- [ ] A markdown cell records your observations about class separation
- [ ] You know the exact column name for the domain/query string and the label

### Test Cases

**Test 1 — Load check**
`df.shape` should return a tuple where the row count is in the thousands or more. If it is under 100 rows, the dataset did not load correctly.

**Test 2 — Label check**
`df['label'].nunique()` should return 2 (binary classification). Print the unique label values and confirm one represents normal traffic and one represents tunneled/malicious.

**Test 3 — Visual separation**
Plot subdomain/query length distributions for both classes on the same histogram. If the tunneled class histogram peak is clearly shifted right (longer lengths), your feature engineering direction is confirmed. If they completely overlap, you may have loaded the wrong column — re-examine.

### Re-entry Note

What you built: EDA notebook with confirmed data understanding.
Next node: M3B — implement Shannon entropy as a feature.
If returning after a break: re-run the notebook top to bottom. It should complete without errors.

---

## NODE: M3B

**ID:** M3B
**Title:** Implement Shannon Entropy Feature
**File Path:** `nodes/M3B_entropy_feature.md`
**Dependencies:** M3A
**Category:** PILLAR 2 — DATA PIPELINE
**Week:** 2
**Estimated Time:** 60 minutes

---

### What You Are Building

A Python function that computes the Shannon entropy of a string. This is the single most important feature for DNS tunneling detection — Base64-encoded subdomains have high entropy, normal words have low entropy. You implement this from scratch using `collections.Counter`, not a library.

### How This Fits Into The Project

```
[ M3A — EDA confirms entropy separates classes ]
>>> [ M3B — Shannon Entropy Function ] <<<
        ↓  used in M3C alongside other features
[ M3E — Feature matrix ]
        ↓
[ All ML models use entropy as a key input feature ]
[ SHAP plots will likely show entropy as top feature ]
```

Entropy is the information-theoretic measure of randomness in a string. A word like `google` has low entropy (predictable character distribution). A Base64 string like `SGVsbG8gV29ybGQ=` has high entropy (near-uniform character distribution). This is the mathematical foundation that connects this project to cryptanalysis.

### What You Need To Know

- Shannon entropy formula: `H = -sum(p_i * log2(p_i))` for each unique character `i`
- `p_i` is the frequency of character `i` divided by the total string length
- `collections.Counter(string)` gives you character frequencies
- `math.log2(p)` computes log base 2
- Entropy of a random string approaches `log2(alphabet_size)` — for Base64 (64 chars) that is 6 bits/char
- Normal domain labels have entropy around 3-4. Tunneled subdomains typically exceed 5.

### What To Study

Search exactly these. Time cap: 10 minutes.

- `Shannon entropy formula string Python`
- `collections Counter Python frequency`

Do NOT use `scipy.stats.entropy` — implement it yourself. This is one of the resume-relevant parts of the project.

### Practice Exercise

Outside the project folder, implement `shannon_entropy(s)` and test it against known values: `shannon_entropy("aaaa")` should return 0.0 (no randomness). `shannon_entropy("abcd")` should return 2.0 (4 equally likely characters). `shannon_entropy("aab")` should be between 0 and 2. Delete when done.

### Implementation — What To Build

Create `pipeline/features.py`:

Write `shannon_entropy(s: str) -> float` that:

- Handles empty string input (return 0.0)
- Uses `collections.Counter` to get character frequencies
- Computes probabilities by dividing each count by total length
- Computes entropy using the Shannon formula with log base 2
- Returns the entropy as a float

Apply this function to the dataset from M3A: add an `entropy` column to your DataFrame by applying `shannon_entropy` to the subdomain portion of each query name. Then plot: histogram of entropy values split by label class. This plot should show clear separation.

### Checklist

- [ ] `shannon_entropy("aaaa")` returns 0.0
- [ ] `shannon_entropy("abcd")` returns 2.0
- [ ] Function handles empty string without crashing
- [ ] Applied to the dataset, the entropy column shows higher values for tunneled class
- [ ] A histogram of entropy by class is plotted and shows separation

### Test Cases

**Test 1 — Known values**
In `tests/test_features.py`, assert `shannon_entropy("aaaa") == 0.0`, `round(shannon_entropy("abcd"), 5) == 2.0`, `shannon_entropy("") == 0.0`.

**Test 2 — Realistic values**
Assert `shannon_entropy("google") < 3.0`. Assert `shannon_entropy("SGVsbG8gV29ybGQ") > 4.5`. These are the real-world ranges you expect.

**Test 3 — Dataset distribution**
After applying to the dataset, check that `df[df['label'] == 'tunneled']['entropy'].mean() > df[df['label'] == 'normal']['entropy'].mean()`. The tunneled class should have higher average entropy.

### Re-entry Note

What you built: Shannon entropy feature implemented from scratch.
Next node: M3C — implement remaining features (length, digit ratio, label count, etc.).
If returning after a break: run `python -m pytest tests/` to confirm entropy tests pass.

---

## NODE: M3C

**ID:** M3C
**Title:** Implement Remaining Feature Functions
**File Path:** `nodes/M3C_remaining_features.md`
**Dependencies:** M3B
**Category:** PILLAR 2 — DATA PIPELINE
**Week:** 2
**Estimated Time:** 75 minutes

---

### What You Are Building

Five additional feature extraction functions in `pipeline/features.py`, each taking a domain name string and returning a numeric value. Together with entropy from M3B, these form the complete feature set for all ML models.

### How This Fits Into The Project

```
[ M3B — Entropy feature ]
>>> [ M3C — Length, ratio, and count features ] <<<
        ↓  complete feature set (6 features total)
[ M3D — Time window aggregation adds 2 more ]
        ↓
[ M3E — Feature matrix ready for models ]
```

A single feature (entropy) is not enough for a robust detector. Tunneling tools can be configured to lower entropy by mixing in readable characters. Multiple independent features make the detector harder to evade and give SHAP something interesting to explain.

### What You Need To Know

For each function, the logic is simple arithmetic on the string. No new libraries needed beyond what you already have.

- **subdomain_length**: length of the first label (before the first dot). Tunneled subdomains are long.
- **digit_ratio**: count of digit characters divided by total string length. Encoded payloads often have more digits than normal words.
- **consonant_vowel_ratio**: count of consonants divided by count of vowels. Real words are pronounceable (balanced). Encoded strings are not.
- **label_count**: number of dot-separated segments in the full domain. Tunneling tools sometimes use many nested subdomains.
- **max_label_length**: length of the longest individual label. Similar signal to subdomain_length but catches cases where the payload is not in the first label.

### What To Study

No new searches needed. These are pure string operations.

### Practice Exercise

None — just implement each function one at a time and verify against obvious test cases before moving to the next.

### Implementation — What To Build

Add to `pipeline/features.py`:

Write each of these five functions with the described logic. Then write a single `extract_features(query_name: str) -> dict` function that calls all six feature functions (including entropy from M3B) and returns a dictionary mapping feature names to their values. This is the function the live scorer (M4A) and dataset pipeline (M3E) will call.

Apply `extract_features` to every row in your dataset DataFrame. The result should be a new DataFrame with 6 numeric columns and the original label column.

### Checklist

- [ ] All five functions are implemented and return numeric values
- [ ] `extract_features` calls all six feature functions and returns a dictionary
- [ ] Applied to the dataset, all 6 feature columns are populated with no NaN values
- [ ] `digit_ratio` for a purely alphabetic string returns 0.0
- [ ] `consonant_vowel_ratio` for a string with no vowels does not divide by zero

### Test Cases

**Test 1 — Unit tests for each function**
In `tests/test_features.py`:
- `subdomain_length("SGVsbG8.evil.com") == 7`
- `digit_ratio("abc123") == 0.5`
- `label_count("a.b.c.com") == 4`
- `max_label_length("short.averylonglabel.com") == 15`
- `consonant_vowel_ratio("aeiou") == 0.0` (no consonants)

**Test 2 — No NaN in feature matrix**
After applying to the full dataset: `assert df[feature_cols].isna().sum().sum() == 0`

**Test 3 — Feature ranges make sense**
All `digit_ratio` values should be between 0.0 and 1.0. All `subdomain_length` values should be positive integers. Assert these ranges hold across the full dataset.

### Re-entry Note

What you built: complete per-query feature extraction pipeline.
Next node: M3D — time window aggregation features (queries per second, unique subdomains per window).
If returning after a break: run `python -m pytest tests/` — all feature tests should pass.

---

## NODE: M3D

**ID:** M3D
**Title:** Time Window Aggregation Features
**File Path:** `nodes/M3D_time_windows.md`
**Dependencies:** M3C
**Category:** PILLAR 2 — DATA PIPELINE
**Week:** 2
**Estimated Time:** 75 minutes

---

### What You Are Building

A function that groups DNS queries by source IP and parent domain over 60-second sliding windows, and computes two behavioural features: queries per second and unique subdomains per window. These are features that only make sense aggregated over time — they cannot be computed from a single query.

### How This Fits Into The Project

```
[ M3C — Per-query features ]
>>> [ M3D — Time window features ] <<<
        ↓  8 features total per query (6 per-query + 2 windowed)
[ M3E — Final feature matrix ]
```

A single query with high entropy might be a false positive. But 50 high-entropy queries to the same parent domain in 60 seconds from the same IP is almost certainly tunneling. Time-window features capture the behavioural pattern, not just the per-query statistics. This is how real network monitoring works.

### What You Need To Know

- Group queries by `(src_ip, parent_domain)` — the parent domain is everything after the first dot
- Within each group, sort by timestamp and create 60-second rolling windows
- For each query, compute how many queries occurred in the 60 seconds before it from the same (IP, domain) pair
- Count unique subdomains seen in that window from the same (IP, domain) pair
- pandas `groupby` and `rolling` with time-based windows handle this, but you may need to set the timestamp column as a DatetimeIndex first

### What To Study

Search exactly these. Time cap: 15 minutes.

- `pandas rolling window time-based groupby`
- `pandas groupby rolling count unique`

### Practice Exercise

Outside the project folder, create a small DataFrame with 10 rows: timestamps 10 seconds apart, alternating between two domain names. Write a rolling count that, for each row, counts how many rows in the previous 60 seconds share the same domain. Verify the counts manually. Delete when done.

### Implementation — What To Build

Add to `pipeline/features.py`:

Write a function that:

- Accepts a DataFrame with columns: `timestamp` (parseable datetime string), `src_ip`, `query_name`
- Derives `parent_domain` by taking everything after the first dot in `query_name`
- Converts timestamp to a proper datetime column
- Groups by `(src_ip, parent_domain)`
- For each group, computes a 60-second rolling count of queries (`queries_per_60s`)
- For each group, computes a 60-second rolling count of unique subdomains (`unique_subdomains_60s`)
- Joins these two new columns back to the original DataFrame
- Returns the DataFrame with these two additional columns added

### Checklist

- [ ] `queries_per_60s` column is added with correct rolling counts
- [ ] `unique_subdomains_60s` column is added with correct unique subdomain counts
- [ ] Queries from different (IP, domain) pairs do not bleed into each other's windows
- [ ] The function handles a DataFrame with a single row without crashing
- [ ] Timestamps are correctly parsed before rolling is applied

### Test Cases

**Test 1 — Rolling count correctness**
Build a test DataFrame: 10 queries all from the same IP and domain, 5 seconds apart (spanning 45 seconds total). All 10 should have a `queries_per_60s` value of at least 1 and at most 10. The last query should see all previous 9 within its 60-second window.

**Test 2 — Cross-domain isolation**
Add 10 more rows with a different domain. Confirm that rows from domain A do not contribute to the window counts of domain B.

**Test 3 — High value for tunneling**
Apply to your dataset rows that are labelled as tunneled. Tunneled rows should show significantly higher `queries_per_60s` and `unique_subdomains_60s` than normal rows on average.

### Re-entry Note

What you built: time-based behavioural features that capture tunneling patterns over time.
Next node: M3E — preprocessing, scaling, and train/test split.
If returning after a break: run the time window function on a small test DataFrame and verify the counts manually.

---

## NODE: M3E

**ID:** M3E
**Title:** Preprocessing, Scaling, and Train/Test Split
**File Path:** `nodes/M3E_preprocessing.md`
**Dependencies:** M3D
**Category:** PILLAR 2 — DATA PIPELINE
**Week:** 2
**Estimated Time:** 60 minutes

---

### What You Are Building

A preprocessing script that takes the fully-featured DataFrame (8 features per row), applies StandardScaler, performs a stratified 80/20 train/test split, and saves the processed feature matrix to `data/features.csv`. This is the final data preparation step before any model training.

### How This Fits Into The Project

```
[ M3D — All 8 features computed ]
>>> [ M3E — Scale + Split + Save ] <<<
        ↓  X_train, X_test, y_train, y_test saved to data/
[ M5 — Random Forest loads this ]
[ M6 — Autoencoder loads this ]
[ M7 — CNN/LSTM loads this ]
```

Every model in the project reads from the same preprocessed data. StandardScaler prevents features with large ranges (like subdomain_length) from dominating features with small ranges (like digit_ratio). Stratified splitting ensures both train and test sets have the same class balance.

### What You Need To Know

- `StandardScaler` fits on training data only — never on test data. `scaler.fit(X_train)`, then `scaler.transform(X_train)` and `scaler.transform(X_test)` separately.
- Stratified split: `train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)`
- Save the scaler using `joblib.dump(scaler, 'data/scaler.pkl')` — models will need it to scale live queries
- Save splits as CSVs: `X_train.to_csv('data/X_train.csv', index=False)` etc.
- Check class balance in both splits after splitting

### What To Study

Search exactly these. Time cap: 10 minutes.

- `sklearn StandardScaler fit transform train test`
- `sklearn train_test_split stratify`

### Practice Exercise

None needed — follow the checklist below.

### Implementation — What To Build

Add to `pipeline/dataset.py`:

Write a preprocessing function that:

- Loads the feature DataFrame (from M3C/M3D results)
- Separates features (X) from labels (y)
- Applies `train_test_split` with `stratify=y` and `random_state=42`
- Fits `StandardScaler` on `X_train` only
- Transforms both `X_train` and `X_test`
- Saves `X_train`, `X_test`, `y_train`, `y_test` as separate CSV files in `data/`
- Saves the fitted scaler to `data/scaler.pkl` using joblib
- Prints class distribution in both train and test splits to confirm stratification worked

### Checklist

- [ ] Four CSV files exist in `data/` after running: X_train, X_test, y_train, y_test
- [ ] `scaler.pkl` exists in `data/`
- [ ] Class distribution percentages in train and test match (approximately) — stratification worked
- [ ] Scaler was fit only on X_train, not on X_test
- [ ] No NaN values in any of the saved files

### Test Cases

**Test 1 — Shape check**
Load the saved CSVs. Assert `len(X_train) + len(X_test) == total_rows` and `len(X_train) / total_rows ≈ 0.8`.

**Test 2 — Stratification check**
Compute `y_train.value_counts(normalize=True)` and `y_test.value_counts(normalize=True)`. The class proportions should match within 1-2%.

**Test 3 — Scaler round-trip**
Load `scaler.pkl`. Apply `scaler.transform(X_test)` again (it was already scaled — this is a sanity check). The values should not change significantly (they are already in the scaled space). Alternatively, verify that `X_train.mean(axis=0)` is approximately 0.0 for all features (StandardScaler centres the data).

### Re-entry Note

What you built: the complete data pipeline. Feature matrix is ready for all three model phases.
What comes next: two parallel tracks. M4A/M4B (live scorer and attack sim) can be done now, or you can jump straight to M5 (Random Forest).
Next node: M4A — live scorer, OR M5A — Random Forest (your choice based on energy).
If returning after a break: load the CSVs and check shapes.

---

## NODE: M4A

**ID:** M4A
**Title:** Live Feature Scorer
**File Path:** `nodes/M4A_live_scorer.md`
**Dependencies:** M2B, M3C
**Category:** PILLAR 2 — DATA PIPELINE
**Week:** 2
**Estimated Time:** 75 minutes

---

### What You Are Building

A script that polls the SQLite database every 5 seconds, picks up new query rows that have not yet been scored, runs them through the feature extraction pipeline from M3C, and writes the scored rows to a results table. This is the bridge between the running DNS server and the ML models.

### How This Fits Into The Project

```
[ M2B — SQLite Logger ] → new rows appear as queries arrive
>>> [ M4A — Live Scorer ] <<<
        ↓  scored rows with 8 features per query
[ Dashboard — reads scored rows for live feed ]
[ Models — can score live queries in near-real-time ]
```

The dataset from M3A is historical. The live scorer connects the trained models to real DNS traffic passing through your server. When you run the attack simulator in M4B, the scorer will pick those queries up and produce features — making the tunneling queries visible to the models.

### What You Need To Know

- Use a `processed` flag column in the database to track which rows have been scored
- `time.sleep(5)` in a loop creates the polling behaviour
- Load the saved scaler from M3E using joblib to scale live features
- The scorer does not run model predictions yet — it just produces the feature vector. Model scoring comes later.
- `ALTER TABLE queries ADD COLUMN processed INTEGER DEFAULT 0` adds the flag if not already present

### What To Study

Search exactly these. Time cap: 10 minutes.

- `python sqlite3 poll new rows`
- `python time sleep loop`

### Practice Exercise

Outside the project folder, write a script that opens a SQLite database, inserts a row every 2 seconds in one thread, and in the main thread polls every 3 seconds for unprocessed rows and prints them. Confirm new rows are picked up. Delete when done.

### Implementation — What To Build

Create `pipeline/scorer.py`:

Write a script that:

- Connects to `data/dns_queries.db`
- Adds a `processed` integer column (default 0) to the queries table if it does not exist
- Enters a loop that runs every 5 seconds
- On each iteration, selects all rows where `processed = 0`
- For each unprocessed row, extracts features using `extract_features` from M3C
- Scales the features using the loaded scaler from M3E
- Prints the query name and its feature vector
- Marks the row as `processed = 1` in the database
- Sleeps 5 seconds and repeats

### Checklist

- [ ] Scorer runs continuously without crashing
- [ ] New rows added to the database while scorer is running are picked up within 10 seconds
- [ ] Each query is scored exactly once — processed rows are not re-scored
- [ ] Feature values printed look reasonable (entropy between 0-6, length positive, ratios between 0-1)
- [ ] Scorer handles an empty database gracefully (no unprocessed rows = loop sleeps and waits)

### Test Cases

**Test 1 — Pickup delay**
Start the DNS server and the scorer simultaneously. Fire a dig query. Within 10 seconds, the scorer terminal should print the feature vector for that query.

**Test 2 — No double processing**
Fire one dig query. Wait 30 seconds. Confirm the scorer terminal shows the query printed exactly once, not twice.

**Test 3 — Feature value sanity**
Fire `dig @127.0.0.1 -p 5353 google.com`. The scorer should print an entropy value below 4.0 (normal domain) and a subdomain length below 10. Fire your tunnel simulator (from M4B) and compare — tunneled queries should show entropy above 5.0.

### Re-entry Note

What you built: the live data pipeline connecting the DNS server to feature extraction.
Next node: M4B — write the tunnel simulator script.
If returning after a break: start the server and scorer, fire a dig query, confirm the scorer prints features.

---

## NODE: M4B

**ID:** M4B
**Title:** Synthetic Tunneling Attack Simulator
**File Path:** `nodes/M4B_tunnel_sim.md`
**Dependencies:** M4A
**Category:** PILLAR 2 — DATA PIPELINE
**Week:** 2
**Estimated Time:** 60 minutes

---

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

## NODE: M5A

**ID:** M5A
**Title:** Random Forest Classifier
**File Path:** `nodes/M5A_random_forest.md`
**Dependencies:** M3E
**Category:** PILLAR 2 — ML PHASE 1
**Week:** 2
**Estimated Time:** 90 minutes

---

### What You Are Building

A trained Random Forest classifier that takes the 8-feature vector from M3E and classifies each DNS query as normal or tunneled. You train it, evaluate it with precision/recall/F1 and a confusion matrix, and save the trained model to disk.

### How This Fits Into The Project

```
[ M3E — X_train, X_test, y_train, y_test ]
>>> [ M5A — Random Forest ] <<<
        ↓  trained model saved
[ M5B — Isolation Forest (comparison) ]
[ M5C — SHAP explainability uses this model ]
[ M8 — Dashboard loads this model for Query Inspector ]
```

Random Forest is your supervised baseline. It requires labelled data and learns explicit decision boundaries. Every other model will be compared against it. This is also the model SHAP will explain — making it the most interpretable part of your ML pipeline.

### What You Need To Know

- `RandomForestClassifier(n_estimators=200, random_state=42)` is a solid starting configuration
- `clf.fit(X_train, y_train)` trains. `clf.predict(X_test)` predicts.
- `classification_report(y_test, y_pred)` gives precision, recall, F1 per class
- For tunneling detection, recall on the tunneled class matters more than precision — missing an attack is worse than a false alarm
- A confusion matrix heatmap using seaborn shows true positive, false positive, true negative, false negative visually
- Save the model with `joblib.dump(clf, 'data/rf_model.pkl')`

### What To Study

Search exactly these. Time cap: 10 minutes.

- `sklearn RandomForestClassifier classification report`
- `sklearn confusion matrix seaborn heatmap`

### Practice Exercise

None — go directly to the notebook. The concepts are standard supervised ML.

### Implementation — What To Build

In `models/phase1_classical.ipynb`, add a new section titled "Phase 1A — Random Forest":

- Load X_train, X_test, y_train, y_test from the saved CSVs
- Train a Random Forest with at least 200 trees
- Predict on X_test
- Print the full classification report
- Plot a confusion matrix as a seaborn heatmap — label axes clearly (Normal / Tunneled)
- Plot the ROC curve and compute ROC-AUC score
- Save the trained model to `data/rf_model.pkl`
- Write 3-5 sentences in a markdown cell: what is your F1 on the tunneled class? Where does the model make mistakes? Is precision or recall higher for tunneled queries?

### Checklist

- [ ] Model trains without errors
- [ ] Classification report is printed with per-class precision, recall, F1
- [ ] Confusion matrix heatmap is saved to `demo/screenshots/M5A_confusion_matrix.png`
- [ ] ROC-AUC score is computed and printed
- [ ] Model is saved to `data/rf_model.pkl`
- [ ] F1 score on tunneled class is above 0.80 (if below, check for data issues)

### Test Cases

**Test 1 — Model loads**
After saving, run: `import joblib; clf = joblib.load('data/rf_model.pkl'); clf.predict(X_test[:5])`. Should return an array of 0s and 1s without errors.

**Test 2 — Prediction sanity**
Pass the feature vector for a known tunneled query (high entropy, long subdomain) through the model. It should predict 1 (tunneled). Pass a feature vector for `google.com` (low entropy, short subdomain). It should predict 0 (normal).

**Test 3 — Feature importance**
`clf.feature_importances_` returns an array of importance scores, one per feature. Print them. Entropy and subdomain_length should be among the top 3 most important features. If they are not, revisit feature engineering.

### Re-entry Note

What you built: trained Random Forest classifier with evaluation metrics.
Next node: M5B — Isolation Forest (unsupervised comparison).
If returning after a break: reload the notebook and re-run from the Random Forest section. The model file still exists in data/.

---

## NODE: M5B

**ID:** M5B
**Title:** Isolation Forest (Unsupervised Anomaly Detection)
**File Path:** `nodes/M5B_isolation_forest.md`
**Dependencies:** M5A
**Category:** PILLAR 2 — ML PHASE 1
**Week:** 3
**Estimated Time:** 75 minutes

---

### What You Are Building

A trained Isolation Forest model that detects anomalous DNS queries without using any labels during training. It learns what normal traffic looks like and flags deviations. You compare its performance directly against the Random Forest from M5A.

### How This Fits Into The Project

```
[ M5A — Random Forest (supervised) ]
>>> [ M5B — Isolation Forest (unsupervised) ] <<<
        ↓  anomaly scores + predictions
[ M5C — SHAP explains Random Forest ]
[ M7D — Model comparison table includes both ]
```

Isolation Forest represents how detection works when you have no labelled attack data — which is realistic for new attack variants. Training on normal traffic only and flagging statistical outliers is a production-realistic approach. Comparing it to the supervised model reveals the cost of not having labels.

### What You Need To Know

- `IsolationForest(contamination=0.05, random_state=42)` — contamination estimates the fraction of anomalies expected in the data (roughly)
- Train ONLY on normal traffic samples: `iso.fit(X_train[y_train == 0])`
- `iso.decision_function(X_test)` returns anomaly scores — more negative = more anomalous
- `iso.predict(X_test)` returns 1 (normal) or -1 (anomaly) — remap -1 to 1 and 1 to 0 for consistency with your label encoding
- Compare precision, recall, F1 against Random Forest in a markdown table

### What To Study

Search exactly these. Time cap: 10 minutes.

- `sklearn IsolationForest fit predict anomaly detection`
- `sklearn IsolationForest decision_function scores`

### Practice Exercise

None — follow the notebook pattern from M5A.

### Implementation — What To Build

In `models/phase1_classical.ipynb`, add a section titled "Phase 1B — Isolation Forest":

- Extract normal-only training samples: rows where label is 0
- Fit Isolation Forest on those samples only
- Run `predict` and `decision_function` on the full X_test
- Remap predictions from {1, -1} to {0, 1}
- Compute precision, recall, F1 on the tunneled class
- Plot the distribution of anomaly scores for normal vs tunneled queries (two overlaid histograms)
- Create a markdown comparison table: Random Forest vs Isolation Forest side by side with precision, recall, F1
- Write 3-5 sentences: where did Isolation Forest miss? Is the recall higher or lower than Random Forest? What does this tell you?

### Checklist

- [ ] Model is trained only on normal traffic
- [ ] Anomaly score distributions for both classes are plotted
- [ ] Predictions are remapped to consistent 0/1 encoding
- [ ] Comparison table with Random Forest exists in the notebook
- [ ] Written analysis explains the performance difference

### Test Cases

**Test 1 — Score distribution**
The mean anomaly score for tunneled queries should be more negative than for normal queries. Assert `scores[y_test == 1].mean() < scores[y_test == 0].mean()`.

**Test 2 — No label leakage**
Confirm you did not accidentally include any tunneled rows in training. `assert (y_train[iso_train_mask] == 0).all()` where iso_train_mask selects what you trained on.

**Test 3 — Comparison sanity**
Isolation Forest recall should be lower than Random Forest recall on the tunneled class (it has less information). If Isolation Forest outperforms Random Forest, something is wrong with one of the setups — investigate before continuing.

### Re-entry Note

What you built: unsupervised anomaly detector + comparison to supervised baseline.
Next node: M5C — SHAP explainability for the Random Forest.
If returning after a break: reload notebook, results are in the cells.

---

## NODE: M5C

**ID:** M5C
**Title:** SHAP Explainability
**File Path:** `nodes/M5C_shap.md`
**Dependencies:** M5B
**Category:** PILLAR 2 — ML PHASE 1
**Week:** 3
**Estimated Time:** 75 minutes

---

### What You Are Building

SHAP (SHapley Additive exPlanations) analysis on the Random Forest model. A global summary plot showing which features drive predictions across all queries, and individual force plots for 3 flagged queries showing exactly why each one was classified as tunneled.

### How This Fits Into The Project

```
[ M5A — Trained Random Forest ]
>>> [ M5C — SHAP Explainability ] <<<
        ↓  plots saved to demo/shap_plots/
[ M8 — Dashboard Query Inspector shows SHAP force plots ]
[ Demo video — "entropy of 5.8 triggered this alert" ]
```

Explainability is what separates a research toy from a usable security tool. A SOC analyst cannot act on "the model says this is bad." They need to know which features triggered the alert. SHAP provides this. It is also a strong resume signal — you understand not just that the model works but why.

### What You Need To Know

- `shap.TreeExplainer(clf)` creates an explainer for tree-based models
- `shap_values = explainer.shap_values(X_test)` — for binary classification this returns a list of two arrays (one per class). Use index [1] for the tunneled class.
- `shap.summary_plot` shows global feature importance across all test samples
- `shap.force_plot` shows why a specific prediction was made — which features pushed the score up or down
- Save plots as PNGs using `matplotlib.pyplot.savefig` for the summary plot. Force plots need special handling — use `shap.save_html` or matplotlib backend.

### What To Study

Search exactly these. Time cap: 15 minutes.

- `shap TreeExplainer summary_plot example`
- `shap force_plot save png matplotlib`

### Practice Exercise

None — follow the notebook pattern.

### Implementation — What To Build

In `models/phase1_classical.ipynb`, add a section titled "Phase 1C — SHAP Explainability":

- Create a SHAP TreeExplainer using your saved Random Forest
- Compute SHAP values for the full X_test set
- Generate and save a global summary plot to `demo/shap_plots/shap_summary.png`
- Find 3 test queries that were correctly classified as tunneled (true positives)
- Generate a force plot for each — showing which features pushed the prediction toward tunneled
- Save each force plot to `demo/shap_plots/shap_force_1.png` etc.
- Write a 200-word analysis markdown cell: which feature has the highest global SHAP importance? What do the force plots tell you about individual predictions? Is this consistent with your intuition about which features matter?

### Checklist

- [ ] SHAP summary plot is saved and entropy appears as a top feature
- [ ] Three force plots are saved, one per selected tunneled query
- [ ] Written analysis explains the SHAP findings in plain language
- [ ] Plots are saved to `demo/shap_plots/` with clear filenames

### Test Cases

**Test 1 — Top feature**
From the SHAP summary plot or `shap_values[1].mean(axis=0)`, identify the feature with highest mean absolute SHAP value. It should be either `entropy` or `subdomain_length`. If it is neither, review your feature engineering.

**Test 2 — Force plot direction**
For a correctly flagged tunneled query, the force plot should show entropy and subdomain_length as features pushing the prediction TOWARD tunneled (red arrows). If they push toward normal (blue arrows), the query may not be a true positive — select a different one.

**Test 3 — Plot files exist**
After running the cell, assert all expected files exist in `demo/shap_plots/`.

### Re-entry Note

What you built: SHAP explainability layer on top of Random Forest. Phase 1 ML is complete.
Next node: M6A — Autoencoder (Phase 2 ML).
If returning after a break: reload the notebook and re-run the SHAP section.

---

## NODE: M6A

**ID:** M6A
**Title:** Autoencoder — Architecture and Training
**File Path:** `nodes/M6A_autoencoder_train.md`
**Dependencies:** M3E
**Category:** PILLAR 2 — ML PHASE 2
**Week:** 3
**Estimated Time:** 90 minutes

---

### What You Are Building

A Keras autoencoder trained only on normal DNS traffic. The encoder compresses the 8-feature input to a 8-dimensional bottleneck. The decoder reconstructs the original input. After training, queries that reconstruct poorly (high reconstruction error) are flagged as anomalous.

### How This Fits Into The Project

```
[ M3E — Feature matrix ]
>>> [ M6A — Autoencoder training ] <<<
        ↓  trained encoder + decoder saved
[ M6B — Threshold tuning + anomaly scoring ]
        ↓
[ M7D — Model comparison table ]
```

The autoencoder has never seen tunneled traffic during training. It learns to reconstruct normal DNS patterns. When it tries to reconstruct a tunneled query, it fails — because the pattern is unfamiliar. The reconstruction error is the anomaly score. This is unsupervised deep learning for threat detection.

### What You Need To Know

- Encoder: Dense layers that progressively reduce dimensionality (input → 32 → 16 → 8)
- Decoder: Dense layers that progressively expand back (8 → 16 → 32 → input_dim)
- The full autoencoder chains encoder and decoder
- Loss function: Mean Squared Error (MSE) between input and reconstruction
- Train on normal traffic only: `X_train_normal = X_train[y_train == 0]`
- Use early stopping: stop training when validation loss stops improving
- `activation='relu'` for hidden layers, `activation='sigmoid'` for the output layer (features are scaled 0-1 after StandardScaler... actually verify this: sigmoid only if features are in [0,1] range. If StandardScaler output can be negative, use linear activation on output.)

### What To Study

Search exactly these. Time cap: 15 minutes.

- `keras autoencoder anomaly detection example`
- `keras EarlyStopping callback`

### Practice Exercise

Outside the project folder, build a tiny autoencoder with input dimension 4, bottleneck 2. Train it on 100 random rows of data. Plot training loss. Confirm loss decreases. Delete when done.

### Implementation — What To Build

Create `models/phase2_autoencoder.ipynb`:

- Load X_train, X_test, y_train, y_test from saved CSVs
- Extract normal-only training data
- Define encoder and decoder as separate Sequential models, then chain them
- Compile with Adam optimizer and MSE loss
- Train with EarlyStopping (patience=5, restore_best_weights=True) and 10% validation split
- Plot training and validation loss curves — save to `demo/screenshots/M6A_loss_curves.png`
- Save the trained autoencoder to `data/autoencoder_model/` using `model.save()`

### Checklist

- [ ] Autoencoder trains without errors
- [ ] Training loss decreases over epochs (loss curve goes down)
- [ ] Validation loss does not diverge significantly from training loss (no severe overfitting)
- [ ] Model is saved to disk
- [ ] Loss curve plot is saved

### Test Cases

**Test 1 — Loss decrease**
After training, assert `history.history['loss'][-1] < history.history['loss'][0]`. Loss must have decreased.

**Test 2 — Reconstruction check**
Pass one normal query through the autoencoder. Compute MSE between input and output. Pass one tunneled query. The tunneled query's MSE should be higher. This is the core assumption of the model.

**Test 3 — Model loads**
After saving: `from tensorflow import keras; ae = keras.models.load_model('data/autoencoder_model/')`. Should load without errors.

### Re-entry Note

What you built: trained autoencoder on normal traffic.
Next node: M6B — threshold tuning and anomaly scoring.
If returning after a break: reload model from disk, run one reconstruction check.

---

## NODE: M6B

**ID:** M6B
**Title:** Autoencoder — Threshold Tuning and Evaluation
**File Path:** `nodes/M6B_autoencoder_threshold.md`
**Dependencies:** M6A
**Category:** PILLAR 2 — ML PHASE 2
**Week:** 3
**Estimated Time:** 60 minutes

---

### What You Are Building

The anomaly scoring and threshold selection for the autoencoder. You compute reconstruction errors for all test queries, choose a threshold (95th percentile of normal traffic errors), convert to binary predictions, and evaluate precision/recall/F1. You also produce the reconstruction error histogram that belongs in the README.

### How This Fits Into The Project

```
[ M6A — Trained autoencoder ]
>>> [ M6B — Threshold tuning + evaluation ] <<<
        ↓  precision/recall/F1 added to comparison table
[ M7D — Final model comparison ]
```

The autoencoder outputs a continuous reconstruction error, not a binary prediction. Choosing where to draw the line between normal and anomalous is a business decision — a lower threshold catches more attacks but causes more false alarms. The 95th percentile of normal errors is a principled starting point.

### What You Need To Know

- Reconstruction error per sample: `MSE = mean((input - reconstruction)^2)` across all features
- Threshold: `np.percentile(errors[y_test == 0], 95)` — 95% of normal traffic errors fall below this
- Predictions: `predictions = (errors > threshold).astype(int)`
- Then compute precision, recall, F1 using sklearn metrics on these binary predictions

### What To Study

No new searches — this is numpy and sklearn metrics from M5A applied to a different score.

### Implementation — What To Build

In `models/phase2_autoencoder.ipynb`, add a section titled "Threshold Tuning and Evaluation":

- Compute reconstruction errors for all X_test samples
- Set threshold at 95th percentile of errors where y_test == 0
- Convert errors to binary predictions using the threshold
- Compute and print precision, recall, F1 for the tunneled class
- Plot overlaid histograms: reconstruction error for normal vs tunneled — save to `demo/screenshots/M6B_reconstruction_error.png`
- Add results to the running model comparison table in a markdown cell
- Write 3 sentences: at this threshold, is recall or precision higher? What happens if you raise the threshold? What is the tradeoff?

### Checklist

- [ ] Reconstruction errors computed for all test samples
- [ ] Threshold set at 95th percentile of normal traffic errors
- [ ] Precision, recall, F1 computed and printed
- [ ] Histogram plot saved showing separation between classes
- [ ] Results added to comparison table

### Test Cases

**Test 1 — Histogram separation**
Visually confirm the two histogram peaks (normal vs tunneled) are separated. If they completely overlap, the autoencoder did not learn — check that you trained on normal traffic only.

**Test 2 — Threshold sensitivity**
Recompute at 90th and 99th percentile thresholds. Print recall at each. Confirm that lowering the threshold increases recall (catches more attacks) but also increases false positives. This demonstrates you understand the tradeoff.

**Test 3 — Comparison sanity**
Autoencoder recall should be in a similar ballpark to Isolation Forest recall (both unsupervised). It should be lower than Random Forest recall (supervised has more information). If autoencoder dramatically outperforms Random Forest, something is wrong.

### Re-entry Note

What you built: complete Phase 2 ML — deep anomaly detection with threshold tuning.
Next node: M7A — character tokenisation for CNN and LSTM.
If returning after a break: reload the notebook, reconstruction errors are computed in saved cells.

---

## NODE: M7A

**ID:** M7A
**Title:** Character-Level Tokenisation
**File Path:** `nodes/M7A_char_tokenisation.md`
**Dependencies:** M3E
**Category:** PILLAR 2 — ML PHASE 3
**Week:** 3
**Estimated Time:** 60 minutes

---

### What You Are Building

A tokenisation pipeline that converts domain name strings into fixed-length integer sequences suitable for input to CNN and LSTM models. Each character maps to an integer index. Sequences are padded or truncated to a fixed length of 100.

### How This Fits Into The Project

```
[ M3E — Raw domain name strings in dataset ]
>>> [ M7A — Character tokenisation ] <<<
        ↓  X_seq: integer sequences, shape (n_samples, 100)
[ M7B — 1D CNN reads X_seq ]
[ M7C — LSTM reads X_seq ]
```

Hand-engineered features (M3C) require you to decide what matters. Character-level models learn what matters directly from the raw domain string. This is the same preprocessing used in NLP character-level models — you treat domain names as text sequences. Tokenisation is the only preprocessing step before feeding to the deep learning models.

### What You Need To Know

- Define a vocabulary of all characters that can appear in a domain name: lowercase a-z, digits 0-9, hyphens, dots
- Create a mapping: `char_to_idx = {char: idx+1 for idx, char in enumerate(vocab)}` — start at 1, reserve 0 for padding
- For each domain name, take the subdomain (first label), convert each character to its index, truncate or pad to length 100
- `keras.preprocessing.sequence.pad_sequences` handles padding and truncation automatically
- Save X_seq and the char_to_idx mapping to disk

### What To Study

Search exactly these. Time cap: 10 minutes.

- `keras pad_sequences character level NLP`
- `python character to index mapping tokenisation`

### Practice Exercise

Outside the project folder, write a tokenise function for the vocabulary `"abc"`. Map 'a'→1, 'b'→2, 'c'→3, 0=padding. Tokenise "abcba" with max length 4: should give `[1, 2, 3, 2]` (truncated). Tokenise "ab" with max length 4: should give `[1, 2, 0, 0]` (padded). Delete when done.

### Implementation — What To Build

Add to `pipeline/features.py`:

Write a tokenisation function that:

- Defines the character vocabulary: `'abcdefghijklmnopqrstuvwxyz0123456789-.'`
- Creates the char-to-index mapping (1-indexed, 0 reserved for padding)
- Accepts a domain string, lowercases it, extracts the subdomain (first label before first dot)
- Converts each character to its index (unknown characters map to 0)
- Returns a list of integers

Then in `models/phase3_lstm_cnn.ipynb`:

- Apply the tokenisation function to all domain names in the dataset
- Use `pad_sequences` with maxlen=100, padding='post', truncating='post'
- Save the resulting array as `data/X_seq.npy`
- Save the char_to_idx mapping as `data/char_to_idx.json`
- Print the shape of X_seq — it should be `(n_samples, 100)`

### Checklist

- [ ] Tokenisation function handles unknown characters (maps to 0, no crash)
- [ ] Tokenisation function lowercases input before mapping
- [ ] X_seq shape is (n_samples, 100)
- [ ] No value in X_seq exceeds `len(vocab) + 1` (the max valid index)
- [ ] Padding produces zeros at the end, not the beginning (post-padding)

### Test Cases

**Test 1 — Known sequence**
Tokenise `"google.com"` — the subdomain is `"google"`. The first 6 values should be the indices for g, o, o, g, l, e. Values 6 through 99 should be 0 (padding). Assert this.

**Test 2 — Long subdomain truncation**
Tokenise a 150-character string. The output should be exactly 100 integers. Assert `len(result) == 100`.

**Test 3 — Dataset shape**
After applying to the full dataset: assert `X_seq.shape == (len(dataset), 100)`. Assert `X_seq.max() <= len(vocab) + 1`.

### Re-entry Note

What you built: character-level tokenisation pipeline.
Next node: M7B and M7C can be done in either order — CNN first or LSTM first.
If returning after a break: load X_seq.npy and verify its shape.

---

## NODE: M7B

**ID:** M7B
**Title:** 1D CNN Classifier
**File Path:** `nodes/M7B_cnn.md`
**Dependencies:** M7A
**Category:** PILLAR 2 — ML PHASE 3
**Week:** 4
**Estimated Time:** 90 minutes

---

### What You Are Building

A 1D Convolutional Neural Network that takes character sequences (from M7A) and classifies them as normal or tunneled. The CNN learns local character n-gram patterns — like the statistical signature of Base64 encoding — directly from raw domain strings.

### How This Fits Into The Project

```
[ M7A — X_seq integer sequences ]
>>> [ M7B — 1D CNN ] <<<
        ↓  precision/recall/F1 + saved model
[ M7D — Model comparison (CNN vs LSTM vs RF vs others) ]
```

The CNN treats character sequences the same way a 1D CNN treats time series or text. Convolution filters slide across the character sequence and detect local patterns — recurring character combinations that appear in Base64 but not in normal domain names. This is the same architecture used in production DGA detectors at Cisco and Palo Alto.

### What You Need To Know

- `Embedding(vocab_size+1, embedding_dim, input_length=100)` converts integer indices to dense vectors
- `Conv1D(filters, kernel_size, activation='relu')` is a 1D convolution — kernel_size=3 detects character trigrams
- `MaxPooling1D(2)` downsamples — reduces sequence length by half
- Stack two Conv1D + MaxPooling1D blocks, then `GlobalMaxPooling1D()` to collapse to a fixed vector
- `Dense(64, relu)` → `Dropout(0.3)` → `Dense(1, sigmoid)` for binary output
- Compile with `binary_crossentropy` loss, `adam` optimizer, `accuracy` metric

### What To Study

Search exactly these. Time cap: 15 minutes.

- `keras Conv1D text classification example`
- `keras Embedding layer input_length`

### Practice Exercise

Outside the project folder, build a minimal 1D CNN with input shape (20,) integers, vocab size 10, one Conv1D layer with 16 filters. Compile and call `model.summary()`. Confirm the output shape flows correctly through each layer. Delete when done.

### Implementation — What To Build

In `models/phase3_lstm_cnn.ipynb`, add a section titled "Phase 3A — 1D CNN":

- Load X_seq from `data/X_seq.npy`
- Perform an 80/20 stratified split on X_seq (same indices as M3E so labels align)
- Build the CNN architecture: Embedding → Conv1D(64, 3) → MaxPooling1D(2) → Conv1D(128, 3) → GlobalMaxPooling1D → Dense(64) → Dropout(0.3) → Dense(1, sigmoid)
- Train with EarlyStopping (patience=3)
- Plot training and validation accuracy curves
- Evaluate on test set: print classification report
- Save model to `data/cnn_model/`

### Checklist

- [ ] Model trains without shape errors
- [ ] Training accuracy increases over epochs
- [ ] Classification report printed with tunneled class F1
- [ ] Model saved to disk
- [ ] No data leakage: test split uses same indices as M3E

### Test Cases

**Test 1 — Model summary**
Call `model.summary()`. Confirm the output layer has 1 unit with sigmoid activation.

**Test 2 — Prediction sanity**
Tokenise and pad `"SGVsbG8gV29ybGQ.evil.test"` manually. Pass through the trained CNN. Output should be close to 1.0 (tunneled). Tokenise `"google"` (normal). Output should be close to 0.0.

**Test 3 — Comparison**
CNN F1 on the tunneled class should be comparable to or better than Random Forest F1. If it is dramatically lower (more than 10 points), check that labels are aligned with X_seq correctly.

### Re-entry Note

What you built: character-level CNN classifier.
Next node: M7C — LSTM (can be done before or after M7B).
If returning after a break: load model from disk, run a prediction sanity check.

---

## NODE: M7C

**ID:** M7C
**Title:** LSTM Classifier
**File Path:** `nodes/M7C_lstm.md`
**Dependencies:** M7A
**Category:** PILLAR 2 — ML PHASE 3
**Week:** 4
**Estimated Time:** 90 minutes

---

### What You Are Building

A character-level LSTM that processes domain name character sequences left to right and classifies them as normal or tunneled. The LSTM captures long-range dependencies across the full subdomain string — patterns that span the entire character sequence.

### How This Fits Into The Project

```
[ M7A — X_seq integer sequences ]
>>> [ M7C — LSTM ] <<<
        ↓  precision/recall/F1 + saved model
[ M7D — Model comparison (LSTM vs CNN vs RF) ]
```

While CNN captures local n-gram patterns, LSTM captures sequential dependencies — it remembers what characters appeared earlier in the sequence when processing later ones. Together, CNN and LSTM represent different inductive biases for the same problem, and comparing them is a genuine research question.

### What You Need To Know

- `LSTM(64, return_sequences=True)` returns a sequence output (needed to stack another LSTM on top)
- `LSTM(32)` after that returns a single vector (the final hidden state)
- `return_sequences=True` on all LSTM layers except the last
- Same Embedding and Dense structure as the CNN
- LSTMs train slower than CNNs on the same data — use EarlyStopping

### What To Study

Search exactly these. Time cap: 10 minutes.

- `keras LSTM text classification return_sequences`
- `keras stacked LSTM example`

### Practice Exercise

Outside the project folder, build a minimal stacked LSTM (2 layers) with input shape (20, 5) (sequence of 20 timesteps, 5 features each). Call `model.summary()` and confirm the output shapes. Delete when done.

### Implementation — What To Build

In `models/phase3_lstm_cnn.ipynb`, add a section titled "Phase 3B — LSTM":

- Use the same X_seq and train/test split as M7B
- Build: Embedding(vocab_size+1, 16, input_length=100) → LSTM(64, return_sequences=True) → LSTM(32) → Dense(32, relu) → Dropout(0.3) → Dense(1, sigmoid)
- Train with EarlyStopping (patience=3)
- Evaluate on test set: print classification report
- Save model to `data/lstm_model/`

### Checklist

- [ ] LSTM trains without errors
- [ ] `return_sequences=True` on the first LSTM layer
- [ ] Classification report printed
- [ ] Model saved to disk
- [ ] Training time noted (LSTMs are typically slower than CNNs)

### Test Cases

**Test 1 — Prediction sanity**
Same as M7B Test 2 — tunneled query should score near 1.0, normal query near 0.0.

**Test 2 — CNN vs LSTM**
Compare F1 scores. They should be within 5-10% of each other. Dramatic differences suggest an implementation bug rather than a genuine model difference at this scale.

**Test 3 — Model loads**
Load from disk and run a prediction. Should work without errors.

### Re-entry Note

What you built: character-level LSTM classifier. Phase 3 models are trained.
Next node: M7D — final model comparison table and analysis.
If returning after a break: load model, run prediction check.

---

## NODE: M7D

**ID:** M7D
**Title:** Final Model Comparison and Analysis
**File Path:** `nodes/M7D_model_comparison.md`
**Dependencies:** M7B, M7C
**Category:** PILLAR 2 — ML PHASE 3
**Week:** 4
**Estimated Time:** 60 minutes

---

### What You Are Building

A consolidated comparison table across all 5 models (Random Forest, Isolation Forest, Autoencoder, CNN, LSTM) with precision, recall, F1, and inference time per model. Plus a written analytical conclusion that answers whether raw character sequences outperformed hand-engineered features.

### How This Fits Into The Project

```
[ M5A, M5B, M5C, M6B, M7B, M7C — all models evaluated ]
>>> [ M7D — Unified comparison + conclusion ] <<<
        ↓  comparison table goes into README and Dashboard
[ M8 — Dashboard shows this table in Model Results tab ]
```

This is the headline deliverable of the entire ML pipeline. A table of numbers is not interesting. The analysis — which model worked best, why, what tradeoffs exist, what this tells you about feature engineering vs learned representations — is what makes this a research-quality project rather than a homework submission.

### What You Need To Know

- Inference time: use `time.time()` before and after running `model.predict(X_test)` for each model
- Collect all metrics you already computed in M5A, M5B, M6B, M7B, M7C — you are assembling, not recomputing
- The analytical questions to answer: Does CNN/LSTM outperform RF? Is the gap large enough to justify the compute cost? Where does each model fail?

### Implementation — What To Build

In `models/phase3_lstm_cnn.ipynb`, add a final section titled "Final Model Comparison":

- Assemble a pandas DataFrame with one row per model and columns: Model, Type, Precision, Recall, F1, Inference_Time_ms
- Display it as a formatted table
- Save it as `data/model_comparison.csv`
- Write a conclusion section (minimum 200 words) as a markdown cell addressing: which model has the best recall? Which is fastest? Would you deploy the CNN or RF in production and why? Did learning from raw characters outperform hand-crafted features? What would you try next?

### Checklist

- [ ] All 5 models have entries in the comparison table
- [ ] Inference time is measured and included
- [ ] Table saved to `data/model_comparison.csv`
- [ ] Written conclusion addresses the hand-engineered vs learned representation question
- [ ] Written conclusion makes a deployment recommendation with reasoning

### Test Cases

**Test 1 — Table completeness**
The comparison table has exactly 5 rows and 6 columns. No NaN values.

**Test 2 — Inference time ordering**
Random Forest inference should be faster than LSTM inference (tree models are faster than RNNs). Assert this if your measurements support it.

**Test 3 — Conclusion specificity**
Your written conclusion should mention specific numbers from the table. A conclusion that says "the CNN performed well" without citing F1 scores is insufficient.

### Re-entry Note

What you built: the complete ML comparison — the headline result of the project.
Next node: M8A — Streamlit dashboard.
If returning after a break: the comparison table is saved to CSV. Load it and review the numbers.

---

## NODE: M8A

**ID:** M8A
**Title:** Streamlit Dashboard — Live Feed Tab
**File Path:** `nodes/M8A_dashboard_live.md`
**Dependencies:** M2B, M4A, M5A
**Category:** INTEGRATION
**Week:** 4
**Estimated Time:** 90 minutes

---

### What You Are Building

The first tab of the Streamlit dashboard: an auto-refreshing table that displays recent DNS queries from the SQLite database, colour-coded by anomaly score. This is the live monitoring view — the thing you show in the demo video while running the attack simulator.

### How This Fits Into The Project

```
[ M2B — SQLite with query rows ]
[ M4A — Scored rows with feature vectors ]
[ M5A — RF model for live predictions ]
>>> [ M8A — Live Feed tab ] <<<
        ↓  visual component of M8B and M8C
```

The dashboard is where the two pillars converge visually. A reviewer watching your demo video sees DNS queries flowing in, normal ones marked green, tunneled ones marked red. This single tab communicates the entire project purpose in 30 seconds without any explanation.

### What You Need To Know

- `streamlit run dashboard/app.py` starts the server on localhost:8501
- `st.tabs(["Live Feed", "Model Results", "Query Inspector"])` creates the tab structure
- `st.dataframe(df, use_container_width=True)` displays a DataFrame
- `st.experimental_rerun()` combined with `time.sleep(5)` creates auto-refresh (or use `st.rerun()` in newer versions)
- Colour coding: use pandas Styler — `df.style.applymap(colour_fn)` — to colour rows by anomaly score
- Load the RF model to generate live predictions for each new query

### What To Study

Search exactly these. Time cap: 15 minutes.

- `streamlit tabs dataframe auto refresh`
- `pandas styler applymap background colour`

### Practice Exercise

Outside the project folder, write a minimal Streamlit app with one tab that displays a hardcoded DataFrame with 3 rows and auto-refreshes every 5 seconds (increment a counter to prove refresh is happening). Confirm it runs in browser. Delete when done.

### Implementation — What To Build

Create `dashboard/app.py`:

Build the first tab with:

- A header: "DNS Exfiltration Detection — Live Monitor"
- Query the SQLite database for the 50 most recent rows
- For each row, load its feature vector (if scored) and run the RF model to get a prediction probability
- Display a DataFrame with columns: Timestamp, Query Name, Entropy, Subdomain Length, Prediction Score, Status
- Colour-code the Status column: green for score < 0.3, orange for 0.3-0.7, red for > 0.7
- Auto-refresh every 5 seconds
- Show a count of total queries and flagged queries in the last hour as metric cards

### Checklist

- [ ] Dashboard runs with `streamlit run dashboard/app.py`
- [ ] Live feed table appears with query data
- [ ] Colour coding is visible and correct
- [ ] Table updates approximately every 5 seconds
- [ ] Running the tunnel simulator while the dashboard is open causes red rows to appear

### Test Cases

**Test 1 — Server starts**
`streamlit run dashboard/app.py` should open the browser automatically and show the tab layout without errors.

**Test 2 — Real-time update**
With dashboard open, fire a dig query. Within 10 seconds, the new query should appear in the table (green).

**Test 3 — Attack visible**
With dashboard open, run the tunnel simulator. Tunneled queries should appear as red rows within 10 seconds.

### Re-entry Note

What you built: live monitoring dashboard tab.
Next node: M8B — Model Results tab and Query Inspector tab.
If returning after a break: run dashboard, fire a dig query, confirm it appears.

---

## NODE: M8B

**ID:** M8B
**Title:** Streamlit Dashboard — Model Results and Query Inspector Tabs
**File Path:** `nodes/M8B_dashboard_results.md`
**Dependencies:** M8A, M5C, M6B, M7D
**Category:** INTEGRATION
**Week:** 4
**Estimated Time:** 90 minutes

---

### What You Are Building

The second and third tabs of the Streamlit dashboard. Tab 2 displays static model evaluation results (confusion matrices, ROC curves, model comparison table, SHAP summary). Tab 3 is an interactive query inspector where you type any domain name and get predictions from all 5 models plus a SHAP force plot.

### How This Fits Into The Project

```
[ All saved model results + plots ]
>>> [ M8B — Results + Inspector tabs ] <<<
        ↓  complete 3-tab dashboard
[ M8C — Demo video records this dashboard ]
```

Tab 3 is the most impressive part of the demo. You type `SGVsbG8gV29ybGQ.evil.test` into a text box, hit enter, and watch all 5 models return their prediction scores alongside a SHAP explanation. This communicates the full project depth in one interactive moment.

### What You Need To Know

- `st.image("path/to/plot.png")` displays saved PNG files
- Load model comparison CSV with pandas and display as `st.dataframe`
- `st.text_input("Enter domain name")` creates the query inspector input
- For SHAP force plots in Streamlit, use `shap.force_plot` with matplotlib=True and then `st.pyplot(fig)`
- Load all 5 models at app startup (cache with `@st.cache_resource`) so predictions are fast

### What To Study

Search exactly these. Time cap: 10 minutes.

- `streamlit st.image display png`
- `streamlit cache_resource load model`

### Implementation — What To Build

In `dashboard/app.py`, add Tab 2 and Tab 3:

**Tab 2 — Model Results:**
- Display the model comparison table from `data/model_comparison.csv`
- Display saved confusion matrix PNGs for RF and Autoencoder
- Display SHAP summary plot
- Display reconstruction error histogram

**Tab 3 — Query Inspector:**
- Text input box for a domain name
- On submit: extract features using `extract_features` from M3C, scale with saved scaler
- Run all available models (RF, Isolation Forest, Autoencoder, CNN if feasible, LSTM if feasible)
- Display each model's prediction score as a progress bar or metric
- Display SHAP force plot for the RF model prediction
- Show the feature vector as a small table

### Checklist

- [ ] Tab 2 displays all saved result images without errors
- [ ] Model comparison table is visible in Tab 2
- [ ] Tab 3 text input accepts a domain name
- [ ] Submitting a domain returns prediction scores from at least 3 models
- [ ] SHAP force plot renders correctly for a submitted domain

### Test Cases

**Test 1 — Normal domain**
Type `google.com` in the Query Inspector. All models should return low anomaly scores (below 0.3 for RF). SHAP force plot should show features pushing toward normal.

**Test 2 — Tunneled domain**
Type `SGVsbG8gV29ybGQ.evil.test`. RF should return score above 0.8. SHAP should show entropy and length as primary drivers.

**Test 3 — All tabs load**
Navigate through all three tabs without any error or exception appearing in the terminal.

### Re-entry Note

What you built: complete 3-tab dashboard.
Next node: M8C — README polish and demo video.
If returning after a break: run dashboard, test all three tabs.

---

## NODE: M8C

**ID:** M8C
**Title:** README Polish and Demo Video
**File Path:** `nodes/M8C_readme_demo.md`
**Dependencies:** M8B
**Category:** INTEGRATION
**Week:** 4
**Estimated Time:** 120 minutes

---

### What You Are Building

The final README in its complete state, and a 4-6 minute screencast demo video. These are the two things a recruiter or NTRO reviewer sees before they look at a single line of code.

### How This Fits Into The Project

```
[ Entire project complete ]
>>> [ M8C — README + Demo Video ] <<<
        ↓  GitHub repository is submission-ready
[ NTRO / cybersecurity internship applications ]
```

A strong project with a weak README gets ignored. A clean README with a demo video embedded at the top communicates confidence and professionalism before the reviewer reads a word of your code. The screencast is also your proof of work — it shows the system actually running, not just code that might run.

### What You Need To Know

- Demo video: use OBS Studio (free, no watermark) or Loom. Record at 1080p. Target 4-6 minutes.
- Upload to YouTube as Unlisted, or Google Drive with link-sharing enabled
- Embed the link at the very top of the README, above everything else
- README sections in order: title, video link, one-paragraph description, architecture diagram, quick start, dataset instructions, model results table, security context section, repo structure

### What To Study

Search exactly these. Time cap: 10 minutes.

- `OBS Studio screen record tutorial quick start`

### Demo Video Script

Follow this structure exactly. Times are targets, not hard limits.

- 0:00-1:00 — DNS Server: two terminals side by side. Run server. Fire a dig query. Show hex dump. Show parsed domain name. 20 seconds of narration: "This is a real DNS packet received at byte level."
- 1:00-1:45 — Attack Simulation: run tunnel_sim.py. Show Base64-looking queries scrolling in server terminal. Narrate: "These are DNS queries carrying encoded data in the subdomain field — the tunneling attack."
- 1:45-3:15 — Dashboard Live Feed: open dashboard. Show normal and tunneled queries colour-coded. Click one flagged query. Show SHAP force plot. Narrate: "Entropy of 5.8 and subdomain length of 94 triggered this alert."
- 3:15-4:15 — Model Results: show comparison table. Give one genuine insight about which model performed best and why.
- 4:15-4:45 — Repo tour: 30 seconds in browser. Show folder structure, README, notebooks. Do not walk through code.

### Implementation — What To Build

Final README must contain (in order):

- Project title + one-line description
- Demo video link (bold, prominent)
- Architecture pipeline diagram (ASCII from the project document)
- Quick start: `pip install -r requirements.txt`, run DNS server command, run dashboard command
- Dataset download instructions with URL
- Model results table (filled in with actual numbers from M7D)
- Security Context section: what is DNS tunneling, why is it hard to detect, why ML helps
- Repository structure tree

Then record and upload the demo video. Embed the link.

### Checklist

- [ ] Demo video is recorded and uploaded
- [ ] Video link is at the top of the README
- [ ] All README sections are complete with real content (no placeholders)
- [ ] Model results table has actual numbers from M7D
- [ ] `pip install -r requirements.txt` works in a fresh virtual environment
- [ ] Final commit pushed: `M-8: Streamlit dashboard, demo video embedded, README finalised — project complete`

### Test Cases

**Test 1 — Clean install**
Create a fresh virtual environment. Run `pip install -r requirements.txt`. Then run `python dns_server/server.py`. It should start without import errors. This proves your requirements.txt is complete.

**Test 2 — README renders**
Open your GitHub repository in a browser. The README should render with: a clickable video link, a visible ASCII architecture diagram, a formatted model results table. Check on mobile too.

**Test 3 — Video link works**
Click the demo video link from the README. The video should play without requiring login or access request.

### Re-entry Note

What you built: the complete, submission-ready project.
The project is done. What comes next (optional): AG-1 Docker, AG-2 CharBERT, AG-3 Threat Intel, AG-4 DGA Detection.
If returning after a break: there is nothing left to do on the core project. Pick an additional goal or submit applications.

---

## DEPENDENCY SUMMARY (for graph generation)

```
M0
└── M1A
    └── M1B
        └── M1C
            └── M1D
                └── M1E
                    └── M1F
                        └── M1G
                            └── M2A
                                └── M2B
                                    └── M3A (Pillar 2 begins)
                                        └── M3B
                                            └── M3C
                                                └── M3D
                                                    └── M3E
                                                        ├── M4A
                                                        │   └── M4B
                                                        ├── M5A
                                                        │   └── M5B
                                                        │       └── M5C
                                                        ├── M6A
                                                        │   └── M6B
                                                        └── M7A
                                                            ├── M7B
                                                            └── M7C
                                                                (M7B + M7C) → M7D
                                                                    └── M8A (also needs M2B, M5A)
                                                                        └── M8B (also needs M5C, M6B, M7D)
                                                                            └── M8C
```

Multi-parent nodes (nodes with more than one dependency):
- M4A: depends on M2B AND M3C
- M8A: depends on M2B AND M4A AND M5A
- M8B: depends on M8A AND M5C AND M6B AND M7D
- M7D: depends on M7B AND M7C

---

*End of planning document. Total nodes: 30. All nodes have complete detail page content. Agent should parse each NODE section, extract the file path, and write the content as a markdown file to that path. The index.html should render the dependency graph using the DEPENDENCY SUMMARY above.*
