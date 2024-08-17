import pandas as pd
import numpy as np

# Set a random seed for reproducibility
np.random.seed(42)

# Generate sample data
n_samples = 100
weights = np.random.randint(1000, 2500, n_samples)  # Weight in kg
base_efficiency = 5 + (weights - 1000) * 0.005  # Base L/100km
noise = np.random.normal(0, 0.5, n_samples)  # Add some noise
efficiency = np.clip(base_efficiency + noise, 4, 15)  # Ensure realistic range

# Create a DataFrame
df = pd.DataFrame({
    'weight_kg': weights,
    'fuel_efficiency_l_100km': np.round(efficiency, 2)
})

# Add some categorical features for extra information
df['manufacturer'] = np.random.choice(['Tata', 'Mahindra', 'Maruti Suzuki', 'Hyundai', 'Honda'], n_samples)
df['model_year'] = np.random.randint(2015, 2024, n_samples)

# Sort and reset index
df = df.sort_values('weight_kg').reset_index(drop=True)

# Display the first few rows
print(df.head())

# Save to CSV
df.to_csv('car_fuel_efficiency_data.csv', index=False)
print("\nDataset saved to 'car_fuel_efficiency_data.csv'")