import pygame
import random
import os
from config import LARGURA, ALTURA, FPS
from entidade import Entidade
from robo import RoboLento, RoboZigueZague, RoboRapido

pygame.init()

TELA = pygame.display.set_mode((LARGURA, ALTURA))
CAMINHO_BACKGROUND = os.path.join(os.path.dirname(__file__), "assets", "images", "background-teste.png")
BACKGROUND = pygame.image.load(CAMINHO_BACKGROUND)
BACKGROUND = pygame.transform.scale(BACKGROUND, (LARGURA, ALTURA))

pygame.display.set_caption("Robot Defense - Template")
clock = pygame.time.Clock()

# JOGADOR
class Jogador(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5)
        self.image.fill((0, 255, 0))  # verde
        self.vida = 5

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.mover(0, -self.velocidade)
        if keys[pygame.K_s]:
            self.mover(0, self.velocidade)
        if keys[pygame.K_a]:
            self.mover(-self.velocidade, 0)
        if keys[pygame.K_d]:
            self.mover(self.velocidade, 0)

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

todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()

jogador = Jogador(LARGURA // 2, ALTURA - 60)
todos_sprites.add(jogador)

pontos = 0
spawn_timer = 0

rodando = True
while rodando:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                tiro = Tiro(jogador.rect.centerx, jogador.rect.y)
                todos_sprites.add(tiro)
                tiros.add(tiro)

    # timer de entrada dos inimigos
    spawn_timer += 1
    
    if spawn_timer % 40 == 0:
        robo = RoboZigueZague(random.randint(40, LARGURA - 40), -40)
        todos_sprites.add(robo)
        inimigos.add(robo)
    if spawn_timer % 60 == 0:
        roboLento = RoboLento(random.randint(40, LARGURA - 40), -40)
        todos_sprites.add(roboLento)
        inimigos.add(roboLento)
    if spawn_timer % 80 == 0:
        roboRapido = RoboRapido(random.randint(40, LARGURA - 40), -40)
        todos_sprites.add(roboRapido)
        inimigos.add(roboRapido)

    # colisão tiro x robô
    colisao = pygame.sprite.groupcollide(inimigos, tiros, True, True)
    pontos += len(colisao)

    # colisão robô x jogador
    if pygame.sprite.spritecollide(jogador, inimigos, True): # type: ignore para não ficar sublinhado de vermelho
        jogador.vida -= 1
        if jogador.vida <= 0:
            print("GAME OVER!")
            rodando = False

    # atualizar
    todos_sprites.update()

    # desenhar
    TELA.fill((20, 20, 20))
    TELA.blit(BACKGROUND, (0, 0))
    todos_sprites.draw(TELA)

    #Painel de pontos e vida
    font = pygame.font.SysFont(None, 30)
    texto = font.render(f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, (255, 255, 255))
    TELA.blit(texto, (10, 10))

    pygame.display.flip()

pygame.quit()
