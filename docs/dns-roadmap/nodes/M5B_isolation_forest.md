### What You Are Building

A trained Isolation Forest model that detects anomalous DNS queries without using any labels during training. It learns what normal traffic looks like and flags deviations. You compare its performance directly against the Random Forest from M5A.

### How This Fits Into The Project

```
[ M5A — Random Forest (supervised) ]
>>> [ M5B — Isolation Forest (unsupervised) ] <<<
        ↓  anomaly scores + predictions
[ M5C — SHAP explains Random Forest ]
[ M7D — Model comparison table includes both ]
```

Isolation Forest represents how detection works when you have no labelled attack data — which is realistic for new attack variants. Training on normal traffic only and flagging statistical outliers is a production-realistic approach. Comparing it to the supervised model reveals the cost of not having labels.

### What You Need To Know

- `IsolationForest(contamination=0.05, random_state=42)` — contamination estimates the fraction of anomalies expected in the data (roughly)
- Train ONLY on normal traffic samples: `iso.fit(X_train[y_train == 0])`
- `iso.decision_function(X_test)` returns anomaly scores — more negative = more anomalous
- `iso.predict(X_test)` returns 1 (normal) or -1 (anomaly) — remap -1 to 1 and 1 to 0 for consistency with your label encoding
- Compare precision, recall, F1 against Random Forest in a markdown table

### What To Study

Search exactly these. Time cap: 10 minutes.

- `sklearn IsolationForest fit predict anomaly detection`
- `sklearn IsolationForest decision_function scores`

### Practice Exercise

None — follow the notebook pattern from M5A.

### Implementation — What To Build

In `models/phase1_classical.ipynb`, add a section titled "Phase 1B — Isolation Forest":

- Extract normal-only training samples: rows where label is 0
- Fit Isolation Forest on those samples only
- Run `predict` and `decision_function` on the full X_test
- Remap predictions from {1, -1} to {0, 1}
- Compute precision, recall, F1 on the tunneled class
- Plot the distribution of anomaly scores for normal vs tunneled queries (two overlaid histograms)
- Create a markdown comparison table: Random Forest vs Isolation Forest side by side with precision, recall, F1
- Write 3-5 sentences: where did Isolation Forest miss? Is the recall higher or lower than Random Forest? What does this tell you?

### Checklist

- [ ] Model is trained only on normal traffic
- [ ] Anomaly score distributions for both classes are plotted
- [ ] Predictions are remapped to consistent 0/1 encoding
- [ ] Comparison table with Random Forest exists in the notebook
- [ ] Written analysis explains the performance difference

### Test Cases

**Test 1 — Score distribution**
The mean anomaly score for tunneled queries should be more negative than for normal queries. Assert `scores[y_test == 1].mean() < scores[y_test == 0].mean()`.

**Test 2 — No label leakage**
Confirm you did not accidentally include any tunneled rows in training. `assert (y_train[iso_train_mask] == 0).all()` where iso_train_mask selects what you trained on.

**Test 3 — Comparison sanity**
Isolation Forest recall should be lower than Random Forest recall on the tunneled class (it has less information). If Isolation Forest outperforms Random Forest, something is wrong with one of the setups — investigate before continuing.

### Re-entry Note

What you built: unsupervised anomaly detector + comparison to supervised baseline.
Next node: M5C — SHAP explainability for the Random Forest.
If returning after a break: reload notebook, results are in the cells.

---