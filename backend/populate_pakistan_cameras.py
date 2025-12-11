import requests
import random

BASE_URL = "http://0.0.0.0:8000"

cities = {
    "Islamabad": {"lat": 33.6844, "lng": 73.0479},
    "Karachi": {"lat": 24.8607, "lng": 67.0011},
    "Lahore": {"lat": 31.5204, "lng": 74.3587},
    "Peshawar": {"lat": 34.0151, "lng": 71.5249},
    "Quetta": {"lat": 30.1798, "lng": 66.9750},
    "Multan": {"lat": 30.1575, "lng": 71.5249},
    "Faisalabad": {"lat": 31.4504, "lng": 73.1350},
    "Rawalpindi": {"lat": 33.5651, "lng": 73.0169},
    "Hyderabad": {"lat": 25.3960, "lng": 68.3578},
    "Gujranwala": {"lat": 32.1603, "lng": 74.1878},
}

def generate_cameras(city_name, center_lat, center_lng, count=10):
    cameras = []
    for i in range(count):
        # Generate random offset to simulate different locations in the city
        lat_offset = random.uniform(-0.05, 0.05)
        lng_offset = random.uniform(-0.05, 0.05)
        
        cam = {
            "lat": center_lat + lat_offset,
            "lng": center_lng + lng_offset,
            "address": f"{city_name} Camera Point {i+1}"
        }
        cameras.append(cam)
    return cameras

def populate():
    all_cameras = []
    print("Generating cameras for major cities in Pakistan...")
    
    for city, coords in cities.items():
        # Add 10-15 cameras per city
        city_cameras = generate_cameras(city, coords["lat"], coords["lng"], count=15)
        all_cameras.extend(city_cameras)
        
    print(f"Total cameras to add: {len(all_cameras)}")
    
    success_count = 0
    for cam in all_cameras:
        try:
            response = requests.post(f"{BASE_URL}/api/camera", json=cam)
            if response.status_code == 200:
                success_count += 1
                print(f"Added: {cam['address']}", end='\r')
        except Exception as e:
            print(f"Error: {e}")
            
    print(f"\nSuccessfully added {success_count} cameras across Pakistan!")

if __name__ == "__main__":
    populate()
