import requests
import json

BASE_URL = "http://0.0.0.0:8000"

import random

cameras = []

cities = [
    {"name": "Lahore", "lat": 31.5204, "lng": 74.3587},
    {"name": "Karachi", "lat": 24.8607, "lng": 67.0011},
    {"name": "Islamabad", "lat": 33.6844, "lng": 73.0479},
    {"name": "Peshawar", "lat": 34.0151, "lng": 71.5249},
    {"name": "Quetta", "lat": 30.1798, "lng": 66.9750},
    {"name": "Multan", "lat": 30.1575, "lng": 71.5249},
    {"name": "Faisalabad", "lat": 31.4504, "lng": 73.1350}
]

for city in cities:
    # Special handling for Karachi to show "all working"
    if city["name"] == "Karachi":
        count = 20
        forced_status = "active"
    else:
        count = 5
        forced_status = None

    for i in range(count):
        # Add slight random offset to coordinates
        lat_offset = random.uniform(-0.08, 0.08)
        lng_offset = random.uniform(-0.08, 0.08)
        
        status = forced_status if forced_status else random.choice(["active", "inactive"])
        light = random.choice(["red", "yellow", "green"])
        speed = random.choice([40, 50, 60, 80, 100])
        
        cameras.append({
            "lat": city["lat"] + lat_offset,
            "lng": city["lng"] + lng_offset,
            "address": f"{city['name']} Camera #{i+1}",
            "light_status": light,
            "status": status,
            "speed_limit": speed
        })

def add_cameras():
    print(f"Adding {len(cameras)} dummy cameras to {BASE_URL}...")
    for cam in cameras:
        try:
            response = requests.post(f"{BASE_URL}/api/camera", json=cam)
            if response.status_code == 200:
                print(f"Successfully added camera at {cam['address']}")
            else:
                print(f"Failed to add camera: {response.text}")
        except Exception as e:
            print(f"Error connecting to server: {e}")

if __name__ == "__main__":
    add_cameras()
