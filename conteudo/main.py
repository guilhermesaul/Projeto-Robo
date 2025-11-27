import pygame
import random
import os
from config import LARGURA, ALTURA, FPS
from robo import RoboLento, RoboZigueZague, RoboRapido, RoboCiclico
from player import Jogador, Tiro

pygame.init()

TELA = pygame.display.set_mode((LARGURA, ALTURA))
CAMINHO_BACKGROUND = os.path.join(os.path.dirname(__file__), "assets", "images", "background-teste.png")
BACKGROUND = pygame.image.load(CAMINHO_BACKGROUND)
BACKGROUND = pygame.transform.scale(BACKGROUND, (LARGURA, ALTURA))

pygame.display.set_caption("Robot Defense - Template")
clock = pygame.time.Clock()

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
    
    # if spawn_timer % 40 == 0:
    #     roboLento = RoboLento(random.randint(40, LARGURA - 40), -40)
    #     todos_sprites.add(roboLento)
    #     inimigos.add(roboLento)
    # if spawn_timer % 60 == 0:
    #     roboRapido = RoboRapido(random.randint(40, LARGURA - 40), -40)
    #     todos_sprites.add(roboRapido)
    #     inimigos.add(roboRapido)
    # if spawn_timer % 80 == 0:
    #     robo = RoboZigueZague(random.randint(40, LARGURA - 40), -40)
    #     todos_sprites.add(robo)
    #     inimigos.add(robo)
    if spawn_timer % 40 == 0:
        roboCiclico = RoboCiclico(random.randint(60, LARGURA - 60), -40)
        todos_sprites.add(roboCiclico)
        inimigos.add(roboCiclico)


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
    if jogador.vida < 2:
     texto = font.render(f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, (255, 0, 0))
    else:
        texto = font.render(f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, (255, 255, 255))
    TELA.blit(texto, (10, 10))

    pygame.display.flip()

pygame.quit()
