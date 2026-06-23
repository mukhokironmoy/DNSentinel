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