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