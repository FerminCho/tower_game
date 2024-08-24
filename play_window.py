import pygame
from base import Base
from enemies import Enemy
from tower import Tower

def run_game(screen):
    all_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()


    screen_surface = pygame.display.get_surface()
    base = Base(screen_surface.get_width(), screen_surface.get_height())
    all_sprites.add(base)

    tower = Tower(screen_surface.get_width(), screen_surface.get_height())
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

        screen.fill((0, 0, 255))  # RGB color (e.g., blue)

        all_sprites.update()
        all_sprites.draw(screen)

        for bullet in bullet_sprites.sprites():
            if bullet.check_collision() or bullet.enemy not in enemy_sprites.sprites():
                bullet_sprites.remove(bullet)
                all_sprites.remove(bullet)
                bullet.hit()
        
        for enemy in enemy_sprites.sprites():
            if base.check_collision(enemy):
                all_sprites.remove(enemy)
                enemy_sprites.remove(enemy)
                base.hp -= 1
                if base.hp == 0:
                    running = False

            if enemy.hp == 0:
                enemy_sprites.remove(enemy)
                all_sprites.remove(enemy)


        # Update the display
        pygame.display.flip()

        pygame.time.Clock().tick(60)