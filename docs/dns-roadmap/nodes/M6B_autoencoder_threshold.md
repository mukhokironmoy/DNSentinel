### What You Are Building

The anomaly scoring and threshold selection for the autoencoder. You compute reconstruction errors for all test queries, choose a threshold (95th percentile of normal traffic errors), convert to binary predictions, and evaluate precision/recall/F1. You also produce the reconstruction error histogram that belongs in the README.

### How This Fits Into The Project

```
[ M6A — Trained autoencoder ]
>>> [ M6B — Threshold tuning + evaluation ] <<<
        ↓  precision/recall/F1 added to comparison table
[ M7D — Final model comparison ]
```

The autoencoder outputs a continuous reconstruction error, not a binary prediction. Choosing where to draw the line between normal and anomalous is a business decision — a lower threshold catches more attacks but causes more false alarms. The 95th percentile of normal errors is a principled starting point.

### What You Need To Know

- Reconstruction error per sample: `MSE = mean((input - reconstruction)^2)` across all features
- Threshold: `np.percentile(errors[y_test == 0], 95)` — 95% of normal traffic errors fall below this
- Predictions: `predictions = (errors > threshold).astype(int)`
- Then compute precision, recall, F1 using sklearn metrics on these binary predictions

### What To Study

No new searches — this is numpy and sklearn metrics from M5A applied to a different score.

### Implementation — What To Build

In `models/phase2_autoencoder.ipynb`, add a section titled "Threshold Tuning and Evaluation":

- Compute reconstruction errors for all X_test samples
- Set threshold at 95th percentile of errors where y_test == 0
- Convert errors to binary predictions using the threshold
- Compute and print precision, recall, F1 for the tunneled class
- Plot overlaid histograms: reconstruction error for normal vs tunneled — save to `demo/screenshots/M6B_reconstruction_error.png`
- Add results to the running model comparison table in a markdown cell
- Write 3 sentences: at this threshold, is recall or precision higher? What happens if you raise the threshold? What is the tradeoff?

### Checklist

- [ ] Reconstruction errors computed for all test samples
- [ ] Threshold set at 95th percentile of normal traffic errors
- [ ] Precision, recall, F1 computed and printed
- [ ] Histogram plot saved showing separation between classes
- [ ] Results added to comparison table

### Test Cases

**Test 1 — Histogram separation**
Visually confirm the two histogram peaks (normal vs tunneled) are separated. If they completely overlap, the autoencoder did not learn — check that you trained on normal traffic only.

**Test 2 — Threshold sensitivity**
Recompute at 90th and 99th percentile thresholds. Print recall at each. Confirm that lowering the threshold increases recall (catches more attacks) but also increases false positives. This demonstrates you understand the tradeoff.

**Test 3 — Comparison sanity**
Autoencoder recall should be in a similar ballpark to Isolation Forest recall (both unsupervised). It should be lower than Random Forest recall (supervised has more information). If autoencoder dramatically outperforms Random Forest, something is wrong.

### Re-entry Note

What you built: complete Phase 2 ML — deep anomaly detection with threshold tuning.
Next node: M7A — character tokenisation for CNN and LSTM.
If returning after a break: reload the notebook, reconstruction errors are computed in saved cells.

---