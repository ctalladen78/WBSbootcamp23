import streamlit as st
import tensorflow as tf
from tensorflow import keras
import requests
import numpy as np

#Title
st.title("Image Classification")

with st.sidebar:
    st.title('🤗💬 LLM Chat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [OpenAI](https://platform.openai.com/docs/models) LLM model

    ''')
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"


#load model, set cache to prevent reloading
@st.cache(allow_output_mutation=True)
def load_model():
    model=tf.keras.models.load_model('basic_model.keras')
    return model

with st.spinner("Loading Model...."):
    model=load_model()
    
#classes for CIFAR-10 dataset
classes=["airplane","automobile","bird","cat","deer","dog","frog","horse","ship","truck"]

# image preprocessing

#load the prediction image
# @st.cache(allow_output_mutation=True)
def load_image(img_path):
    img=tf.keras.preprocessing.image.load_img(img_path,target_size=(28,28))
    img_tensor=keras.preprocessing.image.img_to_array(img)
    img_tensor=tf.expand_dims(img_tensor,axis=0)
    img_tensor/=255.0
    
    return img_tensor

# image_path = st.file_uploader("", type=["jpg", "png"])
# @st.cache_data
image_path = st.file_uploader(
    "📸 Classes: airplane, automobile,bird,cat,deer,dog,frog,horse,ship,truck", 
    accept_multiple_files=False,
    type=["jpg", "png"]
)

if image_path is not None:
    st.write("Predicting Class...")
    with st.spinner("Classifying..."):
        img_tensor=load_image(image_path)
        pred=model.predict(img_tensor)
        pred_class=classes[np.argmax(pred)]
        st.write("Predicted Class:",pred_class)
        st.image(image_path,use_column_width=True)
            

# from img url
# def load_image(image):
#     img=tf.image.decode_jpeg(image,channels=3)
#     img=tf.cast(img,tf.float32)
#     img/=255.0
#     img=tf.image.resize(img,(28,28))
#     img=tf.expand_dims(img,axis=0)
#     return img

#Get image URL from user
# image_path=st.text_input("Enter Image URL to classify...","https://media.istockphoto.com/photos/passenger-airplane-flying-above-clouds-during-sunset-picture-id155439315?k=20&m=155439315&s=612x612&w=0&h=BvXCpRLaP5h1NnvyYI_2iRtSM0Xsz2jQhAmZ7nA7abA=")

#Get image from URL and predict
# if image_path:
#     try:
#         # content=requests.get(image_path).content
#         st.write("Predicting Class...")
#         with st.spinner("Classifying..."):
#             img_tensor=load_image(content)
#             pred=model.predict(img_tensor)
#             pred_class=classes[np.argmax(pred)]
#             st.write("Predicted Class:",pred_class)
#             st.image(content,use_column_width=True)
#     except:
#         st.write("Invalid URL")

