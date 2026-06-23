### What You Are Building

A Keras autoencoder trained only on normal DNS traffic. The encoder compresses the 8-feature input to a 8-dimensional bottleneck. The decoder reconstructs the original input. After training, queries that reconstruct poorly (high reconstruction error) are flagged as anomalous.

### How This Fits Into The Project

```
[ M3E — Feature matrix ]
>>> [ M6A — Autoencoder training ] <<<
        ↓  trained encoder + decoder saved
[ M6B — Threshold tuning + anomaly scoring ]
        ↓
[ M7D — Model comparison table ]
```

The autoencoder has never seen tunneled traffic during training. It learns to reconstruct normal DNS patterns. When it tries to reconstruct a tunneled query, it fails — because the pattern is unfamiliar. The reconstruction error is the anomaly score. This is unsupervised deep learning for threat detection.

### What You Need To Know

- Encoder: Dense layers that progressively reduce dimensionality (input → 32 → 16 → 8)
- Decoder: Dense layers that progressively expand back (8 → 16 → 32 → input_dim)
- The full autoencoder chains encoder and decoder
- Loss function: Mean Squared Error (MSE) between input and reconstruction
- Train on normal traffic only: `X_train_normal = X_train[y_train == 0]`
- Use early stopping: stop training when validation loss stops improving
- `activation='relu'` for hidden layers, `activation='sigmoid'` for the output layer (features are scaled 0-1 after StandardScaler... actually verify this: sigmoid only if features are in [0,1] range. If StandardScaler output can be negative, use linear activation on output.)

### What To Study

Search exactly these. Time cap: 15 minutes.

- `keras autoencoder anomaly detection example`
- `keras EarlyStopping callback`

### Practice Exercise

Outside the project folder, build a tiny autoencoder with input dimension 4, bottleneck 2. Train it on 100 random rows of data. Plot training loss. Confirm loss decreases. Delete when done.

### Implementation — What To Build

Create `models/phase2_autoencoder.ipynb`:

- Load X_train, X_test, y_train, y_test from saved CSVs
- Extract normal-only training data
- Define encoder and decoder as separate Sequential models, then chain them
- Compile with Adam optimizer and MSE loss
- Train with EarlyStopping (patience=5, restore_best_weights=True) and 10% validation split
- Plot training and validation loss curves — save to `demo/screenshots/M6A_loss_curves.png`
- Save the trained autoencoder to `data/autoencoder_model/` using `model.save()`

### Checklist

- [ ] Autoencoder trains without errors
- [ ] Training loss decreases over epochs (loss curve goes down)
- [ ] Validation loss does not diverge significantly from training loss (no severe overfitting)
- [ ] Model is saved to disk
- [ ] Loss curve plot is saved

### Test Cases

**Test 1 — Loss decrease**
After training, assert `history.history['loss'][-1] < history.history['loss'][0]`. Loss must have decreased.

**Test 2 — Reconstruction check**
Pass one normal query through the autoencoder. Compute MSE between input and output. Pass one tunneled query. The tunneled query's MSE should be higher. This is the core assumption of the model.

**Test 3 — Model loads**
After saving: `from tensorflow import keras; ae = keras.models.load_model('data/autoencoder_model/')`. Should load without errors.

### Re-entry Note

What you built: trained autoencoder on normal traffic.
Next node: M6B — threshold tuning and anomaly scoring.
If returning after a break: reload model from disk, run one reconstruction check.

---