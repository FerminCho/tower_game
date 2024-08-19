import pygame
from enemies import Enemy


# Initialize Pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((800, 600))

# Create sprite groups
all_sprites = pygame.sprite.Group()

# Define a simple sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width, self.height = 50, 50

        #self.object_x, self.object_y = self.set_start_position(window_width, window_height)

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))  # Red color
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, 50)

    def update(self):
        # Move the player sprite
        self.rect.x += 0.5
        if self.rect.x > 800:
            self.rect.x = 0

# Create and add sprites to the group
player = Enemy(600, 800)
all_sprites.add(player)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update all sprites
    all_sprites.update()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw all sprites
    all_sprites.draw(screen)

    # Update the display
    pygame.display.flip()

pygame.quit()
