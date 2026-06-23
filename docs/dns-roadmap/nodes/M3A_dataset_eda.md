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