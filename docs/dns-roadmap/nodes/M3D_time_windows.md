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