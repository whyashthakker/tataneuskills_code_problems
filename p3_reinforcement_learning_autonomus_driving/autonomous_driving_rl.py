import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

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

def visualize_environment(ax, env, car_position, action=None, reward=None, total_reward=0):
    ax.clear()
    road = ['_'] * env.size
    road[env.obstacle_position] = 'X'
    road[car_position] = 'C'
    
    ax.set_xlim(-0.5, env.size - 0.5)
    ax.set_ylim(-1, 1)
    ax.set_yticks([])
    ax.set_xticks(range(env.size))
    ax.set_xticklabels(road)
    
    ax.axhline(y=0, color='k', linestyle='-', linewidth=2)
    ax.plot(car_position, 0, 'bo', markersize=20, label='Car')
    ax.plot(env.obstacle_position, 0, 'rx', markersize=20, label='Obstacle')
    
    if action is not None:
        ax.set_title(f"Action: {env.actions[action]}", fontsize=16)
    if reward is not None:
        color = 'green' if reward > 0 else 'red'
        ax.text(env.size/2, 0.5, f"Reward: {reward}", ha='center', va='center', fontsize=16, color=color)
    ax.text(env.size/2, -0.5, f"Total Reward: {total_reward}", ha='center', va='center', fontsize=16)
    
    ax.legend(loc='upper left')

def train_and_visualize(episodes=10, delay=1):
    env = DrivingEnvironment()
    car = AutonomousCar(env.size, len(env.actions))
    rewards = []

    fig, ax = plt.subplots(figsize=(12, 6))
    plt.ion()  # Turn on interactive mode

    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False
        step = 0

        print(f"Episode {episode + 1}")
        visualize_environment(ax, env, state)
        plt.pause(delay)

        while not done:
            action = car.choose_action(state)
            next_state, reward, done = env.step(action)
            car.learn(state, action, reward, next_state)
            
            step += 1
            total_reward += reward
            visualize_environment(ax, env, next_state, action, reward, total_reward)
            plt.pause(delay)
            
            state = next_state

        rewards.append(total_reward)
        print(f"Episode {episode + 1} finished. Total reward: {total_reward}")
        plt.pause(delay)

    plt.ioff()  # Turn off interactive mode
    plt.close()

    return car, rewards

# Train the model with visualization
trained_car, reward_history = train_and_visualize(episodes=5, delay=1)

# Plot the rewards
plt.figure(figsize=(10, 5))
plt.plot(reward_history)
plt.title('Reward History')
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.show()

print("\nFinal Q-table:")
print(trained_car.q_table)