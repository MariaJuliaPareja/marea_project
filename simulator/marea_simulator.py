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
        
   
    if __name__ == "__main__":
        main()