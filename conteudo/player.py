import pygame
from config import ALTURA, LARGURA
from entidade import Entidade

# JOGADOR
class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 7)
        self.image.fill((0, 255, 0))  # verde
        self.vida = 5
        self.velocidade_base = 7
        self.velocidade = self.velocidade_base
        self.velocidade_timer = 0
        self.tiro_triplo_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:  # cima
            self.mover(0, -self.velocidade) 
        if keys[pygame.K_s]:
            self.mover(0, self.velocidade)  # baixo
        if keys[pygame.K_a]:
            self.mover(-self.velocidade, 0)  # esquerda
        if keys[pygame.K_d]:
            self.mover(self.velocidade, 0)  # direita

        # limites de tela
        self.rect.x = max(0, min(self.rect.x, LARGURA - 40))
        self.rect.y = max(0, min(self.rect.y, ALTURA - 40))

        # timers de efeitos temporários
        if self.velocidade_timer > 0:
            self.velocidade_timer -= 1
            if self.velocidade_timer == 0:
                self.velocidade = self.velocidade_base

        if self.tiro_triplo_timer > 0:
            self.tiro_triplo_timer -= 1

    @property
    def tiro_triplo_ativo(self) -> bool:
        return self.tiro_triplo_timer > 0

    def aplicar_powerup(self, tipo: str):
        if tipo == "velocidade":
            self.velocidade_timer += 600 
            self.velocidade = self.velocidade_base + 4
        elif tipo == "vida":
            self.vida = min(self.vida + 1, 9)
        elif tipo == "tiro_triplo":
            self.tiro_triplo_timer += 600
        else:
            raise ValueError(f"Power-up desconhecido: {tipo}")

# TIRO (DO JOGADOR)
class Tiro(Entidade):
    def __init__(self, x, y, dx=0):
        super().__init__(x, y, 10)
        self.dx = dx
        self.image.fill((255, 255, 0))  # amarelo

    def update(self):
        self.rect.x += self.dx
        self.rect.y -= self.velocidade
        if (
            self.rect.y < -20
            or self.rect.x < -20
            or self.rect.x > LARGURA + 20
        ):
            self.kill()
