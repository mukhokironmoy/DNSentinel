### What You Are Building

A trained Random Forest classifier that takes the 8-feature vector from M3E and classifies each DNS query as normal or tunneled. You train it, evaluate it with precision/recall/F1 and a confusion matrix, and save the trained model to disk.

### How This Fits Into The Project

```
[ M3E — X_train, X_test, y_train, y_test ]
>>> [ M5A — Random Forest ] <<<
        ↓  trained model saved
[ M5B — Isolation Forest (comparison) ]
[ M5C — SHAP explainability uses this model ]
[ M8 — Dashboard loads this model for Query Inspector ]
```

Random Forest is your supervised baseline. It requires labelled data and learns explicit decision boundaries. Every other model will be compared against it. This is also the model SHAP will explain — making it the most interpretable part of your ML pipeline.

### What You Need To Know

- `RandomForestClassifier(n_estimators=200, random_state=42)` is a solid starting configuration
- `clf.fit(X_train, y_train)` trains. `clf.predict(X_test)` predicts.
- `classification_report(y_test, y_pred)` gives precision, recall, F1 per class
- For tunneling detection, recall on the tunneled class matters more than precision — missing an attack is worse than a false alarm
- A confusion matrix heatmap using seaborn shows true positive, false positive, true negative, false negative visually
- Save the model with `joblib.dump(clf, 'data/rf_model.pkl')`

### What To Study

Search exactly these. Time cap: 10 minutes.

- `sklearn RandomForestClassifier classification report`
- `sklearn confusion matrix seaborn heatmap`

### Practice Exercise

None — go directly to the notebook. The concepts are standard supervised ML.

### Implementation — What To Build

In `models/phase1_classical.ipynb`, add a new section titled "Phase 1A — Random Forest":

- Load X_train, X_test, y_train, y_test from the saved CSVs
- Train a Random Forest with at least 200 trees
- Predict on X_test
- Print the full classification report
- Plot a confusion matrix as a seaborn heatmap — label axes clearly (Normal / Tunneled)
- Plot the ROC curve and compute ROC-AUC score
- Save the trained model to `data/rf_model.pkl`
- Write 3-5 sentences in a markdown cell: what is your F1 on the tunneled class? Where does the model make mistakes? Is precision or recall higher for tunneled queries?

### Checklist

- [ ] Model trains without errors
- [ ] Classification report is printed with per-class precision, recall, F1
- [ ] Confusion matrix heatmap is saved to `demo/screenshots/M5A_confusion_matrix.png`
- [ ] ROC-AUC score is computed and printed
- [ ] Model is saved to `data/rf_model.pkl`
- [ ] F1 score on tunneled class is above 0.80 (if below, check for data issues)

### Test Cases

**Test 1 — Model loads**
After saving, run: `import joblib; clf = joblib.load('data/rf_model.pkl'); clf.predict(X_test[:5])`. Should return an array of 0s and 1s without errors.

**Test 2 — Prediction sanity**
Pass the feature vector for a known tunneled query (high entropy, long subdomain) through the model. It should predict 1 (tunneled). Pass a feature vector for `google.com` (low entropy, short subdomain). It should predict 0 (normal).

**Test 3 — Feature importance**
`clf.feature_importances_` returns an array of importance scores, one per feature. Print them. Entropy and subdomain_length should be among the top 3 most important features. If they are not, revisit feature engineering.

### Re-entry Note

What you built: trained Random Forest classifier with evaluation metrics.
Next node: M5B — Isolation Forest (unsupervised comparison).
If returning after a break: reload the notebook and re-run from the Random Forest section. The model file still exists in data/.

---