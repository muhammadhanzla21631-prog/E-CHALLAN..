import requests
import json
import os
import sys

# Configuration
BASE_URL = "http://localhost:8000"

def log(msg, status="INFO"):
    """Print colored log messages"""
    colors = {
        "INFO": "\033[94m",      # Blue
        "SUCCESS": "\033[92m",   # Green
        "WARNING": "\033[93m",   # Yellow
        "ERROR": "\033[91m",     # Red
        "RESET": "\033[0m"
    }
    print(f"{colors.get(status, '')}[{status}] {msg}{colors['RESET']}")

def check_server_health():
    """Check if the server is running"""
    try:
        # Try fetching cameras as a health check since there's no dedicated /health endpoint
        response = requests.get(f"{BASE_URL}/api/cameras")
        if response.status_code == 200:
            log("Server is running and accessible.", "SUCCESS")
            return True
        else:
            log(f"Server returned status code: {response.status_code}", "ERROR")
            return False
    except requests.exceptions.ConnectionError:
        log("Could not connect to server. Is it running? (Try: uvicorn main:app --reload)", "ERROR")
        return False
    except Exception as e:
        log(f"Unexpected error checking server: {e}", "ERROR")
        return False

def test_get_cameras():
    """Test fetching camera list"""
    log("Testing /api/cameras...", "INFO")
    try:
        response = requests.get(f"{BASE_URL}/api/cameras")
        if response.status_code == 200:
            cameras = response.json()
            log(f"Successfully fetched {len(cameras)} cameras.", "SUCCESS")
            if len(cameras) > 0:
                log(f"Sample Camera: {cameras[0]['location'] or cameras[0]['address']} (Status: {cameras[0]['status']})", "INFO")
            return True
        else:
            log(f"Failed to fetch cameras. Status: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"Error testing cameras: {e}", "ERROR")
        return False

def test_analytics_dashboard():
    """Test fetching dashboard analytics"""
    log("Testing /api/analytics/dashboard...", "INFO")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/dashboard")
        if response.status_code == 200:
            data = response.json()
            log("Dashboard Analytics Data:", "INFO")
            print(json.dumps(data, indent=2))
            log("Successfully fetched analytics.", "SUCCESS")
            return True
        else:
            log(f"Failed to fetch analytics. Status: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"Error testing analytics: {e}", "ERROR")
        return False

def test_prediction_endpoint():
    """Test the image prediction endpoint"""
    log("Testing /predict (Image Prediction)...", "INFO")
    
    # Create a dummy image for testing
    img_path = "temp_test_image.jpg"
    try:
        # Create a simple black image using PIL if available, else random bytes
        try:
            from PIL import Image
            img = Image.new('RGB', (100, 100), color = 'red')
            img.save(img_path)
        except ImportError:
            with open(img_path, "wb") as f:
                f.write(os.urandom(1024))
        
        with open(img_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/predict", files=files)
            
        if response.status_code == 200:
            result = response.json()
            log(f"Prediction Result: {result}", "SUCCESS")
            return True
        else:
            log(f"Prediction failed. Status: {response.status_code}", "ERROR")
            log(f"Response: {response.text}", "ERROR")
            return False
            
    except Exception as e:
        log(f"Error testing prediction: {e}", "ERROR")
        return False
    finally:
        # Cleanup
        if os.path.exists(img_path):
            os.remove(img_path)

def test_challan_history():
    """Test fetching challan history"""
    log("Testing /api/challans...", "INFO")
    try:
        response = requests.get(f"{BASE_URL}/api/challans?limit=5")
        if response.status_code == 200:
            data = response.json()
            count = data.get('count', 0)
            log(f"Successfully fetched challans. Total count: {count}", "SUCCESS")
            return True
        else:
            log(f"Failed to fetch challans. Status: {response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"Error testing challans: {e}", "ERROR")
        return False

def main():
    print("=======================================")
    print("   E-CHALLAN SYSTEM - API TEST SCRIPT  ")
    print("=======================================")
    
    if not check_server_health():
        sys.exit(1)
        
    print("\n--- Running Tests ---\n")
    
    results = {
        "Cameras": test_get_cameras(),
        "Analytics": test_analytics_dashboard(),
        "Challans": test_challan_history(),
        "Prediction": test_prediction_endpoint()
    }
    
    print("\n=======================================")
    print("   TEST SUMMARY  ")
    print("=======================================")
    all_passed = True
    for test, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        color = "\033[92m" if passed else "\033[91m"
        print(f"{test}: {color}{status}\033[0m")
        if not passed:
            all_passed = False
            
    if all_passed:
        print("\n\033[92mAll tests passed successfully! The backend is ready for the frontend.\033[0m")
    else:
        print("\n\033[91mSome tests failed. Please check the logs above.\033[0m")

if __name__ == "__main__":
    main()
