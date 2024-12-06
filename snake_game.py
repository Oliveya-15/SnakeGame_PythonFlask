import pygame
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Set screen dimensions
WIDTH, HEIGHT = 600, 400

# Define colors
WHITE = (255, 255, 255)
GREEN = (76, 187, 23)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
LIGHT_CORAL = (254, 218, 218)

# Define the size of each block in the grid
BLOCK_SIZE = 20

# Define directions
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Set font for displaying score
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)  # Large font for game over text
small_font = pygame.font.Font(None, 28)  # Smaller font for buttons

# Load sound effects with fallback
def load_sound(filename, default=None):
    try:
        return pygame.mixer.Sound(filename)
    except pygame.error:
        print(f"Sound file {filename} not found, using default.")
        return default

level_click_sound = load_sound("button.mp3")
food_eat_sound = load_sound("eat.mp3")
game_over_sound = load_sound("gameover.mp3")
direction_change_sound = load_sound("move.mp3")
background_music = "music.mp3"  # Background music file

# Load background images with fallback
def load_image(filename, default=None):
    try:
        return pygame.image.load(filename)
    except pygame.error:
        print(f"Image file {filename} not found, using default.")
        return default

game_background = load_image("backimg.jpg", pygame.Surface((WIDTH, HEIGHT)))
score_background = load_image("lastimg.jpeg", pygame.Surface((WIDTH, HEIGHT)))

# Initialize game variables
snake = [(WIDTH // 2, HEIGHT // 2)]
direction = RIGHT
food = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
        random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
score = 0

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Function to handle collision with boundary
def check_boundary_collision():
    if snake[0][0] < 0 or snake[0][0] >= WIDTH or snake[0][1] < 0 or snake[0][1] >= HEIGHT:
        return True
    return False

# Function to handle collision with food
def check_food_collision():
    if snake[0] == food:
        return True
    return False

# Function to handle collision with self
def check_self_collision():
    if snake[0] in snake[1:]:
        return True
    return False

# Function to generate new food
def generate_food():
    return (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
            random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)

# Function to display game over screen
def game_over():
    if game_over_sound:
        pygame.mixer.Sound.play(game_over_sound)
    screen.blit(score_background, (0, 0))
    
    # Display "Game Over" text
    game_over_text = large_font.render("Game Over!", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    
    # Display score text
    score_text = font.render("Your Score: " + str(score), True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 30))
    
    # Display "Play Again" and "Quit" buttons
    play_again_button = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 + 50, 120, 50)
    quit_button = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2 + 50, 100, 50)
    pygame.draw.rect(screen, GREEN, play_again_button)    
    pygame.draw.rect(screen, RED, quit_button)
    play_again_text =small_font.render("Play Again", True, WHITE)  # Smaller font size and white color
    quit_text = font.render("Quit", True, BLACK)
    screen.blit(play_again_text, (WIDTH // 2 - 130 + (120 - play_again_text.get_width()) // 2, HEIGHT // 2 + 60))
    screen.blit(quit_text, (WIDTH // 2 + 10 + (100 - quit_text.get_width()) // 2, HEIGHT // 2 + 60))
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    start_game(clock.get_fps())  # Restart the game with the same speed
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()

# Function to start the snake game
def start_game(speed):
    global snake, direction, food, score, clock
    snake = [(WIDTH // 2, HEIGHT // 2)]
    direction = RIGHT
    food = (random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
            random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE)
    score = 0
    clock = pygame.time.Clock()

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                    if direction_change_sound:
                        pygame.mixer.Sound.play(direction_change_sound)
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                    if direction_change_sound:
                        pygame.mixer.Sound.play(direction_change_sound)
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                    if direction_change_sound:
                        pygame.mixer.Sound.play(direction_change_sound)
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT
                    if direction_change_sound:
                        pygame.mixer.Sound.play(direction_change_sound)

        # Move the snake
        x, y = snake[0]
        if direction == UP:
            y -= BLOCK_SIZE
        elif direction == DOWN:
            y += BLOCK_SIZE
        elif direction == LEFT:
            x -= BLOCK_SIZE
        elif direction == RIGHT:
            x += BLOCK_SIZE

        # Update snake position
        snake.insert(0, (x, y))

        # Check for collision with boundary or self
        if check_boundary_collision() or check_self_collision():
            running = False

        # Check for collision with food
        if check_food_collision():
            if food_eat_sound:
                pygame.mixer.Sound.play(food_eat_sound)
            score += 1
            food = generate_food()
        else:
            snake.pop()

        # Draw background
        screen.blit(game_background, (0, 0))

        # Draw snake with borders
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, DARK_GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE), 2)

        # Draw food with border
        pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, BROWN, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE), 2)

        # Display score
        score_text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(speed)

    # Stop background music and show game over screen
    pygame.mixer.music.stop()
    game_over()

# Main loop
if __name__ == "__main__":
    clock = pygame.time.Clock()
    pygame.mixer.music.load(background_music)  # Load background music
    pygame.mixer.music.play(-1, 0.0)  # Loop the background music

    start_game(10)
    pygame.quit()
