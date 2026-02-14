# Music Generator Summary and Suggested Improvements

## Notebook Summary: `week12/notebooks/MuseLSTM_midi_apr8.ipynb`

The notebook demonstrates a deep learning approach to music generation using Long Short-Term Memory (LSTM) neural networks trained on MIDI data.

### Workflow:
1.  **Environment Setup**: Installs `pretty_midi` and imports essential libraries like `tensorflow`, `numpy`, `pandas`, and `pretty_midi`.
2.  **Data Acquisition**: Downloads the MAESTRO dataset (v2.0.0), which contains over 1,200 MIDI files of piano performances.
3.  **Preprocessing**:
    *   **MIDI to Notes**: Uses `pretty_midi` to extract note information (pitch, start, end) and calculates `step` (time delta between note starts) and `duration`.
    *   **Sequence Generation**: Creates training sequences of 25 notes each. The input to the model is a window of 25 notes, and the target is the subsequent note.
    *   **Normalization**: Pitches are normalized by dividing by the vocabulary size (128).
4.  **Model Architecture**:
    *   An `Input` layer accepting sequences of shape `(25, 3)` (pitch, step, duration).
    *   An `LSTM` layer with 128 units.
    *   Three concurrent `Dense` output heads:
        *   `pitch`: 128 units (intended for note classification).
        *   `step`: 1 unit (regression for timing).
        *   `duration`: 1 unit (regression for note length).
5.  **Training**:
    *   The model is compiled using `mean_squared_error` for all three outputs and optimized with `Adam`.
    *   It is trained for 10 epochs on a small subset (5 files) of the MAESTRO dataset.
6.  **Inference (Generation)**:
    *   Includes a `predict_next_note` function that uses the trained model to sample the next note's properties.
    *   Uses a `temperature` parameter to control the randomness of pitch selection via `tf.random.categorical`.
    *   A generation loop produces a sequence of new notes by iteratively feeding predictions back into the model.

---

## Suggested Improvements

### 1. Refine the Loss Function for Pitch
*   **Current state**: The model uses `mean_squared_error` for the 128-unit pitch output.
*   **Improvement**: Change the loss for the `pitch` head to `SparseCategoricalCrossentropy`. Pitch is a categorical variable. Categorical cross-entropy allows the model to learn a proper probability distribution over the 128 possible MIDI pitches, which is more appropriate than regression-based losses for this feature.

### 2. Scale Training Data
*   **Current state**: The model is trained on only 5 MIDI files.
*   **Improvement**: Train on a significantly larger portion of the MAESTRO dataset (which has >1,200 files). A larger and more diverse dataset will help the model learn more complex musical structures, styles, and harmonic transitions.

### 3. Incorporate Note Velocity
*   **Current state**: The model only predicts pitch, step, and duration, ignoring how hard a note is struck.
*   **Improvement**: Add `velocity` as a fourth feature in both the input and output layers. Velocity is critical for musical expression and dynamics, and including it will result in more human-like, expressive generation.

### 4. Enhance Model Architecture
*   **Stacked LSTMs**: Use multiple LSTM layers to capture more hierarchical and abstract musical patterns.
*   **Attention Mechanisms/Transformers**: Moving towards a Transformer-based architecture or adding an Attention layer to the LSTM can significantly improve the model's ability to maintain long-term structural coherence in the music.
*   **Regularization**: Incorporate `Dropout` or `BatchNormalization` layers to improve training stability and prevent overfitting as the model and dataset scale.

### 5. Data Augmentation
*   **Transposition**: Randomly shift the pitch of training sequences up or down. This teaches the model that musical patterns are independent of the absolute key.
*   **Time Stretching**: Slightly scale the timing (`step` and `duration`) to simulate tempo variations.

### 6. Better Handling of Polyphony
*   **Improvement**: While the current model can represent chords if `step` is 0, explicitly designing for polyphony (e.g., using multi-hot encoding for pitches or chord-specific representations) would better capture harmonic relationships.
