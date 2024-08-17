import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import os

class ObstacleDetector:
    def __init__(self, distance_threshold=2.0, angle_increment=10):
        self.distance_threshold = distance_threshold
        self.angle_increment = angle_increment
    
    def detect_obstacles(self, sensor_data):
        obstacles = []
        for i in range(len(sensor_data)):
            if i == 0:
                prev_distance = sensor_data[-1]
            else:
                prev_distance = sensor_data[i-1]
            
            curr_distance = sensor_data[i]
            
            if abs(curr_distance - prev_distance) > self.distance_threshold:
                angle = i * self.angle_increment
                obstacles.append((angle, curr_distance))
        
        return obstacles
    
    def nearest_obstacle(self, obstacles):
        if not obstacles:
            return None, None
        
        nearest = min(obstacles, key=lambda x: x[1])
        return nearest
    
    def process_sensor_data(self, sensor_data):
        obstacles = self.detect_obstacles(sensor_data)
        nearest = self.nearest_obstacle(obstacles)
        
        return {
            "obstacles": obstacles,
            "nearest_obstacle": nearest,
            "obstacle_count": len(obstacles)
        }

def visualize_sensor_data(sensor_data, obstacles, nearest_obstacle):
    angles = np.arange(0, len(sensor_data) * 10, 10)
    
    fig, ax = plt.subplots(subplot_kw=dict(projection='polar'))
    ax.plot(np.deg2rad(angles), sensor_data)
    
    obstacle_angles = [np.deg2rad(obs[0]) for obs in obstacles]
    obstacle_distances = [obs[1] for obs in obstacles]
    ax.scatter(obstacle_angles, obstacle_distances, c='red', s=50, label='Obstacles')
    
    if nearest_obstacle:
        nearest_angle, nearest_distance = nearest_obstacle
        ax.scatter(np.deg2rad(nearest_angle), nearest_distance, c='green', s=100, label='Nearest Obstacle')
    
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(0, max(sensor_data) + 1)
    ax.set_title("Obstacle Detection Visualization")
    ax.legend()
    
    plt.show()

def process_and_visualize(sensor_data, sample_index=0):
    detector = ObstacleDetector(distance_threshold=2.0)
    result = detector.process_sensor_data(sensor_data.iloc[sample_index])
    
    print(f"Processing sample {sample_index}:")
    print(f"Detected obstacles: {result['obstacle_count']}")
    print(f"Nearest obstacle: {result['nearest_obstacle']}")
    
    visualize_sensor_data(sensor_data.iloc[sample_index], result["obstacles"], result["nearest_obstacle"])

if __name__ == "__main__":
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to the CSV file
    csv_path = os.path.join(current_dir, 'sensor_data.csv')
    
    # Check if the file exists
    if not os.path.exists(csv_path):
        print(f"Error: The file 'sensor_data.csv' was not found in the directory: {current_dir}")
        print("Please make sure you've run 'generate_sensor_data.py' to create the sample data.")
        exit(1)

    # Load the sensor data
    sensor_data = pd.read_csv(csv_path)
    
    # Process and visualize the first sample
    process_and_visualize(sensor_data, sample_index=0)