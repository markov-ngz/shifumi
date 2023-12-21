import tensorflow as tf
import numpy as np 
# obviously path to hide in production 
# model = tf.keras.models.load_model(r"path_to_model")


def predict_coup(image_preprocessed:np.array)->int:
    """
    
    """
    pred = model.predict(image_preprocessed)

    pred_label = np.argmax(pred,axis=0)

    return pred_label

