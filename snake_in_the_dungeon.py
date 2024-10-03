import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
SNAKE_SIZE = 10
FPS = 15
FONT = pygame.font.SysFont('Arial', 30)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Setup the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake in The Dungeon")

def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

def draw_food(food_pos):
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], SNAKE_SIZE, SNAKE_SIZE))

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(screen, BLUE, pygame.Rect(obs[0], obs[1], SNAKE_SIZE, SNAKE_SIZE))

def game_loop(level):
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
    score = 0
    direction = 'RIGHT'
    obstacles = [[random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                   random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE] for _ in range(5 + level)]

    # Initialize enemy positions
    enemy_pos = []
    if level > 1:
        enemy_count = 2 if level == 3 else 1  # Two enemies at level 3, one at level 2
        enemy_pos = [[random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                       random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE] for _ in range(enemy_count)]

    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'

        if direction == 'UP':
            snake_pos[1] -= SNAKE_SIZE
        elif direction == 'DOWN':
            snake_pos[1] += SNAKE_SIZE
        elif direction == 'LEFT':
            snake_pos[0] -= SNAKE_SIZE
        elif direction == 'RIGHT':
            snake_pos[0] += SNAKE_SIZE

        # Snake body growth
        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 10 * level
            food_pos = [random.randrange(1, (WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                        random.randrange(1, (HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
        else:
            snake_body.pop()

        # Collision detection
        if (snake_pos in obstacles or
            snake_pos[0] < 0 or snake_pos[0] >= WIDTH or
            snake_pos[1] < 0 or snake_pos[1] >= HEIGHT):
            break

        # Collision with enemies (Level 2 and 3)
        for pos in enemy_pos:
            pos[0] += random.choice([-SNAKE_SIZE, 0, SNAKE_SIZE])
            pos[1] += random.choice([-SNAKE_SIZE, 0, SNAKE_SIZE])
            pos[0] = max(0, min(WIDTH - SNAKE_SIZE, pos[0]))
            pos[1] = max(0, min(HEIGHT - SNAKE_SIZE, pos[1]))

            if snake_pos == pos:
                break

        screen.fill(BLACK)
        draw_snake(snake_body)
        draw_food(food_pos)
        draw_obstacles(obstacles)

        # lady bug enemies
        for pos in enemy_pos:
            pygame.draw.rect(screen, BLUE, pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))

        score_display = FONT.render(f'Score: {score}', True, WHITE)
        screen.blit(score_display, [0, 0])
        pygame.display.flip()
        clock.tick(FPS)

    return score


def main():
    for level in range(1, 4):
        score = game_loop(level)
        print(f'Game Over! Level {level} Score: {score}')
        pygame.time.wait(2000)

    pygame.quit()

if __name__ == "__main__":
    main()
