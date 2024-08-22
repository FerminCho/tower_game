import pygame
import sys
from enemies import Enemy
from tower import Tower
from base import Base



# Initialize Pygame
pygame.init()

# Set the dimensions of the window
window_width = 800
window_height = 600

# Create the window (display surface)
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pygame Window")

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()

base = Base(window_width, window_height)
all_sprites.add(base)

tower = Tower(window_height, window_width)
#all_sprites.add(tower)


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

    if current_time - Tower.last_shot_time >= Tower.fire_rate and len(enemy_sprites.sprites()) != 0:
        bullet = tower.shoot(enemy_sprites.sprites())
        all_sprites.add(bullet)
        bullet_sprites.add(bullet)
        Tower.last_shot_time = current_time
        bullet.enemy.shots_fired += 1

    if current_time - last_enemy_time >= spawn_rate and number_of_enemies != 0:
        enemy = Enemy(window_height, window_width)
        all_sprites.add(enemy)
        enemy_sprites.add(enemy)
        last_enemy_time = current_time
        number_of_enemies -= 1
    
    for enemy in enemy_sprites.sprites():
        if base.polygon_sprite_collision(enemy.rect):
            print('hit')
            all_sprites.remove(enemy)
            enemy_sprites.remove(enemy)


    screen.fill((0, 0, 255))  # RGB color (e.g., blue)

    all_sprites.update()
    all_sprites.draw(screen)

    for bullet in bullet_sprites.sprites():
        if pygame.sprite.spritecollide(bullet, enemy_sprites, False):
            bullet_sprites.remove(bullet)
            all_sprites.remove(bullet)
            bullet.hit()
    
    for enemy in enemy_sprites.sprites():
        if enemy.hp == 0:
            enemy_sprites.remove(enemy)
            all_sprites.remove(enemy)


    # Update the display
    pygame.display.flip()

    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()