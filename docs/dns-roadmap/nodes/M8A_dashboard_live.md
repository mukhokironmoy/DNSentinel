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