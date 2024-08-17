import numpy as np
import pandas as pd

def generate_sensor_data(num_samples=100, num_angles=36):
    data = []
    for _ in range(num_samples):
        # Generate base distances (clear path)
        base_distances = np.random.uniform(5, 20, num_angles)
        
        # Add random obstacles
        num_obstacles = np.random.randint(1, 4)
        for _ in range(num_obstacles):
            start_angle = np.random.randint(0, num_angles)
            width = np.random.randint(1, 5)
            obstacle_distance = np.random.uniform(1, 5)
            
            for i in range(width):
                angle = (start_angle + i) % num_angles
                base_distances[angle] = min(base_distances[angle], obstacle_distance)
        
        data.append(base_distances)
    
    # Create DataFrame
    columns = [f'angle_{i*10}' for i in range(num_angles)]
    df = pd.DataFrame(data, columns=columns)
    
    return df

if __name__ == "__main__":
    sensor_data = generate_sensor_data()
    sensor_data.to_csv('sensor_data.csv', index=False)
    print("Sample sensor data generated and saved to 'sensor_data.csv'")
    print(sensor_data.head())