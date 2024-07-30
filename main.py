import pygame
import sys
from enemies import enemy
from tower import Tower



#Initialize Pygame
pygame.init()

#Set the dimensions of the window
window_width = 800
window_height = 600

#Create the window (display surface)
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pygame Window")

attacker = enemy(window_height, window_width)
enemies = [attacker]

circle_radius = 10

tower = Tower(window_height, window_width)
bullets = []

draw_circle = False

#Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                draw_circle = True  # Set flag to draw the circle
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                draw_circle = False  # Clear flag to stop drawing the circle

    move = attacker.movement()

    screen.fill((0, 0, 255))  # RGB color (e.g., blue)

    pygame.draw.circle(screen, (0, 0, 0), move, circle_radius)
    # Fill the screen with a color (optional)

    if draw_circle:
        bullet = tower.shoot(enemies)
        bullets.append(bullet)

    for bullet in bullets:
        pygame.draw.circle(screen, (0, 0, 0), bullet.move_bullet(), bullet.radius)

    # Update the display
    pygame.display.flip()

    pygame.time.Clock().tick(60)

#Quit Pygame
pygame.quit()
sys.exit()