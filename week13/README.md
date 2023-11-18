# Image Classification On CIFAR-10 Dataset

## Introduction:
In this project we create a robust image classification pipeline to classify images.
We created 2 different models and recorded their accuracy and loss.  
The app has been deployed at

## Dataset:
The dataset used in this project is the CIFAR-10 dataset which consists of 60000 32x32 colour images in 10 classes, with 6000 images per class. There are 50000 training images and 10000 test images.

## Models:

### Basic CNN
This is a basic CNN model which uses 2D convolution layers with an increasing amount of filters. Max pooling and Batch normalization are used as regularization techniques.
The total number of parameters is ~4.4 million.

### Usage localhost

```
streamlit run app.py
```