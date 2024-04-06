import pygame
import random
import sys
from units.player import Player
from units.goal import Goal
from units.enemy import Enemy
from settings import MAX_COUNT_ENEMY, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, VICTORY, LOSE, VOLUME
from utils import draw_text


pygame.init()
# Loading sound
victory_sound = pygame.mixer.Sound(VICTORY)
lose_sound = pygame.mixer.Sound(LOSE)
victory_sound.set_volume(VOLUME)
lose_sound.set_volume(VOLUME)

# Creating the main window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("labyrinth")

# Creation units
all_sprites = pygame.sprite.Group()
player = Player()
goal = Goal()
enemies = []

def initializeUnits():
    all_sprites.add(player, goal)
    count_enemies = random.randint(1, MAX_COUNT_ENEMY)
    for i in range(count_enemies):
        enemies.append(Enemy())
    all_sprites.add(enemies)

# Moving to a new level, creating new units
def nextLevel():
    global goal
    all_sprites.remove(goal)
    all_sprites.remove(enemies)
    enemies.clear()
    goal = Goal()
    initializeUnits()

# Treatment of the lesion
def gameOver():
    screen.fill(BLACK)
    draw_text(pygame, screen, "Игра окончена!", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    draw_text(pygame, screen, "Нажмите R для рестарта или Q для выхода", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Начать заново
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Main function with game logic
def startGame():
    initializeUnits()
    # Main game loop
    running = True
    while running:
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player Control
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -5
        if keys[pygame.K_RIGHT]:
            dx = 5
        if keys[pygame.K_UP]:
            dy = -5
        if keys[pygame.K_DOWN]:
            dy = 5

        # Game update
        player.update(dx, dy)
        for enemy in enemies:
            enemy.update()

        # Level completion check
        if pygame.sprite.collide_rect(player, goal):
            victory_sound.play()
            draw_text(pygame, screen, "Уровень пройден!", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
            pygame.display.flip()
            pygame.time.delay(2000)  # Задержка перед переходом на следующий уровень
            nextLevel()

        # In the event of a collision with an enemy
        if pygame.sprite.spritecollideany(player, enemies):
            lose_sound.play()
            if gameOver():
                nextLevel()
            else:
                running = False


        # Rendering
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()

        # Delay
        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()
