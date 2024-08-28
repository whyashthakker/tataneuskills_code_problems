import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Car Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Car properties
car_width = 50
car_height = 100
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 10

# Obstacle properties
obstacle_width = 100
obstacle_height = 100
obstacle_speed = 5
obstacles = []

# Game properties
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)

def draw_car(x, y):
    pygame.draw.rect(window, BLUE, (x, y, car_width, car_height))

def draw_obstacle(x, y):
    pygame.draw.rect(window, RED, (x, y, obstacle_width, obstacle_height))

def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))

def game_over():
    game_over_text = font.render("Game Over!", True, WHITE)
    window.blit(game_over_text, (WIDTH // 2 - 70, HEIGHT // 2 - 18))
    pygame.display.update()
    pygame.time.wait(2000)

def main():
    global car_x, score
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= 5
        if keys[pygame.K_RIGHT] and car_x < WIDTH - car_width:
            car_x += 5

        # Create new obstacles
        if len(obstacles) < 3 and random.randint(1, 30) == 1:
            obstacle_x = random.randint(0, WIDTH - obstacle_width)
            obstacles.append([obstacle_x, -obstacle_height])

        # Move and remove obstacles
        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
            if obstacle[1] > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

        # Check for collisions
        for obstacle in obstacles:
            if car_y < obstacle[1] + obstacle_height and \
               car_y + car_height > obstacle[1] and \
               car_x < obstacle[0] + obstacle_width and \
               car_x + car_width > obstacle[0]:
                game_over()
                return

        # Draw everything
        window.fill((0, 0, 0))
        draw_car(car_x, car_y)
        for obstacle in obstacles:
            draw_obstacle(obstacle[0], obstacle[1])
        show_score()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()