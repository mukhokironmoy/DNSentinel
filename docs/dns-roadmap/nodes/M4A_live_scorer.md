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