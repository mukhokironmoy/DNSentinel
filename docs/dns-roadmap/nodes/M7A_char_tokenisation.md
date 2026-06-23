### What You Are Building

A tokenisation pipeline that converts domain name strings into fixed-length integer sequences suitable for input to CNN and LSTM models. Each character maps to an integer index. Sequences are padded or truncated to a fixed length of 100.

### How This Fits Into The Project

```
[ M3E — Raw domain name strings in dataset ]
>>> [ M7A — Character tokenisation ] <<<
        ↓  X_seq: integer sequences, shape (n_samples, 100)
[ M7B — 1D CNN reads X_seq ]
[ M7C — LSTM reads X_seq ]
```

Hand-engineered features (M3C) require you to decide what matters. Character-level models learn what matters directly from the raw domain string. This is the same preprocessing used in NLP character-level models — you treat domain names as text sequences. Tokenisation is the only preprocessing step before feeding to the deep learning models.

### What You Need To Know

- Define a vocabulary of all characters that can appear in a domain name: lowercase a-z, digits 0-9, hyphens, dots
- Create a mapping: `char_to_idx = {char: idx+1 for idx, char in enumerate(vocab)}` — start at 1, reserve 0 for padding
- For each domain name, take the subdomain (first label), convert each character to its index, truncate or pad to length 100
- `keras.preprocessing.sequence.pad_sequences` handles padding and truncation automatically
- Save X_seq and the char_to_idx mapping to disk

### What To Study

Search exactly these. Time cap: 10 minutes.

- `keras pad_sequences character level NLP`
- `python character to index mapping tokenisation`

### Practice Exercise

Outside the project folder, write a tokenise function for the vocabulary `"abc"`. Map 'a'→1, 'b'→2, 'c'→3, 0=padding. Tokenise "abcba" with max length 4: should give `[1, 2, 3, 2]` (truncated). Tokenise "ab" with max length 4: should give `[1, 2, 0, 0]` (padded). Delete when done.

### Implementation — What To Build

Add to `pipeline/features.py`:

Write a tokenisation function that:

- Defines the character vocabulary: `'abcdefghijklmnopqrstuvwxyz0123456789-.'`
- Creates the char-to-index mapping (1-indexed, 0 reserved for padding)
- Accepts a domain string, lowercases it, extracts the subdomain (first label before first dot)
- Converts each character to its index (unknown characters map to 0)
- Returns a list of integers

Then in `models/phase3_lstm_cnn.ipynb`:

- Apply the tokenisation function to all domain names in the dataset
- Use `pad_sequences` with maxlen=100, padding='post', truncating='post'
- Save the resulting array as `data/X_seq.npy`
- Save the char_to_idx mapping as `data/char_to_idx.json`
- Print the shape of X_seq — it should be `(n_samples, 100)`

### Checklist

- [ ] Tokenisation function handles unknown characters (maps to 0, no crash)
- [ ] Tokenisation function lowercases input before mapping
- [ ] X_seq shape is (n_samples, 100)
- [ ] No value in X_seq exceeds `len(vocab) + 1` (the max valid index)
- [ ] Padding produces zeros at the end, not the beginning (post-padding)

### Test Cases

**Test 1 — Known sequence**
Tokenise `"google.com"` — the subdomain is `"google"`. The first 6 values should be the indices for g, o, o, g, l, e. Values 6 through 99 should be 0 (padding). Assert this.

**Test 2 — Long subdomain truncation**
Tokenise a 150-character string. The output should be exactly 100 integers. Assert `len(result) == 100`.

**Test 3 — Dataset shape**
After applying to the full dataset: assert `X_seq.shape == (len(dataset), 100)`. Assert `X_seq.max() <= len(vocab) + 1`.

### Re-entry Note

What you built: character-level tokenisation pipeline.
Next node: M7B and M7C can be done in either order — CNN first or LSTM first.
If returning after a break: load X_seq.npy and verify its shape.

---