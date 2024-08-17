### Problem Statement:
Implement a simple reinforcement learning algorithm to train an autonomous vehicle to navigate a basic road environment. The goal is to teach the car to stay in its lane and avoid obstacles.

### Requirements:
1. Create a simple 2D environment representing a road with lanes and obstacles.
2. Implement a Q-learning algorithm for the car to learn optimal actions.
3. Define states, actions, and rewards appropriate for the driving task.
4. Train the model and demonstrate improved performance over time.

### Solution:

import numpy as np
import matplotlib.pyplot as plt

class AutonomousCar:
    def __init__(self, states, actions, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.q_table = np.zeros((states, actions))
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(self.q_table.shape[1])  # Explore
        else:
            return np.argmax(self.q_table[state, :])  # Exploit

    def learn(self, state, action, reward, next_state):
        predict = self.q_table[state, action]
        target = reward + self.discount_factor * np.max(self.q_table[next_state, :])
        self.q_table[state, action] += self.learning_rate * (target - predict)

class DrivingEnvironment:
    def __init__(self, size=5):
        self.size = size
        self.actions = ['left', 'stay', 'right']
        self.reset()

    def reset(self):
        self.car_position = self.size // 2
        self.obstacle_position = np.random.randint(0, self.size)
        return self.car_position

    def step(self, action):
        # Move car
        if action == 0:  # left
            self.car_position = max(0, self.car_position - 1)
        elif action == 2:  # right
            self.car_position = min(self.size - 1, self.car_position + 1)

        # Check for collision or successful navigation
        if self.car_position == self.obstacle_position:
            reward = -10  # Collision
            done = True
        elif self.car_position == self.size // 2:
            reward = 1  # Stayed in the middle lane
            done = False
        else:
            reward = -1  # Moved away from middle lane
            done = False

        return self.car_position, reward, done

def train(episodes=1000):
    env = DrivingEnvironment()
    car = AutonomousCar(env.size, len(env.actions))
    rewards = []

    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            action = car.choose_action(state)
            next_state, reward, done = env.step(action)
            car.learn(state, action, reward, next_state)
            state = next_state
            total_reward += reward

        rewards.append(total_reward)

    return car, rewards

# Train the model
trained_car, reward_history = train()

# Plot the rewards
plt.plot(reward_history)
plt.title('Reward History')
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.show()

# Test the trained model
env = DrivingEnvironment()
state = env.reset()
done = False
while not done:
    action = trained_car.choose_action(state)
    state, reward, done = env.step(action)
    print(f"Car Position: {state}, Reward: {reward}")

print("Final Q-table:")
print(trained_car.q_table)