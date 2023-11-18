
import collections
import pandas as pd
import streamlit as st
import tensorflow as tf
from tensorflow import keras
import numpy as np
import pretty_midi
from scipy.io import wavfile
from keras.utils.data_utils import get_file
import midi2audio
import io
from midi2audio import FluidSynth
# import fluidsynth
from infer import process_input, notes_to_midi
from converter import convert
import tempfile
import pathlib
import streamlit as st
# from pydub import AudioSegment
# from music21 import converter, instrument, note, chord, midi


st.title("Image Classification")

@st.cache(allow_output_mutation=True)
def load_model():
    model=tf.keras.models.load_model('model.h5',compile=False)
    # model.compile(loss='mean_squared_error', optimizer='adam',metrics=['accuracy'])
    model.compile()
    return model

with st.spinner("Loading Model...."):
    model=tf.keras.models.load_model('model.h5',compile=False)

    # model=load_model()

fp = st.file_uploader("Upload a file")
if fp is not None:
    
    # https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader
    print(fp) # bytesIO type
    input_pm = pretty_midi.PrettyMIDI(fp)
    instrument = input_pm.instruments[0]
    instrument_name = pretty_midi.program_to_instrument_name(instrument.program)
    print(instrument_name)
    generated_notes = process_input(input_pm,model)
    out_file = 'out.midi'

    # TODO directory to store midi in runtime 
    temp_midi = tempfile.TemporaryFile()

    out_pm = notes_to_midi(
        generated_notes, out_file=temp_midi, 
        instrument_name=instrument_name
        )
    print(type(out_pm))

    # test 4
    # https://docs.python.org/3/library/tempfile.html
    # https://stackoverflow.com/questions/75528026/saving-files-from-streamlit-into-a-temporary-directory
    # https://discuss.streamlit.io/t/accessing-temporary-files-on-streamlit-sharing/16221/4
    # https://stackoverflow.com/questions/70541416/how-to-convert-mid-to-mp3-using-ffmpeg
    temp_dir_mp3 = tempfile.TemporaryDirectory()
    temp_mp3 = tempfile.TemporaryFile()
    # st.write(temp_dir.name)

    # TODO convert midi to mp3
    # conv = AudioSegment.from_file(temp_midi, format="mid")
    # converter.export("out.mp3", format="mp3")
    # conv.export(temp_mp3, format="mp3")

    st.audio(temp_midi)


    # if uploaded_file is not None:
    #     with open(uploaded_file_path, 'wb') as output_temporary_file:
    #         # output_temporary_file.write(uploaded_file.read())
    #         output_temporary_file.write(out_file)
    # else:
    #     st.error('file not created')
    

else:
    st.title('Please upload a midi file')
