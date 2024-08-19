import pygame
import sys
from enemies import Enemy
from tower import Tower



# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_width = 800
window_height = 600

# Create the window (display surface)
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pygame Window")

enemies = []

circle_radius = 10

tower = Tower(window_height, window_width)
bullets = []

spawn_rate = 2000  # Fire every 1000 ms (1 second)
last_enemy_time = pygame.time.get_ticks()  # Track time of last shot
number_of_enemies = 10

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()

    if current_time - Tower.last_shot_time >= Tower.fire_rate and len(enemies) != 0:
        bullet = tower.shoot(enemies)
        bullets.append(bullet)
        Tower.last_shot_time = current_time
        bullet.enemy.shots_fired += 1

    if current_time - last_enemy_time >= spawn_rate and number_of_enemies != 0:
        enemies.append(Enemy(window_height, window_width))
        last_enemy_time = current_time
        number_of_enemies -= 1


    screen.fill((0, 0, 255))  # RGB color (e.g., blue)

    for enemy in enemies:
        enemy_circle = pygame.draw.circle(screen, (0, 0, 0), enemy.movement(), circle_radius)
        enemy.circle_draw = enemy_circle

        if enemy.hp <= 0:
            enemies.remove(enemy)



    for bullet in bullets:
        bullet_circle = pygame.draw.circle(screen, (0, 0, 0), bullet.move_bullet(), bullet.radius)

        if bullet.check_collision():
            bullets.remove(bullet)
            bullet.hit()
#fix so the circle are part of the objects


    # Update the display
    pygame.display.flip()

    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()