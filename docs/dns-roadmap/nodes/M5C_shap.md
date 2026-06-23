### What You Are Building

SHAP (SHapley Additive exPlanations) analysis on the Random Forest model. A global summary plot showing which features drive predictions across all queries, and individual force plots for 3 flagged queries showing exactly why each one was classified as tunneled.

### How This Fits Into The Project

```
[ M5A — Trained Random Forest ]
>>> [ M5C — SHAP Explainability ] <<<
        ↓  plots saved to demo/shap_plots/
[ M8 — Dashboard Query Inspector shows SHAP force plots ]
[ Demo video — "entropy of 5.8 triggered this alert" ]
```

Explainability is what separates a research toy from a usable security tool. A SOC analyst cannot act on "the model says this is bad." They need to know which features triggered the alert. SHAP provides this. It is also a strong resume signal — you understand not just that the model works but why.

### What You Need To Know

- `shap.TreeExplainer(clf)` creates an explainer for tree-based models
- `shap_values = explainer.shap_values(X_test)` — for binary classification this returns a list of two arrays (one per class). Use index [1] for the tunneled class.
- `shap.summary_plot` shows global feature importance across all test samples
- `shap.force_plot` shows why a specific prediction was made — which features pushed the score up or down
- Save plots as PNGs using `matplotlib.pyplot.savefig` for the summary plot. Force plots need special handling — use `shap.save_html` or matplotlib backend.

### What To Study

Search exactly these. Time cap: 15 minutes.

- `shap TreeExplainer summary_plot example`
- `shap force_plot save png matplotlib`

### Practice Exercise

None — follow the notebook pattern.

### Implementation — What To Build

In `models/phase1_classical.ipynb`, add a section titled "Phase 1C — SHAP Explainability":

- Create a SHAP TreeExplainer using your saved Random Forest
- Compute SHAP values for the full X_test set
- Generate and save a global summary plot to `demo/shap_plots/shap_summary.png`
- Find 3 test queries that were correctly classified as tunneled (true positives)
- Generate a force plot for each — showing which features pushed the prediction toward tunneled
- Save each force plot to `demo/shap_plots/shap_force_1.png` etc.
- Write a 200-word analysis markdown cell: which feature has the highest global SHAP importance? What do the force plots tell you about individual predictions? Is this consistent with your intuition about which features matter?

### Checklist

- [ ] SHAP summary plot is saved and entropy appears as a top feature
- [ ] Three force plots are saved, one per selected tunneled query
- [ ] Written analysis explains the SHAP findings in plain language
- [ ] Plots are saved to `demo/shap_plots/` with clear filenames

### Test Cases

**Test 1 — Top feature**
From the SHAP summary plot or `shap_values[1].mean(axis=0)`, identify the feature with highest mean absolute SHAP value. It should be either `entropy` or `subdomain_length`. If it is neither, review your feature engineering.

**Test 2 — Force plot direction**
For a correctly flagged tunneled query, the force plot should show entropy and subdomain_length as features pushing the prediction TOWARD tunneled (red arrows). If they push toward normal (blue arrows), the query may not be a true positive — select a different one.

**Test 3 — Plot files exist**
After running the cell, assert all expected files exist in `demo/shap_plots/`.

### Re-entry Note

What you built: SHAP explainability layer on top of Random Forest. Phase 1 ML is complete.
Next node: M6A — Autoencoder (Phase 2 ML).
If returning after a break: reload the notebook and re-run the SHAP section.

---