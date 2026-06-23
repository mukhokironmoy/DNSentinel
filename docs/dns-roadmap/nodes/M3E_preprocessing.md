### What You Are Building

A preprocessing script that takes the fully-featured DataFrame (8 features per row), applies StandardScaler, performs a stratified 80/20 train/test split, and saves the processed feature matrix to `data/features.csv`. This is the final data preparation step before any model training.

### How This Fits Into The Project

```
[ M3D — All 8 features computed ]
>>> [ M3E — Scale + Split + Save ] <<<
        ↓  X_train, X_test, y_train, y_test saved to data/
[ M5 — Random Forest loads this ]
[ M6 — Autoencoder loads this ]
[ M7 — CNN/LSTM loads this ]
```

Every model in the project reads from the same preprocessed data. StandardScaler prevents features with large ranges (like subdomain_length) from dominating features with small ranges (like digit_ratio). Stratified splitting ensures both train and test sets have the same class balance.

### What You Need To Know

- `StandardScaler` fits on training data only — never on test data. `scaler.fit(X_train)`, then `scaler.transform(X_train)` and `scaler.transform(X_test)` separately.
- Stratified split: `train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)`
- Save the scaler using `joblib.dump(scaler, 'data/scaler.pkl')` — models will need it to scale live queries
- Save splits as CSVs: `X_train.to_csv('data/X_train.csv', index=False)` etc.
- Check class balance in both splits after splitting

### What To Study

Search exactly these. Time cap: 10 minutes.

- `sklearn StandardScaler fit transform train test`
- `sklearn train_test_split stratify`

### Practice Exercise

None needed — follow the checklist below.

### Implementation — What To Build

Add to `pipeline/dataset.py`:

Write a preprocessing function that:

- Loads the feature DataFrame (from M3C/M3D results)
- Separates features (X) from labels (y)
- Applies `train_test_split` with `stratify=y` and `random_state=42`
- Fits `StandardScaler` on `X_train` only
- Transforms both `X_train` and `X_test`
- Saves `X_train`, `X_test`, `y_train`, `y_test` as separate CSV files in `data/`
- Saves the fitted scaler to `data/scaler.pkl` using joblib
- Prints class distribution in both train and test splits to confirm stratification worked

### Checklist

- [ ] Four CSV files exist in `data/` after running: X_train, X_test, y_train, y_test
- [ ] `scaler.pkl` exists in `data/`
- [ ] Class distribution percentages in train and test match (approximately) — stratification worked
- [ ] Scaler was fit only on X_train, not on X_test
- [ ] No NaN values in any of the saved files

### Test Cases

**Test 1 — Shape check**
Load the saved CSVs. Assert `len(X_train) + len(X_test) == total_rows` and `len(X_train) / total_rows ≈ 0.8`.

**Test 2 — Stratification check**
Compute `y_train.value_counts(normalize=True)` and `y_test.value_counts(normalize=True)`. The class proportions should match within 1-2%.

**Test 3 — Scaler round-trip**
Load `scaler.pkl`. Apply `scaler.transform(X_test)` again (it was already scaled — this is a sanity check). The values should not change significantly (they are already in the scaled space). Alternatively, verify that `X_train.mean(axis=0)` is approximately 0.0 for all features (StandardScaler centres the data).

### Re-entry Note

What you built: the complete data pipeline. Feature matrix is ready for all three model phases.
What comes next: two parallel tracks. M4A/M4B (live scorer and attack sim) can be done now, or you can jump straight to M5 (Random Forest).
Next node: M4A — live scorer, OR M5A — Random Forest (your choice based on energy).
If returning after a break: load the CSVs and check shapes.

---