# Python Snippets for String Quartet Generation (12 Seconds)

The following snippets can be added to the `week12/notebooks/MuseLSTM_midi_apr8.ipynb` notebook to enable the generation of a 12-second string quartet MIDI.

### 1. Updated Prediction Function
This version is cleaner and ensures scalar outputs for recent TensorFlow versions.

```python
import tensorflow as tf
import numpy as np
import pretty_midi

def predict_next_note(notes, model, temperature=1.0):
    """
    Predicts the next note's pitch, step, and duration.
    Input notes: (seq_length, 3) array, pitch normalized (0-1).
    """
    inputs = tf.expand_dims(notes, 0)
    predictions = model.predict(inputs, verbose=0)

    pitch_logits = predictions['pitch']
    step = predictions['step']
    duration = predictions['duration']

    pitch_logits /= temperature
    pitch = tf.random.categorical(pitch_logits, num_samples=1)
    pitch = tf.squeeze(pitch)

    step = tf.maximum(0.0, tf.squeeze(step))
    duration = tf.maximum(0.0, tf.squeeze(duration))

    return int(pitch), float(step), float(duration)
```

### 2. String Quartet Generation Loop
This snippet generates four parts (Violin 1, Violin 2, Viola, Cello) and combines them, limiting the duration to 12 seconds.

```python
def generate_string_quartet(model, seed_notes, out_file='string_quartet.mid', duration_sec=12):
    # Normalize pitch for the model if not already done
    input_notes_template = seed_notes.copy()
    if input_notes_template[:, 0].max() > 1.0:
        input_notes_template[:, 0] /= 128.0

    # Instruments: (Name, MIDI Program)
    instruments_config = [
        ('Violin 1', 40), ('Violin 2', 40), ('Viola', 41), ('Cello', 42)
    ]

    pm_out = pretty_midi.PrettyMIDI()

    for name, program in instruments_config:
        print(f"Generating {name}...")
        inst = pretty_midi.Instrument(program=program, name=name)
        input_seq = input_notes_template.copy()
        prev_start = 0
        current_time = 0

        while current_time < duration_sec:
            pitch, step, duration = predict_next_note(input_seq, model, temperature=1.3)

            start = prev_start + step
            end = start + duration

            # Simple heuristic range check for strings
            if 'Violin' in name: pitch = np.clip(pitch, 55, 100)
            elif 'Viola' in name: pitch = np.clip(pitch, 48, 90)
            elif 'Cello' in name: pitch = np.clip(pitch, 36, 72)

            note = pretty_midi.Note(velocity=np.random.randint(70, 90),
                                    pitch=pitch, start=start, end=end)
            inst.notes.append(note)

            # Update sequence for next prediction
            new_note = np.array([pitch/128.0, step, duration])
            input_seq = np.roll(input_seq, -1, axis=0)
            input_seq[-1] = new_note

            prev_start = start
            current_time = start
            if len(inst.notes) > 500: break

        pm_out.instruments.append(inst)

    pm_out.write(out_file)
    print(f"Saved string quartet to {out_file}")
    return pm_out

# Usage Example (assuming 'model' is loaded and 'sample_notes' is available):
# generate_string_quartet(model, sample_notes)
```
