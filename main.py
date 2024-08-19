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

all_sprites = pygame.sprite.Group()
enemy = Enemy(window_height, window_width)
all_sprites.add(enemy)
enemies = []

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

    #if current_time - Tower.last_shot_time >= Tower.fire_rate and len(enemies) != 0:
    #    bullet = tower.shoot(enemies)
    #    bullets.append(bullet)
    #    Tower.last_shot_time = current_time
    #    bullet.enemy.shots_fired += 1

    #if current_time - last_enemy_time >= spawn_rate and number_of_enemies != 0:
    #    all_sprites.add(Enemy(window_height, window_width))
    #    last_enemy_time = current_time
    #    number_of_enemies -= 1


    screen.fill((0, 0, 255))  # RGB color (e.g., blue)

    all_sprites.update()
    all_sprites.draw(screen)



    #for bullet in bullets:
    #    bullet_circle = pygame.draw.circle(screen, (0, 0, 0), bullet.move_bullet(), bullet.radius)

    #    if bullet.check_collision():
    #        bullets.remove(bullet)
    #        bullet.hit()


    # Update the display
    pygame.display.flip()

    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()