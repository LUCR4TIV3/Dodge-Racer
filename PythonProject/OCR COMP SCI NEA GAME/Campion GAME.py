import pygame
import random

pygame.init()

# Set up game screen
screen = pygame.display.set_mode((900, 650))
pygame.display.set_caption("Dodge Racer")

# Load images
icon = pygame.image.load('sport-car.png')
pygame.display.set_icon(icon)
background = pygame.image.load('game bg.png')
blurred_background = pygame.transform.smoothscale(background, (900, 650))  # resizing with smoothscale often gives a softer or less sharp look, which can feel like a blur
PlayerImg = pygame.image.load('main-car.png')
obstacle_img = pygame.image.load('cone.png')
obstacle_img = obstacle_img.convert_alpha() # prepares the image so it runs more smoothly in the game (faster blitting).

# Font settings
font = pygame.font.Font(None, 36)  # In-game text (small)
large_font = pygame.font.Font(None, 72)  # Larger text for menus

background_y = 0  # Track background position


# Player settings
PlayerX = 405 # starting x position of player
PlayerY = 550 # starting y position of the player
player_speed = 4 # This means each time the player moves, their position changes by 4 pixels per frame
player_dx = 0 # dx stands for change in  x (horizontally), how much a players position should change along the x-axis per frame
player_dy = 0 # dy stands for change in  y (vertically), how much a players position should change along the y-axis per frame

# If Right Arrow is pressed, player_dx = 4 → Moves right.
# If Left Arrow is pressed, player_dx = -4 → Moves left.
# If both or neither are pressed, player_dx = 0 → No movement.

# Obstacle settings
speed = 4 # This means that the obstacle moves at a speed of 4 pixels per frame
obstacles = [] # This creates an empty list that will store obstacle positions. Each obstacle is represented as a list containing its x and y coordinates,
min_horizontal_gap = 110  # Minimum gap between obstacles

def player(x, y):
    screen.blit(PlayerImg, (x, y))

# This function spawns obstacles in a way that ensures they are not too close to each other horizontally.
def generate_obstacle():
    max_attempts = 10 # This limits the number of attempts when trying to place an obstacle.
    for _ in range(max_attempts):  # Try 10 times to find a valid position
        x = random.randint(147, 753 - obstacle_img.get_width()) # Random horizontal position
        y = -obstacle_img.get_height() # Start above screen

        # Ensure new obstacle is not too close to existing ones
        too_close = any(abs(x - obs[0]) < min_horizontal_gap for obs in obstacles)
        # abs(x - obs[0]):  returns the absolute value, makes sure the value is positive so we know the correct horizontal distance between the new object and a previous one.
        # < min_horizontal_gap for obs in obstacles:  checks every x value of the obstacle to ensure the minimum horizontal gap is maintained
        if not too_close: # If spacing is okay, add the obstacle
            obstacles.append([x, y])
            break # Stop trying after finding a valid position

# Function to move obstacles
def move_obstacles():
    global speed
    for obstacle in obstacles.copy(): # Loop through a copy to avoid issues when removing items
        obstacle[1] += speed # Move obstacle down
        if obstacle[1] > 650: # Remove if it goes off-screen
            obstacles.remove(obstacle)

# Function to draw obstacles
def draw_obstacles():
    for obstacle in obstacles:
        screen.blit(obstacle_img, (obstacle[0], obstacle[1]))

# Function to check collision with smaller hit-boxes
def check_collision():
    # Define a much smaller hit-box for the player
    player_rect = pygame.Rect(
        PlayerX + 15,  # Move hit-box inside more
        PlayerY + 15,
        PlayerImg.get_width() - 30,  # Reduce width even more
        PlayerImg.get_height() - 30   # Reduce height even more
    )

    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(
            obstacle[0] + 10,  # Move hit-box inside more
            obstacle[1] + 10,
            obstacle_img.get_width() - 20,  # Reduce width more
            obstacle_img.get_height() - 20   # Reduce height more
        )

        if player_rect.colliderect(obstacle_rect):
            return True  # Collision detected

    return False  # No collision


def show_text(text, x, y, font_size=36):
    font_to_use = large_font if font_size > 36 else font
    render = font_to_use.render(text, True, (0, 25, 250))  # Text color is black
    screen.blit(render, (x, y))


def start_menu():
    while True:
        screen.blit(blurred_background, (0, 0))  # Blurred background
        show_text("Dodge Racer", 300, 200, 72)  # Larger text
        show_text("Press ENTER to Start", 200, 300, 48)  # Medium text
        pygame.display.update() # refreshing the screen so that the player sees the latest changes
        for event in pygame.event.get(): # checks all the actions the player or the system has made since the last time we checked
            if event.type == pygame.QUIT: # checks if the player closed the game window. If they did, the game will shut down.
                pygame.quit()
                exit() # these make sure the game shuts down properly when the player closes the window
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: # this checks if the player pressed the Enter key
                return # If the player pressed Enter, this makes the game move to the next step, like starting the game


def game_over_screen(score):
    while True: #  This starts a loop that keeps showing the game over screen until the player takes an action, like pressing a key to restart or quit
        screen.blit(blurred_background, (0, 0))  # Blurred background
        show_text("Game Over!", 320, 200, 72)
        show_text(f"Your score was: {score}", 250, 300, 48)
        show_text("Press ENTER to Play Again", 120, 400, 48) # shows all necessary game over text
        pygame.display.update() # refreshing the screen so that the player sees the latest changes
        for event in pygame.event.get(): # checks all the actions the player or the system has made since the last time we checked
            if event.type == pygame.QUIT: # checks if the player closed the game window. If they did, the game will shut down.
                pygame.quit()
                exit() # these make sure the game shuts down properly when the player closes the window
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: # This checks if the player presses the Enter key
                return #  If the Enter key is pressed, this causes the function to stop and return control, usually to start a new game


clock = pygame.time.Clock() # This creates a clock that controls how fast the game runs
start_menu() # This runs the start screen of the game

running = True # This starts the game and keeps it running. It ensures the game loop continues
start_time = pygame.time.get_ticks() # helps keep track of how long the game has been running
speed_increase_time = start_time # makes sure that the speed boost happens as soon as the game starts.  As time goes on, this number will be used to tell the game when 10 seconds have passed. When 10 seconds are up, the speed will speed up.

while running:
    screen.fill((0, 0, 0)) # Clear screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    player_dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed
    # keys is a dictionary-like structure that stores the state of all keys.
    # for example: keys[pygame.K_RIGHT] is 1 if the right arrow key is pressed, otherwise 0.
    player_dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * player_speed
    PlayerX += player_dx
    PlayerY += player_dy
    # since the variables PlayerX and PlayerY store the player's position, We add player_dx and player_dy to update the position.

    # Keep player inside boundaries
    PlayerX = max(147, min(753 - PlayerImg.get_width(), PlayerX))
    PlayerY = max(0, min(650 - PlayerImg.get_height(), PlayerY))

    # Generate obstacles randomly with spacing
    if random.random() < 0.05:  # 5% chance per frame
        generate_obstacle()
        if random.random() < 0.25:  # 25% chance to spawn an extra obstacle
            generate_obstacle()

    move_obstacles() # function updates the positions of the obstacles on the screen, making them move downwards based on the speed of the game
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000 # This line calculates how much time has passed since the game started.

    # Increase speed every 10 seconds
    if elapsed_time % 10 == 0 and pygame.time.get_ticks() - speed_increase_time >= 10000: # This line checks if 10 seconds have passed since the last speed increase.
        speed += 0.5 # the game speed is increased by 0.5
        speed_increase_time = pygame.time.get_ticks() # This line remembers the time when the game last got faster, so the game can wait 10 seconds before increasing the speed again.

    # Draw the background twice to create a scrolling effect
    screen.blit(background, (0, background_y))
    screen.blit(background, (0, background_y - 650))  # Draw a second background above the first one
    draw_obstacles()
    player(PlayerX, PlayerY)
    show_text(f"Score: {elapsed_time}", 750, 10)
    pygame.display.update()

    if check_collision():
        game_over_screen(elapsed_time)
        obstacles.clear()
        PlayerX, PlayerY = 405, 550
        start_time = pygame.time.get_ticks()
        speed = 4  # Reset speed after game over

    # Move background downward
    background_y += speed

    # Reset background position when it moves off-screen
    if background_y >= 650:
        background_y = 0

    clock.tick(60)

pygame.quit()
