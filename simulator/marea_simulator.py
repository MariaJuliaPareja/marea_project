#Imports
import json
import time
import random
import requests
import numpy as np
from datetime import datetime

#Class which will work as a simulation of the sensors 
class MAREASimulator:
    #Initiating the class
    def __init__(self):
        #Examples of devices, th
        self.devices = {
            "MAREA_001": {"lat": -12.0464, "lon": -77.0428, "name": "Lima Coast"},
            "MAREA_002": {"lat": -12.0500, "lon": -77.0500, "name": "Callao Bay"},
            "MAREA_003": {"lat": -12.0400, "lon": -77.0350, "name": "Miraflores"}
        }
        #Loading API
        self.api_url = "http://localhost:8000/api/sensor-data"
        #Default levels of contamination
        self.contamination_active = False
        self.contamination_device = None
    #Function to generate normal readings
    def generate_normal_reading(self, device_id):
        device = self.devices[device_id]
        
        return {
            "device_id": device_id,
            "timestamp": time.time(),
            "location": {
                "latitude": device["lat"] + random.uniform(-0.001, 0.001),
                "longitude": device["lon"] + random.uniform(-0.001, 0.001)
            },
            "sensors": { #Information as an example 
                "turbidity": round(random.uniform(1.0, 15.0), 1),
            },
            "system": { #Clasifications of the alerts as an example
                "battery_level": round(random.uniform(85, 100), 1),
                "threat_level": "NORMAL",
                "confidence": round(random.uniform(0.85, 0.95), 2)
            }
        }
    #Specifical function to readings of data of a contamination of the water
    def generate_contaminated_reading(self, device_id):
        device = self.devices[device_id]
        
        return {
            "device_id": device_id,
            "timestamp": time.time(),
            "location": {
                "latitude": device["lat"] + random.uniform(-0.001, 0.001),
                "longitude": device["lon"] + random.uniform(-0.001, 0.001)
            },
            "sensors": {
                "turbidity": round(random.uniform(20.0, 60.0), 1),
            },
            "system": {
                "battery_level": round(random.uniform(80, 95), 1),
                "threat_level": "CRITICAL" if random.random() > 0.3 else "HIGH",
                "confidence": round(random.uniform(0.80, 0.95), 2)
            }
        }
    #Sending a reading solicitude to the API
    def send_reading(self, reading):
        try:
            response = requests.post(self.api_url, json=reading, timeout=5)
            return response.status_code == 200
        except Exception as e:
            print(f"Error SENDING the solicitude: {e}")
            return False
    #Function to simulate a contamination
    def simulate_contamination(self, device_id, duration_minutes=30):
        print(f"Contamination number {device_id} for {duration_minutes} minutes")
        self.contamination_active = True
        self.contamination_device = device_id
        
        # Ending of the contamition 
        import threading 
        def end_contamination():
            time.sleep(duration_minutes * 60)
            self.contamination_active = False
            self.contamination_device = None
            print("End of similation of contamination")
        
        thread = threading.Thread(target=end_contamination)
        thread.daemon = True
        thread.start()
    #Running the simulation
    def run_simulation(self, interval=30):
        #
        print("Simulator started")
        print(f"Sending data each {interval} seconds")
        print("Dashboard: http://localhost:8000")
        print("=" * 50)
        
        while True:
            try:
                for device_id in self.devices:
                    #Deciding the type of lecture
                    if (self.contamination_active and 
                        self.contamination_device == device_id):
                        reading = self.generate_contaminated_reading(device_id)
                        icon = "🚨"
                    else:
                        reading = self.generate_contaminated_reading(device_id)
                        icon = "✅"
                    #Sending data
                    success = self.send_reading(reading)
                    #On consolee
                    device_name = self.devices[device_id]["name"]
                    threat = reading["system"]["threat_level"]
                    tr = reading["sensors"]["turbidity"]
                    
                    print(f"{icon} {device_id} ({device_name})")
                    print(f"   State: {threat} | Turbidity: {tr} ")
                    print(f"   Sending: {'Yes' if success else 'No'}")
                    print()
                
                print("-" * 30)
                time.sleep(interval) #Simulation the time of each sending-value
                
            except KeyboardInterrupt:
                print("\nStopped simulation")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)

   
    if __name__ == "__main__":
        main()