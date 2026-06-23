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