import json
from queue import Queue
import threading
import time
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np

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

# Global variables for visualization
collected_data_count = 0
processed_data_count = 0
api_calls_count = 0

# Set up the visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
fig.suptitle("Vehicle Telematics Microservices Visualization", fontsize=16)

# Data Collection and Processing plot
bar_width = 0.35
index = np.arange(2)
collected_bar = ax1.bar(index[0], 0, bar_width, label='Collected Data')
processed_bar = ax1.bar(index[1], 0, bar_width, label='Processed Data')
ax1.set_ylabel('Number of Data Points')
ax1.set_title('Data Collection and Processing')
ax1.set_xticks(index)
ax1.set_xticklabels(('Collected', 'Processed'))
ax1.legend()

# API Calls plot
api_calls_plot, = ax2.plot([], [], label='API Calls')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Number of API Calls')
ax2.set_title('API Gateway Activity')
ax2.legend()

# Animation update function
def update(frame):
    global collected_data_count, processed_data_count, api_calls_count

    # Update data counts
    collected_data_count += 1
    if frame % 2 == 0:  # Simulate processing every 2 seconds
        processed_data_count += 1
    if frame % 5 == 0:  # Simulate API call every 5 seconds
        api_calls_count += 1

    # Update Data Collection and Processing plot
    collected_bar[0].set_height(collected_data_count)
    processed_bar[0].set_height(processed_data_count)
    ax1.set_ylim(0, max(collected_data_count, processed_data_count) + 5)

    # Update API Calls plot
    api_calls_plot.set_data(range(frame+1), [api_calls_count] * (frame+1))
    ax2.set_xlim(0, frame)
    ax2.set_ylim(0, api_calls_count + 1)

    return collected_bar, processed_bar, api_calls_plot

# Set up and run the services
data_collector = DataCollectionService()
data_processor = DataProcessingService()
api_gateway = APIGateway(data_processor)

# Start the services in separate threads
threading.Thread(target=data_collector.collect_data, daemon=True).start()
threading.Thread(target=data_processor.process_data, daemon=True).start()

# Create the animation
ani = FuncAnimation(fig, update, frames=range(60), interval=1000, repeat=False)

plt.tight_layout()
plt.show()

print("\nSimulation complete.")
