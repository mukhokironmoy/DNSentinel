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