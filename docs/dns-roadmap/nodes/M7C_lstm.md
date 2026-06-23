### What You Are Building

A character-level LSTM that processes domain name character sequences left to right and classifies them as normal or tunneled. The LSTM captures long-range dependencies across the full subdomain string — patterns that span the entire character sequence.

### How This Fits Into The Project

```
[ M7A — X_seq integer sequences ]
>>> [ M7C — LSTM ] <<<
        ↓  precision/recall/F1 + saved model
[ M7D — Model comparison (LSTM vs CNN vs RF) ]
```

While CNN captures local n-gram patterns, LSTM captures sequential dependencies — it remembers what characters appeared earlier in the sequence when processing later ones. Together, CNN and LSTM represent different inductive biases for the same problem, and comparing them is a genuine research question.

### What You Need To Know

- `LSTM(64, return_sequences=True)` returns a sequence output (needed to stack another LSTM on top)
- `LSTM(32)` after that returns a single vector (the final hidden state)
- `return_sequences=True` on all LSTM layers except the last
- Same Embedding and Dense structure as the CNN
- LSTMs train slower than CNNs on the same data — use EarlyStopping

### What To Study

Search exactly these. Time cap: 10 minutes.

- `keras LSTM text classification return_sequences`
- `keras stacked LSTM example`

### Practice Exercise

Outside the project folder, build a minimal stacked LSTM (2 layers) with input shape (20, 5) (sequence of 20 timesteps, 5 features each). Call `model.summary()` and confirm the output shapes. Delete when done.

### Implementation — What To Build

In `models/phase3_lstm_cnn.ipynb`, add a section titled "Phase 3B — LSTM":

- Use the same X_seq and train/test split as M7B
- Build: Embedding(vocab_size+1, 16, input_length=100) → LSTM(64, return_sequences=True) → LSTM(32) → Dense(32, relu) → Dropout(0.3) → Dense(1, sigmoid)
- Train with EarlyStopping (patience=3)
- Evaluate on test set: print classification report
- Save model to `data/lstm_model/`

### Checklist

- [ ] LSTM trains without errors
- [ ] `return_sequences=True` on the first LSTM layer
- [ ] Classification report printed
- [ ] Model saved to disk
- [ ] Training time noted (LSTMs are typically slower than CNNs)

### Test Cases

**Test 1 — Prediction sanity**
Same as M7B Test 2 — tunneled query should score near 1.0, normal query near 0.0.

**Test 2 — CNN vs LSTM**
Compare F1 scores. They should be within 5-10% of each other. Dramatic differences suggest an implementation bug rather than a genuine model difference at this scale.

**Test 3 — Model loads**
Load from disk and run a prediction. Should work without errors.

### Re-entry Note

What you built: character-level LSTM classifier. Phase 3 models are trained.
Next node: M7D — final model comparison table and analysis.
If returning after a break: load model, run prediction check.

---