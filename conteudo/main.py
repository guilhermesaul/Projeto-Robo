import pygame
import random
import os
from config import LARGURA, ALTURA, FPS
from robo import RoboLento, RoboZigueZague, RoboRapido, RoboCiclico, RoboSaltador, RoboCacador 
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
temporizador_spawn = 0
estado = "jogando"  # ou "game_over"
fade_alpha = 0  # controle de fade in/out
fade_direcao = 1  # 1 para fade in, -1 para fade out

def resetar_jogo():
    global pontos, temporizador_spawn, todos_sprites, inimigos, tiros, jogador, estado, fade_alpha, fade_direcao
    pontos = 0
    temporizador_spawn = 0
    todos_sprites.empty()
    inimigos.empty()
    tiros.empty()
    jogador = Jogador(LARGURA // 2, ALTURA - 60)
    todos_sprites.add(jogador)
    estado = "jogando"
    fade_alpha = 0
    fade_direcao = 1

rodando = True
while rodando:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if estado == "jogando":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                tiro = Tiro(jogador.rect.centerx, jogador.rect.y)
                todos_sprites.add(tiro)
                tiros.add(tiro)
        elif estado == "game_over":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                resetar_jogo()

    if estado == "jogando":
        temporizador_spawn += 1
    
    # if spawn_timer % 40 == 0:
    #     roboLento = RoboLento(random.randint(40, LARGURA - 40), -40)
    #     todos_sprites.add(roboLento)
    #     inimigos.add(roboLento)
        
    if estado == "jogando":
        # RoboSaltador: entra com frequência moderada
        if temporizador_spawn % 75 == 0:
            roboSaltador = RoboSaltador(random.randint(40, LARGURA - 40), -40)
            todos_sprites.add(roboSaltador)
            inimigos.add(roboSaltador)
        # RoboCacador: menos frequente e mais perigoso
        if temporizador_spawn % 120 == 0:
            roboCacador = RoboCacador(random.randint(40, LARGURA - 40), -60, jogador)
            todos_sprites.add(roboCacador)
            inimigos.add(roboCacador)
    # if spawn_timer % 60 == 0:
    #     roboRapido = RoboRapido(random.randint(40, LARGURA - 40), -40)
    #     todos_sprites.add(roboRapido)
    #     inimigos.add(roboRapido)
    # if spawn_timer % 80 == 0:
    #     robo = RoboZigueZague(random.randint(40, LARGURA - 40), -40)
    #     todos_sprites.add(robo)
    #     inimigos.add(robo)
    # if spawn_timer % 40 == 0:
    #     roboCiclico = RoboCiclico(random.randint(60, LARGURA - 60), -40)
    #     todos_sprites.add(roboCiclico)
    #     inimigos.add(roboCiclico)


    # colisão tiro x robô
    if estado == "jogando":
        colisao = pygame.sprite.groupcollide(inimigos, tiros, True, True)
        pontos += len(colisao)

    # colisão robô x jogador
    if estado == "jogando":
        if pygame.sprite.spritecollide(jogador, inimigos, True): # type: ignore
            jogador.vida -= 1
            if jogador.vida <= 0:
                estado = "game_over"
                fade_alpha = 0  # começa fade in do game over
                fade_direcao = 1

    # atualizar
    if estado == "jogando":
        todos_sprites.update()

    # desenhar
    TELA.fill((20, 20, 20))
    TELA.blit(BACKGROUND, (0, 0))
    todos_sprites.draw(TELA)

    #Painel de pontos e vida
    font = pygame.font.SysFont(None, 30)
    if estado == "jogando":
        if jogador.vida < 2:
            texto = font.render(f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, (255, 0, 0))
        else:
            texto = font.render(f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, (255, 255, 255))
        TELA.blit(texto, (10, 10))
    else:
        # Controle do fade in/out
        if fade_direcao == 1:
            fade_alpha += 5
            if fade_alpha >= 255:
                fade_alpha = 255
                fade_direcao = 0  # fade completo, mantém
        
        # Tela de Game Over com fade
        fonte_grande = pygame.font.SysFont(None, 72)
        fonte_media = pygame.font.SysFont(None, 40)
        texto_gameover = fonte_grande.render("GAME OVER", True, (255, 0, 0))
        texto_pontos = fonte_media.render(f"Pontuação: {pontos}", True, (255, 255, 255))
        texto_restart = fonte_media.render("Aperte ESPAÇO para reiniciar", True, (0, 255, 255))
        
        # overlay escuro com fade
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(min(int(fade_alpha * 0.7), 180))
        overlay.fill((0, 0, 0))
        TELA.blit(overlay, (0, 0))
        
        # textos com fade
        texto_gameover.set_alpha(fade_alpha)
        texto_pontos.set_alpha(fade_alpha)
        texto_restart.set_alpha(fade_alpha)
        
        TELA.blit(texto_gameover, (LARGURA//2 - texto_gameover.get_width()//2, ALTURA//2 - 120))
        TELA.blit(texto_pontos, (LARGURA//2 - texto_pontos.get_width()//2, ALTURA//2 - 40))
        TELA.blit(texto_restart, (LARGURA//2 - texto_restart.get_width()//2, ALTURA//2 + 40))

    pygame.display.flip()

pygame.quit()
