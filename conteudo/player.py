import os
import pygame
from config import ALTURA, LARGURA
from entidade import Entidade

CAMINHO_NAVE_PLAYER = os.path.join(
    os.path.dirname(__file__),
    "assets",
    "images",
    "nave_player.png",
)
TAMANHO_NAVE_PLAYER = (100, 118)

# JOGADOR
class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 7)
        sprite = pygame.image.load(CAMINHO_NAVE_PLAYER).convert_alpha()
        self.image = pygame.transform.scale(sprite, TAMANHO_NAVE_PLAYER)
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.inflate(-20, -20)

        self.vida = 500
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
        self.rect.x = max(0, min(self.rect.x, LARGURA - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ALTURA - self.rect.height))
        self.hitbox.center = self.rect.center

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
            self.velocidade_timer = 600 
            self.velocidade = self.velocidade_base + 4
        elif tipo == "vida":
            self.vida = min(self.vida + 1, 9)
        elif tipo == "tiro_triplo":
            # acumula tempo caso pegue outro enquanto ativo
            self.tiro_triplo_timer = min(self.tiro_triplo_timer + 400, 800)
        else:
            raise ValueError(f"Power-up desconhecido: {tipo}")

# TIRO (DO JOGADOR)
class Tiro(Entidade):
    def __init__(self, x, y, dx=0):
        super().__init__(x, y, 10)
        self.dx = dx
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__), "assets", "images", "tiroJogador.png")
        imagem_original = pygame.image.load(CAMINHO_IMAGEM ).convert_alpha()
        self.image = pygame.transform.rotate(imagem_original, +90)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(center=(x, y))
   
    def update(self):
        self.rect.x += self.dx
        self.rect.y -= self.velocidade
        if (
            self.rect.y < -20
            or self.rect.x < -20
            or self.rect.x > LARGURA + 20
        ):
            self.kill()
