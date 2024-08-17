## Problem 4: Microservice Architecture for Vehicle Telematics

### Problem Statement:
Design and implement a basic microservice architecture for a vehicle telematics system. The system should collect data from various sensors, process it, and provide insights about the vehicle's performance and health.

### Requirements:
1. Implement at least three microservices: Data Collection, Data Processing, and API Gateway.
2. Use a message queue for communication between services.
3. Implement basic endpoints for retrieving vehicle health and performance metrics.
4. Ensure the architecture is scalable and loosely coupled.

### Solution:

```python
# Note: This is a simplified implementation. In a real-world scenario, you'd use proper web frameworks and message brokers.

import json
from queue import Queue
import threading
import time
import random

# Simulated message queue
message_queue = Queue()

class DataCollectionService:
    def collect_data(self):
        while True:
            data = {
                "vehicle_id": random.randint(1000, 9999),
                "speed": random.uniform(0, 120),
                "fuel_level": random.uniform(0, 100),
                "engine_temp": random.uniform(50, 120),
                "timestamp": time.time()
            }
            message_queue.put(json.dumps(data))
            time.sleep(1)  # Collect data every second

class DataProcessingService:
    def __init__(self):
        self.vehicle_data = {}

    def process_data(self):
        while True:
            if not message_queue.empty():
                data = json.loads(message_queue.get())
                vehicle_id = data["vehicle_id"]
                if vehicle_id not in self.vehicle_data:
                    self.vehicle_data[vehicle_id] = []
                self.vehicle_data[vehicle_id].append(data)
                # Keep only the last 60 data points (1 minute of data)
                self.vehicle_data[vehicle_id] = self.vehicle_data[vehicle_id][-60:]

    def get_vehicle_health(self, vehicle_id):
        if vehicle_id not in self.vehicle_data:
            return None
        latest_data = self.vehicle_data[vehicle_id][-1]
        health_status = "Good"
        if latest_data["engine_temp"] > 100:
            health_status = "Warning: High Engine Temperature"
        elif latest_data["fuel_level"] < 10:
            health_status = "Warning: Low Fuel"
        return {
            "vehicle_id": vehicle_id,
            "health_status": health_status,
            "last_updated": latest_data["timestamp"]
        }

    def get_vehicle_performance(self, vehicle_id):
        if vehicle_id not in self.vehicle_data:
            return None
        data = self.vehicle_data[vehicle_id]
        avg_speed = sum(d["speed"] for d in data) / len(data)
        return {
            "vehicle_id": vehicle_id,
            "average_speed": avg_speed,
            "data_points": len(data)
        }

class APIGateway:
    def __init__(self, data_processor):
        self.data_processor = data_processor

    def get_vehicle_health(self, vehicle_id):
        return self.data_processor.get_vehicle_health(vehicle_id)

    def get_vehicle_performance(self, vehicle_id):
        return self.data_processor.get_vehicle_performance(vehicle_id)

# Set up and run the services
data_collector = DataCollectionService()
data_processor = DataProcessingService()
api_gateway = APIGateway(data_processor)

# Start the services in separate threads
threading.Thread(target=data_collector.collect_data, daemon=True).start()
threading.Thread(target=data_processor.process_data, daemon=True).start()

# Simulate API calls
time.sleep(10)  # Wait for some data to be collected
print(api_gateway.get_vehicle_health(1234))
print(api_gateway.get_vehicle_performance(1234))
```

### Explanation:
This problem implements a basic microservice architecture for a vehicle telematics system. It consists of three main components:

1. Data Collection Service: Simulates collecting data from vehicle sensors.
2. Data Processing Service: Processes the collected data and maintains a record for each vehicle.
3. API Gateway: Provides endpoints for retrieving vehicle health and performance metrics.

The services communicate through a simulated message queue. This architecture demonstrates the principles of microservices, including loose coupling and scalability.

```

Explanation of what's happening in this visualization:

1. Microservice Architecture:
   - The code implements a basic microservice architecture for a vehicle telematics system.
   - There are three main components: Data Collection Service, Data Processing Service, and API Gateway.

2. Data Collection Service:
   - Simulates collecting data from vehicles every second.
   - Generates random data for vehicle_id, speed, fuel_level, and engine_temp.
   - Sends this data to a message queue (simulated by a Python Queue).

3. Data Processing Service:
   - Continuously reads data from the message queue.
   - Processes and stores the data for each vehicle.
   - Maintains a rolling window of the last 60 data points for each vehicle.

4. API Gateway:
   - Provides an interface to retrieve vehicle health and performance data.
   - Can be called to get the latest health status or average performance metrics for a specific vehicle.

5. Visualization:
   - The top graph shows the number of data points collected and processed over time.
   - The bottom graph shows the number of API calls made over time.

6. Real-time Updates:
   - The visualization updates every second to show the ongoing activity in the system.
   - You can see the collected data increasing faster than the processed data, simulating real-world scenarios where processing might be slower than data collection.
   - API calls are simulated to occur less frequently than data collection and processing.

To use this script:

1. Save it as `visual_vehicle_telematics.py` in VS Code.
2. Ensure you have the required libraries:
   ```
   pip install matplotlib numpy
   ```
3. Run the script:
   ```
   python visual_vehicle_telematics.py
   ```

During a presentation or call, you can explain:
- How data flows through the system from collection to processing.
- The difference between data collection and processing rates.
- How the API Gateway provides access to processed data.
- The scalability of this architecture for handling multiple vehicles simultaneously.

This visualization helps to illustrate the concept of microservices and how they interact in a vehicle telematics system, making it more engaging and understandable for viewers.