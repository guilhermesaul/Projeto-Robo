import pygame
from config import LARGURA, ALTURA
from entidade import Entidade

# JOGADOR
class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 7)
        self.image.fill((0, 255, 0))  # verde
        self.vida = 5

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]: #cima        
            self.mover(0, -self.velocidade)#baixo
        if keys[pygame.K_s]:
            self.mover(0, self.velocidade)#baixo
        if keys[pygame.K_a]:
            self.mover(-self.velocidade, 0)#esquerda
        if keys[pygame.K_d]:
            self.mover(self.velocidade, 0)#direita

        # limites de tela
        self.rect.x = max(0, min(self.rect.x, LARGURA - 40))
        self.rect.y = max(0, min(self.rect.y, ALTURA - 40))

# TIRO (DO JOGADOR)
class Tiro(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 10)
        self.image.fill((255, 255, 0))  # amarelo

    def update(self):
        self.rect.y -= self.velocidade
        if self.rect.y < 0:
            self.kill()