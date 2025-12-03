import pygame
import os
import random
from entidade import Entidade
from config import LARGURA, ALTURA

class BossFinal(Entidade):
    def __init__(self, grupo_tiros=None):
        super().__init__(LARGURA // 2, 80, velocidade=3)

        #  IMAGEM DO BOSS 
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__), "assets", "images", "boss.png")
        if os.path.exists(CAMINHO_IMAGEM):
            img = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.scale(img, (256, 256))  # dobro do tamanho normal
        else:
            # Caso não tenha imagem ainda, cria um placeholder
            self.image = pygame.Surface((256, 256))
            self.image.fill((200, 30, 30))  # vermelho escuro

        self.rect = self.image.get_rect(center=(LARGURA // 2, 100))

        #  ATRIBUTOS DO BOSS 
        self.vida_max = 3000
        self.vida = self.vida_max

        self.dano = 30  # mais dano que inimigo comum
        self.velocidade = 3
        self.direcao = 1  # esquerda/direita

        # tiros
        self.grupo_tiros = grupo_tiros
        self.tiro_timer = 70  # velocidade de tiro
        self.vel_tiro = 8     # tiro mais rápido

    
    # Padrão de movimento
    
    def mover_horizontal(self):
        self.rect.x += self.velocidade * self.direcao

        # bater nas bordas
        if self.rect.right >= LARGURA - 20:
            self.direcao = -1
        elif self.rect.left <= 20:
            self.direcao = 1

    
    # Ataque do Boss
    
    def tentar_atirar(self):
        if self.grupo_tiros is None:
            return

        self.tiro_timer -= 1

        if self.tiro_timer <= 0:
            # atira 3 tiros ao mesmo tempo (dano maior)
            for offset in [-40, 0, 40]:
                tiro = TiroBoss(self.rect.centerx + offset, self.rect.bottom, self.vel_tiro)
                self.grupo_tiros.add(tiro)

            self.tiro_timer = random.randint(50, 100)

    
    # Update principal
    
    def update(self):
        self.mover_horizontal()
        self.tentar_atirar()

    
    # Barra de vida (opcional)
    
    def desenhar_barra_de_vida(self, tela):
        largura = 300
        altura = 20
        x = (LARGURA - largura) // 2
        y = 20

        # fundo
        pygame.draw.rect(tela, (100, 0, 0), (x, y, largura, altura))
        # vida atual
        vida_atual = int((self.vida / self.vida_max) * largura)
        pygame.draw.rect(tela, (255, 0, 0), (x, y, vida_atual, altura))


# TIRO DO BOSS — maior e mais rápido que o tiro normal

class TiroBoss(Entidade):
    def __init__(self, x, y, velocidade):
        super().__init__(x, y, velocidade)
        self.image = pygame.Surface((12, 20))
        self.image.fill((255, 80, 80))  # vermelho forte
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y > ALTURA:
            self.kill()
