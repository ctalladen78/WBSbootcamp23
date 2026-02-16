import collections
import numpy as np
import pandas as pd
import pretty_midi
import tensorflow as tf

def predict_next_note(notes, model, temperature=1.0):
    """
    Predicts the next note's pitch, step, and duration.
    Input notes should be a (seq_length, 3) array where pitch is normalized (0-1).
    """
    inputs = tf.expand_dims(notes, 0)
    predictions = model.predict(inputs, verbose=0)

    pitch_logits = predictions['pitch']
    step = predictions['step']
    duration = predictions['duration']

    pitch_logits /= temperature
    pitch = tf.random.categorical(pitch_logits, num_samples=1)
    pitch = tf.squeeze(pitch) # Squeeze all dimensions to get a scalar

    # Ensure step and duration are non-negative and scalar
    step = tf.maximum(0.0, tf.squeeze(step))
    duration = tf.maximum(0.0, tf.squeeze(duration))

    return int(pitch), float(step), float(duration)

def generate_string_quartet(model_path, out_file='string_quartet.mid', duration_sec=12, seed_midi_path=None):
    """
    Generates a 12-second string quartet MIDI using the provided model.
    """
    try:
        model = tf.keras.models.load_model(model_path, compile=False)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # 1. Prepare a seed sequence
    # If no seed MIDI is provided, use a default sequence
    seq_length = 25
    if seed_midi_path:
        try:
            pm_seed = pretty_midi.PrettyMIDI(seed_midi_path)
            instrument = pm_seed.instruments[0]
            sorted_notes = sorted(instrument.notes, key=lambda x: x.start)
            seed_data = []
            prev_start = sorted_notes[0].start
            for n in sorted_notes[:seq_length]:
                seed_data.append([n.pitch, n.start - prev_start, n.end - n.start])
                prev_start = n.start
            seed_notes = np.array(seed_data)
        except:
            print("Could not load seed MIDI, using default.")
            seed_notes = np.zeros((seq_length, 3))
            seed_notes[:, 0] = 60; seed_notes[:, 1] = 0.5; seed_notes[:, 2] = 0.5
    else:
        seed_notes = np.zeros((seq_length, 3))
        # Default seed: C4 notes
        seed_notes[:, 0] = 60
        seed_notes[:, 1] = 0.4
        seed_notes[:, 2] = 0.3

    # Normalize pitch for the model (0-1 range)
    input_notes_template = seed_notes.copy()
    input_notes_template[:, 0] /= 128.0

    # String Quartet: Violin 1, Violin 2, Viola, Cello
    instruments_config = [
        ('Violin 1', 40),
        ('Violin 2', 40),
        ('Viola', 41),
        ('Cello', 42)
    ]

    pm_out = pretty_midi.PrettyMIDI()

    for name, program in instruments_config:
        print(f"Generating track for {name}...")
        inst = pretty_midi.Instrument(program=program, name=name)
        input_seq = input_notes_template.copy()

        prev_start = 0
        current_time = 0

        # Use a slightly higher temperature for diversity between parts
        temp = 1.3

        while current_time < duration_sec:
            pitch, step, duration = predict_next_note(input_seq, model, temp)

            start = prev_start + step
            end = start + duration

            # Simple heuristic range check for string instruments
            # (Optional, but helps keep it somewhat realistic)
            if name.startswith('Violin'):
                pitch = np.clip(pitch, 55, 100)
            elif name == 'Viola':
                pitch = np.clip(pitch, 48, 90)
            elif name == 'Cello':
                pitch = np.clip(pitch, 36, 72)

            note = pretty_midi.Note(velocity=np.random.randint(70, 90),
                                    pitch=pitch, start=start, end=end)
            inst.notes.append(note)

            # Update sequence
            new_note = np.array([pitch/128.0, step, duration])
            input_seq = np.roll(input_seq, -1, axis=0)
            input_seq[-1] = new_note

            prev_start = start
            current_time = start

            if len(inst.notes) > 500: break # Safety break

        pm_out.instruments.append(inst)

    pm_out.write(out_file)
    print(f"Successfully saved 12-second string quartet to {out_file}")

if __name__ == "__main__":
    import os
    # Look for model in common locations
    model_file = 'model.h5'
    if not os.path.exists(model_file):
        model_file = 'week12/model.h5'

    if os.path.exists(model_file):
        generate_string_quartet(model_file)
    else:
        print(f"Model file not found (checked 'model.h5' and 'week12/model.h5').")
