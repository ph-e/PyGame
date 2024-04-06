import pygame
import random
from settings import BLUE, SCREEN_HEIGHT, SCREEN_WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.spawn_random()
        self.speed_x = random.randint(-5, 5)
        self.speed_y = random.randint(-5, 5)


    def spawn_random(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.speed_x *= -1
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            self.speed_y *= -1

        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.rect.y))
    