import pygame
import random
import os
from config import LARGURA, ALTURA, FPS
from audio import inicializar_audio, tocar_musica_boss, parar_musica
from robo import RoboLento, RoboZigueZague, RoboRapido, RoboCiclico, RoboSaltador, RoboCacador, Boss 
from player import Jogador, Tiro

# Preconfigura o mixer antes do init para evitar erros/latência no Windows
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()

BASE_DIR = os.path.dirname(__file__)
SONS, CAMINHO_MUSICA_BOSS = inicializar_audio(BASE_DIR)

TELA = pygame.display.set_mode((LARGURA, ALTURA))
CAMINHO_BACKGROUND = os.path.join(os.path.dirname(__file__), "assets", "images", "background-teste.png")
BACKGROUND = pygame.image.load(CAMINHO_BACKGROUND)
BACKGROUND = pygame.transform.scale(BACKGROUND, (LARGURA, ALTURA))

pygame.display.set_caption("Robot Defense - Template")
clock = pygame.time.Clock()

todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()
# novo: grupo para tiros dos robôs
tiros_inimigos = pygame.sprite.Group()

jogador = Jogador(LARGURA // 2, ALTURA - 60)
todos_sprites.add(jogador)

pontos = 0
temporizador_spawn = 0
estado = "menu"  # menu, jogando, pausado, game_over, vitoria, boss
fade_alpha = 0
fade_direcao = 1
fase_atual = 1
opcao_menu = 0  # 0 = Iniciar, 1 = Sair
opcao_pausa = 0  # 0 = Continuar, 1 = Sair
cadencia_tiro = 0  # cooldown para rajada automática
boss_ativo = False
boss_spawnou = False
musica_boss_tocando = False

# Configuração de fases
FASES = {
    1: {"nome": "Fase 1: Iniciante", "duracao": 600, "robos": ["lento", "rapido"]},
    2: {"nome": "Fase 2: Saltadores", "duracao": 700, "robos": ["lento", "saltador", "ziguezague"]},
    3: {"nome": "Fase 3: Caçadores", "duracao": 900, "robos": ["rapido", "cacador", "ciclico"]},
    4: {"nome": "Fase 4: Boss Final", "duracao": 9999999, "robos": []}
}

def resetar_jogo():
    global pontos, temporizador_spawn, todos_sprites, inimigos, tiros, jogador, estado, fade_alpha, fade_direcao, fase_atual, tiros_inimigos, boss_ativo, boss_spawnou, musica_boss_tocando
    pontos = 0
    temporizador_spawn = 0
    fase_atual = 1
    boss_ativo = False
    boss_spawnou = False
    musica_boss_tocando = False
    pygame.mixer.music.stop()
    todos_sprites.empty()
    inimigos.empty()
    tiros.empty()
    tiros_inimigos.empty()
    jogador = Jogador(LARGURA // 2, ALTURA - 60)
    todos_sprites.add(jogador)
    estado = "jogando"
    fade_alpha = 0
    fade_direcao = 1

def spawnar_inimigos():
    global temporizador_spawn
    fase = FASES[fase_atual]
    robos_permitidos = fase["robos"]
    
    # RoboLento
    if "lento" in robos_permitidos and temporizador_spawn % 50 == 0:
        robo = RoboLento(random.randint(40, LARGURA - 40), -40, grupo_tiros=tiros_inimigos)
        todos_sprites.add(robo)
        inimigos.add(robo)
    
    # RoboRapido
    if "rapido" in robos_permitidos and temporizador_spawn % 60 == 0:
        robo = RoboRapido(random.randint(40, LARGURA - 40), -40, grupo_tiros=tiros_inimigos)
        todos_sprites.add(robo)
        inimigos.add(robo)
    
    # RoboSaltador
    if "saltador" in robos_permitidos and temporizador_spawn % 75 == 0:
        robo = RoboSaltador(random.randint(40, LARGURA - 40), -40, grupo_tiros=tiros_inimigos)
        todos_sprites.add(robo)
        inimigos.add(robo)
    
    # RoboZigueZague
    if "ziguezague" in robos_permitidos and temporizador_spawn % 80 == 0:
        robo = RoboZigueZague(random.randint(40, LARGURA - 40), -40, grupo_tiros=tiros_inimigos)
        todos_sprites.add(robo)
        inimigos.add(robo)
    
    # RoboCacador
    if "cacador" in robos_permitidos and temporizador_spawn % 120 == 0:
        robo = RoboCacador(random.randint(40, LARGURA - 40), -60, jogador, grupo_tiros=tiros_inimigos)
        todos_sprites.add(robo)
        inimigos.add(robo)
    
    # RoboCiclico
    if "ciclico" in robos_permitidos and temporizador_spawn % 90 == 0:
        robo = RoboCiclico(random.randint(60, LARGURA - 60), -40, grupo_tiros=tiros_inimigos)
        todos_sprites.add(robo)
        inimigos.add(robo)

rodando = True
while rodando:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if estado == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    opcao_menu = 1 - opcao_menu
                elif event.key == pygame.K_RETURN:
                    if opcao_menu == 0:
                        resetar_jogo()
                    else:
                        rodando = False
        
        elif estado == "jogando":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estado = "pausado"
        
        elif estado == "pausado":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    opcao_pausa = 1 - opcao_pausa
                elif event.key == pygame.K_RETURN:
                    if opcao_pausa == 0:
                        estado = "jogando"
                    else:
                        estado = "menu"
                        opcao_menu = 0
        
        elif estado == "game_over" or estado == "vitoria":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                estado = "menu"
                opcao_menu = 0

    if estado == "jogando":
        temporizador_spawn += 1
        
        # Verificar progressão de fase
        if temporizador_spawn >= FASES[fase_atual]["duracao"] and fase_atual < len(FASES):
            fase_atual += 1
            temporizador_spawn = 0
            
            # Se chegou na fase 4, spawna o boss
            if fase_atual == 4 and not boss_spawnou:
                boss = Boss(LARGURA // 2, -100, grupo_tiros=tiros_inimigos)
                todos_sprites.add(boss)
                inimigos.add(boss)
                boss_ativo = True
                boss_spawnou = True
                
                # Toca música do boss
                if not musica_boss_tocando and os.path.exists(CAMINHO_MUSICA_BOSS):
                    tocar_musica_boss(CAMINHO_MUSICA_BOSS)
                    musica_boss_tocando = True
        
        # Spawnar inimigos da fase atual (não spawna na fase do boss)
        if fase_atual < 4:
            spawnar_inimigos()
        
        # Sistema de rajada automática ao segurar espaço
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if cadencia_tiro <= 0:
                tiro = Tiro(jogador.rect.centerx, jogador.rect.y)
                todos_sprites.add(tiro)
                tiros.add(tiro)
                if SONS.get("laser"):
                    SONS["laser"].play()
                cadencia_tiro = 10  # intervalo entre tiros (menor = mais rápido)
        
        if cadencia_tiro > 0:
            cadencia_tiro -= 1


    # colisão tiro x robô
    if estado == "jogando":
        # colisão tiro jogador x robo
        colisoes = pygame.sprite.groupcollide(inimigos, tiros, False, True)
        for inimigo, tiros_atingidos in colisoes.items():
            if isinstance(inimigo, Boss):
                # Boss leva dano mas não morre automaticamente
                if inimigo.receber_dano():
                    # Boss morreu
                    pontos += 50
                    if SONS.get("explosao"):
                        SONS["explosao"].play()
                    parar_musica()
                    musica_boss_tocando = False
                    boss_ativo = False
                    # Vitória ao derrotar o boss
                    estado = "vitoria"
                    fade_alpha = 0
                    fade_direcao = 1
            else:
                # Inimigos normais morrem com um tiro
                inimigo.kill()
                pontos += 1
                if SONS.get("explosao"):
                    SONS["explosao"].play()
        
        # colisão tiro jogador x tiro inimigo -> ambos somem
        pygame.sprite.groupcollide(tiros, tiros_inimigos, True, True)

    # colisão robô x jogador
    if estado == "jogando":
        colisoes_jogador = pygame.sprite.spritecollide(jogador, inimigos, False) # type: ignore para nao ficar sublinhado de vermelho
        if colisoes_jogador:
            for inimigo in colisoes_jogador:
                if not isinstance(inimigo, Boss):
                    inimigo.kill()
                jogador.vida -= 1
                if jogador.vida <= 0:
                    estado = "game_over"
                    fade_alpha = 0
                    fade_direcao = 1
                    parar_musica()
                    musica_boss_tocando = False
        
        # colisão tiro inimigo x jogador
        if pygame.sprite.spritecollide(jogador, tiros_inimigos, True): # type: ignore | para nao ficar sublinhado de vermelho
            jogador.vida -= 1
            if jogador.vida <= 0:
                estado = "game_over"
                fade_alpha = 0
                fade_direcao = 1
                parar_musica()
                musica_boss_tocando = False

    # atualizar
    if estado == "jogando":
        todos_sprites.update()
        tiros_inimigos.update()   # atualiza tiros dos robôs também

    # desenhar
    TELA.fill((20, 20, 20))
    TELA.blit(BACKGROUND, (0, 0))
    todos_sprites.draw(TELA)
    tiros_inimigos.draw(TELA)   # desenha tiros dos robôs

    #Painel de pontos e vida
    font = pygame.font.SysFont(None, 30)
    
    if estado == "menu":
        # Menu inicial
        fonte_titulo = pygame.font.SysFont(None, 80)
        fonte_opcao = pygame.font.SysFont(None, 50)
        
        titulo = fonte_titulo.render("ROBOT DEFENSE", True, (0, 255, 255))
        TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, ALTURA//2 - 150))
        
        cor_iniciar = (255, 255, 0) if opcao_menu == 0 else (255, 255, 255)
        cor_sair = (255, 255, 0) if opcao_menu == 1 else (255, 255, 255)
        
        texto_iniciar = fonte_opcao.render("► INICIAR" if opcao_menu == 0 else "  INICIAR", True, cor_iniciar)
        texto_sair = fonte_opcao.render("► SAIR" if opcao_menu == 1 else "  SAIR", True, cor_sair)
        
        TELA.blit(texto_iniciar, (LARGURA//2 - 80, ALTURA//2 + 20))
        TELA.blit(texto_sair, (LARGURA//2 - 80, ALTURA//2 + 80))
        
        fonte_info = pygame.font.SysFont(None, 28)
        info = fonte_info.render("Use SETAS e ENTER para navegar", True, (150, 150, 150))
        TELA.blit(info, (LARGURA//2 - info.get_width()//2, ALTURA - 50))
    
    elif estado == "jogando":
        if jogador.vida < 2:
            texto = font.render(f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, (255, 0, 0))
        else:
            texto = font.render(f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, (255, 255, 255))
        TELA.blit(texto, (10, 10))
        
        # Mostrar fase atual
        texto_fase = font.render(FASES[fase_atual]["nome"], True, (255, 255, 0))
        TELA.blit(texto_fase, (LARGURA - texto_fase.get_width() - 10, 10))
        
        # Mostrar vida do boss se estiver ativo
        if boss_ativo:
            for inimigo in inimigos:
                if isinstance(inimigo, Boss):
                    barra_largura = 200
                    barra_altura = 20
                    barra_x = LARGURA // 2 - barra_largura // 2
                    barra_y = 50
                    
                    # Fundo da barra
                    pygame.draw.rect(TELA, (100, 100, 100), (barra_x, barra_y, barra_largura, barra_altura))
                    # Vida atual
                    vida_largura = int((inimigo.vida / 50) * barra_largura)
                    pygame.draw.rect(TELA, (255, 0, 0), (barra_x, barra_y, vida_largura, barra_altura))
                    # Borda
                    pygame.draw.rect(TELA, (255, 255, 255), (barra_x, barra_y, barra_largura, barra_altura), 2)
                    
                    texto_boss = font.render("BOSS", True, (255, 255, 255))
                    TELA.blit(texto_boss, (barra_x + barra_largura // 2 - texto_boss.get_width() // 2, barra_y - 25))
                    break
    
    elif estado == "pausado":
        # Overlay de pausa
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        TELA.blit(overlay, (0, 0))
        
        fonte_titulo = pygame.font.SysFont(None, 80)
        fonte_opcao = pygame.font.SysFont(None, 50)
        
        titulo = fonte_titulo.render("PAUSADO", True, (255, 255, 0))
        TELA.blit(titulo, (LARGURA//2 - titulo.get_width()//2, ALTURA//2 - 120))
        
        cor_continuar = (255, 255, 0) if opcao_pausa == 0 else (255, 255, 255)
        cor_sair = (255, 255, 0) if opcao_pausa == 1 else (255, 255, 255)
        
        texto_continuar = fonte_opcao.render("► CONTINUAR" if opcao_pausa == 0 else "  CONTINUAR", True, cor_continuar)
        texto_sair = fonte_opcao.render("► SAIR" if opcao_pausa == 1 else "  SAIR", True, cor_sair)
        
        TELA.blit(texto_continuar, (LARGURA//2 - 120, ALTURA//2))
        TELA.blit(texto_sair, (LARGURA//2 - 120, ALTURA//2 + 70))
    
    elif estado == "game_over":
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
        texto_restart = fonte_media.render("Aperte ESPAÇO para voltar ao menu", True, (0, 255, 255))
        
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
    
    elif estado == "vitoria":
        # Controle do fade in/out
        if fade_direcao == 1:
            fade_alpha += 5
            if fade_alpha >= 255:
                fade_alpha = 255
                fade_direcao = 0
        
        # Tela de Vitória com fade
        fonte_grande = pygame.font.SysFont(None, 72)
        fonte_media = pygame.font.SysFont(None, 40)
        texto_vitoria = fonte_grande.render("VITÓRIA!", True, (0, 255, 0))
        texto_pontos = fonte_media.render(f"Pontuação: {pontos}", True, (255, 255, 255))
        texto_restart = fonte_media.render("Aperte ESPAÇO para voltar ao menu", True, (255, 255, 0))
        
        # overlay escuro com fade
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(min(int(fade_alpha * 0.7), 180))
        overlay.fill((0, 0, 0))
        TELA.blit(overlay, (0, 0))
        
        # textos com fade
        texto_vitoria.set_alpha(fade_alpha)
        texto_pontos.set_alpha(fade_alpha)
        texto_restart.set_alpha(fade_alpha)
        
        TELA.blit(texto_vitoria, (LARGURA//2 - texto_vitoria.get_width()//2, ALTURA//2 - 120))
        TELA.blit(texto_pontos, (LARGURA//2 - texto_pontos.get_width()//2, ALTURA//2 - 40))
        TELA.blit(texto_restart, (LARGURA//2 - texto_restart.get_width()//2, ALTURA//2 + 40))


    pygame.display.flip()

pygame.quit()
