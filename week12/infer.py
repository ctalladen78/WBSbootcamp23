import streamlit as st
import collections
import datetime
import numpy as np
import pandas as pd
import pretty_midi
import tensorflow as tf

from typing import Dict, List, Optional, Sequence, Tuple

from keras.layers import Dense, LSTM, LeakyReLU, Input, BatchNormalization, Activation, Dropout
from keras.models import Sequential, load_model, Model
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.optimizers import Adam


def predict_next_note(notes: np.ndarray, keras_model: tf.keras.Model, 
                      temperature: float = 1.0) -> int:
    """Generates a note IDs using a trained sequence model."""
    if keras_model is None:
        print('no model')
        return
    
    assert temperature > 0

    # Add batch dimension
    inputs = tf.expand_dims(notes, 0)

    predictions = keras_model.predict(inputs)
    print(predictions)
    pitch_logits = predictions['pitch']
    step = predictions['step']
    duration = predictions['duration']

    pitch_logits /= temperature
    pitch = tf.random.categorical(pitch_logits, num_samples=1)
    pitch = tf.squeeze(pitch, axis=-1)
    duration = tf.squeeze(duration, axis=-1)
    step = tf.squeeze(step, axis=-1)

    # `step` and `duration` values should be non-negative
    step = tf.maximum(0, step)
    duration = tf.maximum(0, duration)

    return int(pitch), float(step), float(duration)

# generated notes to midi format for export
def notes_to_midi(notes: pd.DataFrame, out_file: str, instrument_name: str,
                  velocity: int = 100) -> pretty_midi.PrettyMIDI:

    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(
      program=pretty_midi.instrument_name_to_program(
          instrument_name))

    prev_start = 0
    for i, note in notes.iterrows():
        start = float(prev_start + note['step'])
        end = float(start + note['duration'])
        
        note = pretty_midi.Note(velocity=velocity, pitch=int(note['pitch']),
                                start=start, end=end)
        instrument.notes.append(note)
        prev_start = start

    pm.instruments.append(instrument)
    # temp_file_2 = tempfile.NamedTemporaryFile(delete=False)

    pm.write(out_file)
    return pm

# example_file = path+'example.midi'
# example_pm = notes_to_midi(
#     raw_notes, out_file=example_file, instrument_name=instrument_name)


def generate(xin,model):
  # generate prediction from sample_notes
  temperature = 2.0
  num_predictions = 120
  seq_length = 25
  vocab_size = 128
  if model is None:
        print('no model')
        return
  
  # sample_notes = np.stack([raw_notes[key] for key in key_order], axis=1)

  # The initial sequence of notes while the pitch is normalized similar to training sequences
  input_notes = (
    xin[:seq_length] / np.array([vocab_size, 1, 1]))

  print(len(input_notes))
  generated_notes_ls = []
  prev_start = 0

  for _ in range(num_predictions):
      pitch, step, duration = predict_next_note(input_notes, model, temperature)
      start = prev_start + step
      end = start + duration
      input_note = (pitch, step, duration)
      generated_notes_ls.append((*input_note, start, end))
      input_notes = np.delete(input_notes, 0, axis=0)
      input_notes = np.append(input_notes, np.expand_dims(input_note, 0), axis=0)
      prev_start = start

  key_order = ['pitch', 'step', 'duration']
  generated_notes_df = pd.DataFrame(
      generated_notes_ls, columns=(*key_order, 'start', 'end'))

  # generated_notes_df.head(10)
  return generated_notes_df

def process_input(input_midi,model):
    if model is None:
        print('no model')
        return
    # pm = input_midi
    instrument = input_midi.instruments[0]
    instrument_name = pretty_midi.program_to_instrument_name(instrument.program)

    notes = collections.defaultdict(list)

    # Sort the notes by start time
    sorted_notes = sorted(instrument.notes, key=lambda note: note.start)
    prev_start = sorted_notes[0].start

    for note in sorted_notes:
        start = note.start
        end = note.end
        notes['pitch'].append(note.pitch)
        notes['start'].append(start)
        notes['end'].append(end)
        notes['step'].append(start - prev_start)
        notes['duration'].append(end - start)
        prev_start = start

    test_midi_df =  pd.DataFrame({name: np.array(value) for name, value in notes.items()})
    test_midi_df.head(1)

    key_order = ['pitch', 'step', 'duration']
    sample_notes0 = np.stack([test_midi_df[key] for key in key_order], axis=1)
    generated_notes0 = generate(sample_notes0,model)
    return generated_notes0