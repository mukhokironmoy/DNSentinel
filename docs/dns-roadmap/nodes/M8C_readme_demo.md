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