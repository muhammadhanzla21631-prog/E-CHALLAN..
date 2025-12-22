# GPU Support Setup

This project uses TensorFlow Lite for inference. To enable GPU acceleration, you need to ensure that the TensorFlow Lite GPU Delegate is available on your system.

## Prerequisites

1.  **NVIDIA GPU**: Ensure you have a compatible NVIDIA GPU.
2.  **Drivers**: Install the latest NVIDIA drivers.
3.  **CUDA & cuDNN**: Install the appropriate CUDA Toolkit and cuDNN versions compatible with your TensorFlow version.

## Enabling GPU for TFLite

The backend is configured to automatically look for the TFLite GPU Delegate library (`libtensorflowlite_gpu_delegate.so` on Linux).

### Steps to Install Delegate

1.  **Build or Download the Delegate**:
    You typically need to build the TensorFlow Lite GPU delegate from source or find a pre-built binary for your architecture.
    
    If you are using the full `tensorflow` package (as listed in `requirements.txt`), it might not include the delegate shared library by default in a way that is easily loadable via `load_delegate` without some configuration.

    **Option A: Using `tflite-runtime` (Recommended for Edge Devices)**
    If you are on an edge device (like Jetson Nano or Raspberry Pi), install `tflite-runtime` which often comes with delegates.

    **Option B: Building from Source (Linux)**
    Clone the TensorFlow repository and build the delegate:
    ```bash
    bazel build -c opt --config=cuda //tensorflow/lite/delegates/gpu:libtensorflowlite_gpu_delegate.so
    ```
    Then copy the resulting `.so` file to your system library path (e.g., `/usr/lib/`) or the project directory.

2.  **Verify Installation**:
    Start the backend server:
    ```bash
    uvicorn main:app --reload
    ```
    Check the logs for:
    `Success: TFLite GPU Delegate loaded.`
    
    Or visit the system info endpoint:
    `GET /api/system/info`

## Troubleshooting

-   **"TFLite GPU Delegate not found"**: This means the `.so` file is missing or not in the library path. The system will fall back to CPU.
-   **CUDA Errors**: Ensure your CUDA/cuDNN versions match the TensorFlow version installed.

## Standard TensorFlow GPU

The project also checks for standard TensorFlow GPU availability. If you switch to using standard TensorFlow models (SavedModel format) instead of TFLite, `tensorflow` will automatically use the GPU if CUDA is correctly configured.
