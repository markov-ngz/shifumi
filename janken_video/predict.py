import tensorflow as tf
import numpy as np 
import os
# obviously path to hide in production 

model = tf.keras.models.load_model("shifumi_models/model_classifier/")


def predict_coup(image_preprocessed:np.array)->int:
    """
    
    """
    pred = model.predict(image_preprocessed)

    pred_label = np.argmax(pred)

    return pred_label

