import numpy as np
import tensorflow as tf
from .preprocess import preprocess_image


# Load TFLite model
tflite_path = "model/model.tflite"
interpreter = None
input_details = None
output_details = None
labels = []

try:
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    # Load labels
    with open("model/labels.txt", "r") as f:
        labels = [line.strip() for line in f.readlines()]
except Exception as e:
    print(f"Warning: Could not load model or labels: {e}")


def predict_image(image_bytes):
    if interpreter is None:
        return "Model not loaded (Dummy Prediction)"
        
    img = preprocess_image(image_bytes)
    img = np.expand_dims(img, axis=0).astype(np.float32)

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])[0]
    label_index = np.argmax(output)
    if label_index < len(labels):
        return labels[label_index]
    return "Unknown"