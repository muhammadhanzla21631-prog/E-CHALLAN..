import numpy as np
import tensorflow as tf
import os
from .preprocess import preprocess_image


# Load TFLite model
tflite_path = "model/model.tflite"
interpreter = None
input_details = None
output_details = None
labels = []
device_used = "CPU"

def load_model():
    global interpreter, input_details, output_details, labels, device_used
    
    delegates = []
    # Try loading GPU delegate
    try:
        # Note: The delegate library must be present in the system library path
        delegate_options = {"precision_loss_allowed": 1, "inference_preference": 1}
        delegate = tf.lite.experimental.load_delegate('libtensorflowlite_gpu_delegate.so', delegate_options)
        delegates.append(delegate)
        device_used = "GPU (TFLite Delegate)"
        print("Success: TFLite GPU Delegate loaded.")
    except Exception as e:
        print(f"Info: TFLite GPU Delegate not found or failed to load. Using CPU. Details: {e}")
        device_used = "CPU"

    # Try loading Model
    try:
        if not os.path.exists(tflite_path):
            raise FileNotFoundError(f"Model file not found at {tflite_path}")

        interpreter = tf.lite.Interpreter(model_path=tflite_path, experimental_delegates=delegates)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        # Load labels
        if os.path.exists("model/labels.txt"):
            with open("model/labels.txt", "r") as f:
                labels = [line.strip() for line in f.readlines()]
        else:
            print("Warning: labels.txt not found.")
            
    except Exception as e:
        print(f"Error: Failed to load TFLite model: {e}")
        print("System will run without ML predictions.")
        interpreter = None
        device_used = "None (Model Failed)"

# Initialize model on import
load_model()

def get_device_info():
    physical_devices = tf.config.list_physical_devices('GPU')
    tf_gpu_available = len(physical_devices) > 0
    return {
        "inference_device": device_used,
        "tf_gpu_available": tf_gpu_available,
        "gpu_devices": [d.name for d in physical_devices]
    }

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