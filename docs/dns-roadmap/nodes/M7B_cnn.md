### What You Are Building

A 1D Convolutional Neural Network that takes character sequences (from M7A) and classifies them as normal or tunneled. The CNN learns local character n-gram patterns — like the statistical signature of Base64 encoding — directly from raw domain strings.

### How This Fits Into The Project

```
[ M7A — X_seq integer sequences ]
>>> [ M7B — 1D CNN ] <<<
        ↓  precision/recall/F1 + saved model
[ M7D — Model comparison (CNN vs LSTM vs RF vs others) ]
```

The CNN treats character sequences the same way a 1D CNN treats time series or text. Convolution filters slide across the character sequence and detect local patterns — recurring character combinations that appear in Base64 but not in normal domain names. This is the same architecture used in production DGA detectors at Cisco and Palo Alto.

### What You Need To Know

- `Embedding(vocab_size+1, embedding_dim, input_length=100)` converts integer indices to dense vectors
- `Conv1D(filters, kernel_size, activation='relu')` is a 1D convolution — kernel_size=3 detects character trigrams
- `MaxPooling1D(2)` downsamples — reduces sequence length by half
- Stack two Conv1D + MaxPooling1D blocks, then `GlobalMaxPooling1D()` to collapse to a fixed vector
- `Dense(64, relu)` → `Dropout(0.3)` → `Dense(1, sigmoid)` for binary output
- Compile with `binary_crossentropy` loss, `adam` optimizer, `accuracy` metric

### What To Study

Search exactly these. Time cap: 15 minutes.

- `keras Conv1D text classification example`
- `keras Embedding layer input_length`

### Practice Exercise

Outside the project folder, build a minimal 1D CNN with input shape (20,) integers, vocab size 10, one Conv1D layer with 16 filters. Compile and call `model.summary()`. Confirm the output shape flows correctly through each layer. Delete when done.

### Implementation — What To Build

In `models/phase3_lstm_cnn.ipynb`, add a section titled "Phase 3A — 1D CNN":

- Load X_seq from `data/X_seq.npy`
- Perform an 80/20 stratified split on X_seq (same indices as M3E so labels align)
- Build the CNN architecture: Embedding → Conv1D(64, 3) → MaxPooling1D(2) → Conv1D(128, 3) → GlobalMaxPooling1D → Dense(64) → Dropout(0.3) → Dense(1, sigmoid)
- Train with EarlyStopping (patience=3)
- Plot training and validation accuracy curves
- Evaluate on test set: print classification report
- Save model to `data/cnn_model/`

### Checklist

- [ ] Model trains without shape errors
- [ ] Training accuracy increases over epochs
- [ ] Classification report printed with tunneled class F1
- [ ] Model saved to disk
- [ ] No data leakage: test split uses same indices as M3E

### Test Cases

**Test 1 — Model summary**
Call `model.summary()`. Confirm the output layer has 1 unit with sigmoid activation.

**Test 2 — Prediction sanity**
Tokenise and pad `"SGVsbG8gV29ybGQ.evil.test"` manually. Pass through the trained CNN. Output should be close to 1.0 (tunneled). Tokenise `"google"` (normal). Output should be close to 0.0.

**Test 3 — Comparison**
CNN F1 on the tunneled class should be comparable to or better than Random Forest F1. If it is dramatically lower (more than 10 points), check that labels are aligned with X_seq correctly.

### Re-entry Note

What you built: character-level CNN classifier.
Next node: M7C — LSTM (can be done before or after M7B).
If returning after a break: load model from disk, run a prediction sanity check.

---