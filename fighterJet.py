# Importing the libraries
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jet Plane Bombing Game")

# Load background image and music
background_img = pygame.image.load("residential_area.jpg")
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Load images
jet_img = pygame.image.load("jet_plane.png")
jet_img = pygame.transform.scale(jet_img, (100, 50))
bomb_img = pygame.image.load("bomb.png")
bomb_img = pygame.transform.scale(bomb_img, (40, 40))
blast_img = pygame.image.load("explosion.png")
blast_img = pygame.transform.scale(blast_img, (70, 70))  # Increased blast size slightly
house_imgs = [pygame.image.load("house.png"), pygame.image.load("house.png"),
              pygame.image.load("house.png")]
house_imgs = [pygame.transform.scale(house, (70, 70)) for house in house_imgs]  # Resize houses

# Set up variables
jet_x = -100
jet_y = 50  # Fixed y-coordinate for the jet
bombs = []  # List to store bomb positions and states
houses = []  # List to store house positions
score = 0
game_over = False

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

# Timer variables
time_remaining = 10 * 60 
timer_font = pygame.font.Font(None, 48)

# Function to generate bombs
def generate_bombs():
    global bombs
    bombs.append({"position": (jet_x + 50, jet_y + 50), "state": "falling",
                  "blast_timer": 0})  # Generate bomb at the current position of the jet


# Function to generate houses
def generate_houses():
    global houses
    num_bottom_houses = 4
    bottom_house_width = screen_width // num_bottom_houses

    for i in range(num_bottom_houses):
        house_x = i * bottom_house_width + (bottom_house_width - 70) // 2  # Center the houses horizontally
        house_y = screen_height - 100  # Position the houses at the bottom of the screen
        houses.append(
            {"position": (house_x, house_y), "image": random.choice(house_imgs)})  # Randomly select house image


# Main game loop
running = True
while running:
    screen.blit(background_img, (0, 0))  # Draw background image

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Drop bomb when spacebar is pressed
                generate_bombs()

    # Update jet position
    jet_x += 5
    if jet_x > screen_width:
        jet_x = -100

    # Generate houses if not already generated
    if not houses:
        generate_houses()

    # Update bomb positions and states
    for bomb in bombs:
        if bomb["state"] == "falling":
            bomb["position"] = (bomb["position"][0], bomb["position"][1] + 10)  # Update bomb position
            for house in houses:
                if house["position"][0] < bomb["position"][0] < house["position"][0] + 100 and house["position"][1] < \
                        bomb["position"][1] < house["position"][1] + 100:
                    bomb["state"] = "exploded"
                    bomb["blast_timer"] = pygame.time.get_ticks()  # Start blast timer
                    score += 1
                    houses.remove(house)  # Remove the house when bombed

    # Draw images
    for house in houses:
        screen.blit(house["image"], house["position"])  # Draw houses first

    for bomb in bombs:
        if bomb["state"] == "falling":
            screen.blit(bomb_img, bomb["position"])
        elif bomb["state"] == "exploded":
            # Adjust blast position to be on top of the house
            screen.blit(blast_img, (bomb["position"][0] - 10, bomb["position"][1] - 10))
            if pygame.time.get_ticks() - bomb["blast_timer"] >= 1000:  # Display blast for 1 second
                bombs.remove(bomb)  # Remove the bomb after 1 second

    screen.blit(jet_img, (jet_x, jet_y))  # Draw jet after everything else

    # Display score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Display timer
    if not game_over:
        time_text = timer_font.render("Time: " + str(time_remaining // 60) + ":" + str(time_remaining % 60).zfill(2), True, (255, 255, 255))
        screen.blit(time_text, (screen_width - 200, 10))

    # Update timer
    if not game_over:
        if time_remaining > 0:
            time_remaining -= 1
        else:
            game_over = True

    # Display "Game Over" if all houses are destroyed or time runs out
    if game_over:
        game_over_text = font.render("Game Over", True, (255, 255, 255))
        screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2))
        running = False  # Stop the game loop

    pygame.display.flip()
    clock.tick(30)

# Quit Pygame
pygame.quit()
sys.exit()
