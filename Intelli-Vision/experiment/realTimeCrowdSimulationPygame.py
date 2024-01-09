import pygame
import random
import math

# Constants and variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CROWD_SIZE = 50
AVATAR_RADIUS = 5
AVATAR_SPEED = 2

# Color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Real-time Crowd Simulation')

# Function to calculate distance between points
def distance(point1, point2):
    return math.sqrt((point1 - point2)**2 + (point1 - point2)**2)

# Class representing each crowd member
class Avatar:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx, self.dy = self.get_random_direction()

    def get_random_direction(self):
        angle = random.random() * 2 * math.pi
        return AVATAR_SPEED * math.cos(angle), AVATAR_SPEED * math.sin(angle)

    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Check screen boundaries
        if self.x < AVATAR_RADIUS or self.x > SCREEN_WIDTH - AVATAR_RADIUS:
            self.x -= self.dx
            self.dx *= -1
        if self.y < AVATAR_RADIUS or self.y > SCREEN_HEIGHT - AVATAR_RADIUS:
            self.y -= self.dy
            self.dy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), AVATAR_RADIUS)

# Create a crowd
crowd = [Avatar(random.randint(AVATAR_RADIUS, SCREEN_WIDTH - AVATAR_RADIUS), random.randint(AVATAR_RADIUS, SCREEN_HEIGHT - AVATAR_RADIUS)) for _ in range(CROWD_SIZE)]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    for avatar in crowd:
        avatar.move()

    # Draw
    screen.fill(BLACK)
    for avatar in crowd:
        avatar.draw(screen)

    pygame.display.flip()

# Clean up
pygame.quit()
