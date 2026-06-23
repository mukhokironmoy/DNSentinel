### What You Are Building

The second and third tabs of the Streamlit dashboard. Tab 2 displays static model evaluation results (confusion matrices, ROC curves, model comparison table, SHAP summary). Tab 3 is an interactive query inspector where you type any domain name and get predictions from all 5 models plus a SHAP force plot.

### How This Fits Into The Project

```
[ All saved model results + plots ]
>>> [ M8B — Results + Inspector tabs ] <<<
        ↓  complete 3-tab dashboard
[ M8C — Demo video records this dashboard ]
```

Tab 3 is the most impressive part of the demo. You type `SGVsbG8gV29ybGQ.evil.test` into a text box, hit enter, and watch all 5 models return their prediction scores alongside a SHAP explanation. This communicates the full project depth in one interactive moment.

### What You Need To Know

- `st.image("path/to/plot.png")` displays saved PNG files
- Load model comparison CSV with pandas and display as `st.dataframe`
- `st.text_input("Enter domain name")` creates the query inspector input
- For SHAP force plots in Streamlit, use `shap.force_plot` with matplotlib=True and then `st.pyplot(fig)`
- Load all 5 models at app startup (cache with `@st.cache_resource`) so predictions are fast

### What To Study

Search exactly these. Time cap: 10 minutes.

- `streamlit st.image display png`
- `streamlit cache_resource load model`

### Implementation — What To Build

In `dashboard/app.py`, add Tab 2 and Tab 3:

**Tab 2 — Model Results:**
- Display the model comparison table from `data/model_comparison.csv`
- Display saved confusion matrix PNGs for RF and Autoencoder
- Display SHAP summary plot
- Display reconstruction error histogram

**Tab 3 — Query Inspector:**
- Text input box for a domain name
- On submit: extract features using `extract_features` from M3C, scale with saved scaler
- Run all available models (RF, Isolation Forest, Autoencoder, CNN if feasible, LSTM if feasible)
- Display each model's prediction score as a progress bar or metric
- Display SHAP force plot for the RF model prediction
- Show the feature vector as a small table

### Checklist

- [ ] Tab 2 displays all saved result images without errors
- [ ] Model comparison table is visible in Tab 2
- [ ] Tab 3 text input accepts a domain name
- [ ] Submitting a domain returns prediction scores from at least 3 models
- [ ] SHAP force plot renders correctly for a submitted domain

### Test Cases

**Test 1 — Normal domain**
Type `google.com` in the Query Inspector. All models should return low anomaly scores (below 0.3 for RF). SHAP force plot should show features pushing toward normal.

**Test 2 — Tunneled domain**
Type `SGVsbG8gV29ybGQ.evil.test`. RF should return score above 0.8. SHAP should show entropy and length as primary drivers.

**Test 3 — All tabs load**
Navigate through all three tabs without any error or exception appearing in the terminal.

### Re-entry Note

What you built: complete 3-tab dashboard.
Next node: M8C — README polish and demo video.
If returning after a break: run dashboard, test all three tabs.

---