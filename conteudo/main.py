import os
import random

import pygame

from config import ALTURA, FPS, LARGURA
from player import Jogador, Tiro
from powerup import PowerUp, gerar_tipo_powerup
from robo import (
    RoboCacador,
    RoboCiclico,
    RoboLento,
    RoboRapido,
    RoboSaltador,
    RoboZigueZague,
    Explosao,
    Boss
)

pygame.init()
pygame.mixer.init()

CAMINHO_SOM_LASER = os.path.join(
    os.path.dirname(__file__), "assets", "audios", "laser-shot.wav"
)
CAMINHO_SOM_EXPLOSAO = os.path.join(
    os.path.dirname(__file__), "assets", "audios", "explosao-nave.wav"
)
CAMINHO_MUSICA_BACKGROUND = os.path.join(
    os.path.dirname(__file__), "assets", "audios", "trilha-sonora-background.mp3"
)
CAMINHO_MUSICA_BOSS = os.path.join(
    os.path.dirname(__file__), "assets", "audios", "trilha-sonora-boss.mp3"
)
CAMINHO_MUSICA_FASE_SECRETA = os.path.join(
    os.path.dirname(__file__), "assets", "audios", "trilha-sonora-fase-secreta.mp3"
)
SOM_LASER = pygame.mixer.Sound(CAMINHO_SOM_LASER)
SOM_EXPLOSAO = pygame.mixer.Sound(CAMINHO_SOM_EXPLOSAO)
SOM_LASER.set_volume(0.3)
SOM_EXPLOSAO.set_volume(0.4)

TELA = pygame.display.set_mode((LARGURA, ALTURA))
CAMINHO_BACKGROUND = os.path.join(
    os.path.dirname(__file__), "assets", "images", "background-fases-normais.png"
)
BACKGROUND = pygame.image.load(CAMINHO_BACKGROUND)
BACKGROUND = pygame.transform.scale(BACKGROUND, (LARGURA, ALTURA))

# Background da Fase Secreta
CAMINHO_BACKGROUND_CAOS = os.path.join(
    os.path.dirname(__file__), "assets", "images", "background-fase-secreta.png"
)
BACKGROUND_CAOS = pygame.image.load(CAMINHO_BACKGROUND_CAOS)
BACKGROUND_CAOS = pygame.transform.scale(BACKGROUND_CAOS, (LARGURA, ALTURA))

pygame.display.set_caption("Robot Defense - Template")
clock = pygame.time.Clock()

todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
tiros = pygame.sprite.Group()
# novo: grupo para tiros dos robôs
tiros_inimigos = pygame.sprite.Group()
# power-ups
powerups = pygame.sprite.Group()

POWERUP_CHANCE = 0.18

jogador = Jogador(LARGURA // 2, ALTURA - 60)
todos_sprites.add(jogador)

pontos = 0
temporizador_spawn = 0
estado = "menu"  # menu, jogando, pausado, game_over, vitoria, transicao_caos
fade_alpha = 255  # Começa com tela preta para fade in inicial
fade_direcao = -1  # -1 = fade in (clarear)
fase_atual = 1
opcao_menu = 0  # 0 = Iniciar, 1 = Sair
opcao_pausa = 0  # 0 = Continuar, 1 = Sair
cadencia_tiro = 0  # cooldown para rajada automática
musica_atual = None  # controle da música tocando
musica_fade_out = False  # flag para fade out em progresso
musica_proxima = None  # próxima música a tocar após fade
musica_volume = 0.5  # volume atual da música
boss_ativo = False
boss_spawnou = False
inimigos_escapados = 0  # Contador para Easter Egg
fase_caos_desbloqueada = False  # Flag para Fase do Caos
timer_transicao_caos = 0  # Timer para a tela de transição

# Configuração de fases
FASES = {
    1: {"nome": "Fase 1: Iniciante", "duracao": 6, "robos": ["lento", "rapido"]},
    2: {
        "nome": "Fase 2: Saltadores",
        "duracao": 7,
        "robos": ["lento", "saltador", "ziguezague"],
    },
    3: {
        "nome": "Fase 3: Caçadores",
        "duracao": 9,
        "robos": ["rapido", "cacador", "ciclico"],
    },
    4: {
        "nome": "Fase 4: Boss Final",
        "duracao": 9999999,
        "robos": [],
    },
    5: {
        "nome": "FASE DO CAOS",
        "duracao": 1800,  # 30 segundos de caos puro
        "robos": ["lento", "rapido", "saltador", "ziguezague", "cacador", "ciclico"],
    },
}


def resetar_jogo():
    global \
        pontos, \
        temporizador_spawn, \
        todos_sprites, \
        inimigos, \
        tiros, \
        jogador, \
        estado, \
        fade_alpha, \
        fade_direcao, \
        fase_atual, \
        tiros_inimigos, \
        powerups, \
        musica_atual, \
        musica_fade_out, \
        musica_proxima, \
        musica_volume, \
        boss_ativo, \
        boss_spawnou, \
        inimigos_escapados, \
        fase_caos_desbloqueada
    pontos = 0
    temporizador_spawn = 0
    fase_atual = 1
    boss_ativo = False
    boss_spawnou = False
    inimigos_escapados = 0
    fase_caos_desbloqueada = False
    musica_fade_out = False
    musica_proxima = None
    musica_volume = 0.5
    todos_sprites.empty()
    inimigos.empty()
    tiros.empty()
    tiros_inimigos.empty()
    powerups.empty()
    jogador = Jogador(LARGURA // 2, ALTURA - 60)
    todos_sprites.add(jogador)
    estado = "jogando"
    fade_alpha = 0
    fade_direcao = 0
    
    # Iniciar música de fundo das fases normais
    if os.path.exists(CAMINHO_MUSICA_BACKGROUND):
        pygame.mixer.music.load(CAMINHO_MUSICA_BACKGROUND)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # loop infinito
        musica_atual = "background"


def spawnar_inimigos():
    global temporizador_spawn
    fase = FASES[fase_atual]
    robos_permitidos = fase["robos"]

    # RoboLento
    if "lento" in robos_permitidos and temporizador_spawn % 50 == 0:
        robo = RoboLento(
            random.randint(40, LARGURA - 40), -40, grupo_tiros=tiros_inimigos
        )
        todos_sprites.add(robo)
        inimigos.add(robo)

    # RoboRapido
    if "rapido" in robos_permitidos and temporizador_spawn % 60 == 0:
        robo = RoboRapido(
            random.randint(40, LARGURA - 40), -40, grupo_tiros=tiros_inimigos
        )
        todos_sprites.add(robo)
        inimigos.add(robo)

    # RoboSaltador
    if "saltador" in robos_permitidos and temporizador_spawn % 75 == 0:
        robo = RoboSaltador(
            random.randint(40, LARGURA - 40), -40, grupo_tiros=tiros_inimigos
        )
        todos_sprites.add(robo)
        inimigos.add(robo)

    # RoboZigueZague
    if "ziguezague" in robos_permitidos and temporizador_spawn % 80 == 0:
        robo = RoboZigueZague(
            random.randint(40, LARGURA - 40), -40, grupo_tiros=tiros_inimigos
        )
        todos_sprites.add(robo)
        inimigos.add(robo)

    # RoboCacador
    if "cacador" in robos_permitidos and temporizador_spawn % 120 == 0:
        robo = RoboCacador(
            random.randint(40, LARGURA - 40), -60, jogador, grupo_tiros=tiros_inimigos
        )
        todos_sprites.add(robo)
        inimigos.add(robo)

    # RoboCiclico
    if "ciclico" in robos_permitidos and temporizador_spawn % 90 == 0:
        robo = RoboCiclico(
            random.randint(60, LARGURA - 60), -40, grupo_tiros=tiros_inimigos
        )
        todos_sprites.add(robo)
        inimigos.add(robo)


def tentar_drop_powerup(inimigo):
    """Chance de derrubar um power-up na posição do inimigo destruído."""
    if random.random() <= POWERUP_CHANCE:
        tipo = gerar_tipo_powerup()
        powerup = PowerUp(inimigo.rect.centerx, inimigo.rect.centery, tipo)
        todos_sprites.add(powerup)
        powerups.add(powerup)


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

    # Processar tela de transição para Fase do Caos
    if estado == "transicao_caos":
        timer_transicao_caos += 1
        # Após 4 segundos (240 frames), iniciar Fase do Caos
        if timer_transicao_caos >= 240:
            estado = "jogando"
            fase_atual = 5
            temporizador_spawn = 0
            
            # Power-ups especiais no início
            jogador.aplicar_powerup("tiro_triplo")
            jogador.aplicar_powerup("velocidade")
            jogador.vida = min(jogador.vida + 3, 10)  # Recupera vida

    # Processar fade in inicial
    if fade_direcao == -1:
        fade_alpha -= 8
        if fade_alpha <= 0:
            fade_alpha = 0
            fade_direcao = 0
    
    if estado == "jogando":
        temporizador_spawn += 1

        # Verificar progressão de fase
        if temporizador_spawn >= FASES[fase_atual]["duracao"]:
            # Vitória na Fase do Caos
            if fase_atual == 5:
                estado = "vitoria"
                fade_alpha = 0
                fade_direcao = 1
                pygame.mixer.music.stop()
            elif fase_atual < len(FASES):
                fase_atual += 1
                temporizador_spawn = 0
            
            # Spawnar boss ao entrar na fase 4
            if fase_atual == 4 and not boss_spawnou:
                boss = Boss(LARGURA // 2, -100, grupo_tiros=tiros_inimigos)
                todos_sprites.add(boss)
                inimigos.add(boss)
                boss_ativo = True
                boss_spawnou = True
            
            # Trocar música ao entrar na fase 4 (boss)
            if fase_atual == 4 and musica_atual != "boss":
                if os.path.exists(CAMINHO_MUSICA_BOSS):
                    pygame.mixer.music.load(CAMINHO_MUSICA_BOSS)
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    musica_atual = "boss"

        # Spawnar inimigos da fase atual
        if fase_atual < 4:
            spawnar_inimigos()
        elif fase_atual == 5:
            # FASE DO CAOS - Spawn intensificado
            spawnar_inimigos()
            # Spawn extra de inimigos (dobra a quantidade)
            if temporizador_spawn % 25 == 0:  # Muito mais rápido
                tipos = ["lento", "rapido", "saltador", "ziguezague", "cacador", "ciclico"]
                tipo_escolhido = random.choice(tipos)
                
                if tipo_escolhido == "lento":
                    robo = RoboLento(random.randint(40, LARGURA - 40), -40, grupo_tiros=tiros_inimigos)
                elif tipo_escolhido == "rapido":
                    robo = RoboRapido(random.randint(40, LARGURA - 40), -40, grupo_tiros=tiros_inimigos)
                elif tipo_escolhido == "saltador":
                    robo = RoboSaltador(random.randint(40, LARGURA - 40), -40, grupo_tiros=tiros_inimigos)
                elif tipo_escolhido == "ziguezague":
                    robo = RoboZigueZague(random.randint(40, LARGURA - 40), -40, grupo_tiros=tiros_inimigos)
                elif tipo_escolhido == "cacador":
                    robo = RoboCacador(random.randint(40, LARGURA - 40), -60, jogador, grupo_tiros=tiros_inimigos)
                else:  # ciclico
                    robo = RoboCiclico(random.randint(60, LARGURA - 60), -40, grupo_tiros=tiros_inimigos)
                
                todos_sprites.add(robo)
                inimigos.add(robo)
        
        # Sistema de rajada automática ao segurar espaço
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if cadencia_tiro <= 0:
                novos_tiros = []
                if jogador.tiro_triplo_ativo:
                    for deslocamento, dx in [(-15, -2), (0, 0), (15, 2)]:
                        novos_tiros.append(
                            Tiro(
                                jogador.rect.centerx + deslocamento, jogador.rect.y, dx
                            )
                        )
                else:
                    novos_tiros.append(Tiro(jogador.rect.centerx, jogador.rect.y))

                for tiro in novos_tiros:
                    todos_sprites.add(tiro)
                    tiros.add(tiro)
                SOM_LASER.play()
                cadencia_tiro = 10  # intervalo entre tiros (menor = mais rápido)

        if cadencia_tiro > 0:
            cadencia_tiro -= 1

    # colisão tiro x robô
    if estado == "jogando":
        # colisão tiro jogador x robo
        colisao = pygame.sprite.groupcollide(inimigos, tiros, False, True)
        if colisao:
            for inimigo in colisao:
                # Tratamento especial para o boss
                if isinstance(inimigo, Boss):
                    morreu, dropar_powerup = inimigo.receber_dano()
                    
                    # Dropar power-up se a flag retornar True
                    if dropar_powerup:
                        tipo = gerar_tipo_powerup()  # Escolhe aleatoriamente entre os 3 tipos
                        powerup = PowerUp(inimigo.rect.centerx, inimigo.rect.centery, tipo)
                        todos_sprites.add(powerup)
                        powerups.add(powerup)
                    
                    if morreu:
                        # Boss morreu
                        explosao = Explosao(inimigo.rect.centerx, inimigo.rect.centery)
                        todos_sprites.add(explosao)
                        pontos += 1000
                        boss_ativo = False
                        SOM_EXPLOSAO.play()
                        
                        # EASTER EGG: Verificar se nenhum inimigo escapou
                        print(f"DEBUG: Boss derrotado! Inimigos escapados: {inimigos_escapados}")
                        if inimigos_escapados == 0:
                            # Fase do Caos desbloqueada! Ir para tela de transição
                            estado = "transicao_caos"
                            timer_transicao_caos = 0
                            fase_caos_desbloqueada = True
                            
                            # Limpar tela
                            inimigos.empty()
                            tiros.empty()
                            tiros_inimigos.empty()
                            
                            # Iniciar fade out da música do boss e carregar próxima
                            musica_fade_out = True
                            musica_proxima = "fase_secreta"
                        else:
                            # Vitória normal
                            estado = "vitoria"
                            fade_alpha = 0
                            fade_direcao = 1
                            pygame.mixer.music.stop()
                else:
                    # Inimigos normais morrem em 1 tiro
                    explosao = Explosao(inimigo.rect.centerx, inimigo.rect.centery)
                    todos_sprites.add(explosao)
                    inimigo.kill()
                    pontos += 1
                    tentar_drop_powerup(inimigo)
                    SOM_EXPLOSAO.play()


        # colisão tiro jogador x tiro inimigo -> ambos somem
        pygame.sprite.groupcollide(tiros, tiros_inimigos, True, True)

        # coleta de power-ups
        coletados = pygame.sprite.spritecollide(jogador, powerups, True)  # type: ignore[arg-type]
        for item in coletados:
            jogador.aplicar_powerup(item.tipo)

     # colisão tiro inimigo x jogador (simples: cada tiro que acertar subtrai 1 vida)
    if estado == "jogando":
        # pega a lista de tiros inimigos que colidiram com o jogador e já remove esses tiros
        tiros_acertaram = pygame.sprite.spritecollide(jogador, tiros_inimigos, True)  # type: ignore[arg-type]
        if tiros_acertaram:
            # para cada tiro que acertou, tira 1 vida
            for _ in tiros_acertaram:
                jogador.vida -= 1
                # checa se acabou a vida
                if jogador.vida <= 0:
                    estado = "game_over"
                    fade_alpha = 0
                    fade_direcao = 1
                    break  # sair do loop de tiros (já morreu)
                
    # colisão robô x jogador
    if estado == "jogando":
        # Verifica colisão sem remover os inimigos automaticamente
        inimigos_colididos = pygame.sprite.spritecollide(jogador, inimigos, False)  # type: ignore[arg-type]
        for inimigo in inimigos_colididos:
            jogador.vida -= 1
            # Remove apenas inimigos normais, Boss não é removido
            if not isinstance(inimigo, Boss):
                inimigo.kill()
            if jogador.vida <= 0:
                estado = "game_over"
                fade_alpha = 0  # começa fade in do game over
                fade_direcao = 1
                break

    # atualizar
    if estado == "jogando":
        todos_sprites.update()
        tiros_inimigos.update()  # atualiza tiros dos robôs também
        
        # Rastrear inimigos que escapam (qualquer fase) e contar para o Easter Egg apenas nas fases 1-3
        for inimigo in list(inimigos):
            if inimigo.rect.top > ALTURA:
                if fase_atual < 4 and not isinstance(inimigo, Boss):
                    inimigos_escapados += 1
                    print(f"DEBUG: Inimigo escapou! Total escapados: {inimigos_escapados}")
                inimigo.kill()  # Remove do grupo de sprites
    
    # Sistema de fade de música
    if musica_fade_out:
        musica_volume -= 0.02  # Diminui gradualmente
        if musica_volume <= 0:
            musica_volume = 0
            pygame.mixer.music.stop()
            
            # Carregar e tocar próxima música
            if musica_proxima == "fase_secreta":
                if os.path.exists(CAMINHO_MUSICA_FASE_SECRETA):
                    pygame.mixer.music.load(CAMINHO_MUSICA_FASE_SECRETA)
                    pygame.mixer.music.set_volume(0)
                    pygame.mixer.music.play(-1)
                    musica_atual = "fase_secreta"
                    musica_fade_out = False
                    musica_proxima = None
                    # Agora fazer fade in
        else:
            pygame.mixer.music.set_volume(musica_volume)
    elif musica_atual == "fase_secreta" and musica_volume < 0.5:
        # Fade in da música da fase secreta
        musica_volume += 0.02
        if musica_volume > 0.5:
            musica_volume = 0.5
        pygame.mixer.music.set_volume(musica_volume)

    # desenhar
    TELA.fill((20, 20, 20))
    
    # Background especial para Fase do Caos
    if fase_atual == 5:
        TELA.blit(BACKGROUND_CAOS, (0, 0))
    else:
        TELA.blit(BACKGROUND, (0, 0))

    # Painel de pontos e vida
    font = pygame.font.SysFont(None, 30)

    if estado == "menu":
        # Menu inicial
        CAMINHO_FONTE = os.path.join(os.path.dirname(__file__), "assets", "fonte", "Orbitron-VariableFont_wght.ttf")
        fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 80)
        fonte_opcao = pygame.font.Font(CAMINHO_FONTE, 50)
                
        titulo = fonte_titulo.render("ROBOT DEFENSE", True, (0, 255, 255))
        TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2 - 150))

        cor_iniciar = (255, 255, 0) if opcao_menu == 0 else (255, 255, 255)
        cor_sair = (255, 255, 0) if opcao_menu == 1 else (255, 255, 255)
        
        texto_iniciar = fonte_opcao.render("► INICIAR" if opcao_menu == 0 else "  INICIAR", True, cor_iniciar)
        texto_sair = fonte_opcao.render("► SAIR" if opcao_menu == 1 else "  SAIR", True, cor_sair)
        
        TELA.blit(texto_iniciar, (LARGURA//2 - 80, ALTURA//2 + 20))
        TELA.blit(texto_sair, (LARGURA//2 - 80, ALTURA//2 + 80))
        
        fonte_info = pygame.font.Font(CAMINHO_FONTE, 28)
        info = fonte_info.render("Use SETAS e ENTER para navegar", True, (150, 150, 150))
        TELA.blit(info, (LARGURA//2 - info.get_width()//2, ALTURA - 50))
    
    elif estado == "jogando":
        # Desenhar sprites apenas quando jogando
        todos_sprites.draw(TELA)
        tiros_inimigos.draw(TELA)
        
        if jogador.vida < 2:
            texto = font.render(
                f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, (255, 0, 0)
            )
        else:
            texto = font.render(
                f"Vida: {jogador.vida}  |  Pontos: {pontos}", True, (255, 255, 255)
            )
        TELA.blit(texto, (10, 10))

        bonus_msgs = []
        if jogador.velocidade_timer > 0:
            bonus_msgs.append(f"Velocidade {jogador.velocidade_timer // FPS + 1}s")
        if jogador.tiro_triplo_timer > 0:
            bonus_msgs.append(f"Tiro triplo {jogador.tiro_triplo_timer // FPS + 1}s")
        if bonus_msgs:
            texto_power = font.render(
                "Power-ups: " + " | ".join(bonus_msgs), True, (0, 200, 255)
            )
            TELA.blit(texto_power, (10, 40))

        # Mostrar fase atual
        if fase_atual == 5:
            # Texto especial para Fase do Caos
            fonte_caos = pygame.font.Font(CAMINHO_FONTE, 40)
            texto_fase = fonte_caos.render("!!! FASE DO CAOS !!!", True, (255, 0, 255))
            TELA.blit(texto_fase, (LARGURA - texto_fase.get_width() - 10, 10))
            
            # Contador de tempo restante
            tempo_restante = (FASES[5]["duracao"] - temporizador_spawn) // FPS
            texto_tempo = font.render(f"Tempo: {tempo_restante}s", True, (255, 255, 0))
            TELA.blit(texto_tempo, (LARGURA - texto_tempo.get_width() - 10, 60))
        else:
            texto_fase = font.render(FASES[fase_atual]["nome"], True, (255, 255, 0))
            TELA.blit(texto_fase, (LARGURA - texto_fase.get_width() - 10, 10))
        
        # Mostrar barra de vida do boss se estiver ativo
        if boss_ativo:
            for inimigo in inimigos:
                if isinstance(inimigo, Boss):
                    # Desenhar barra de vida manualmente
                    barra_largura = 300
                    barra_altura = 20
                    x = (LARGURA - barra_largura) // 2
                    y = 50
                    # fundo
                    pygame.draw.rect(TELA, (100, 0, 0), (x, y, barra_largura, barra_altura))
                    # vida atual
                    vida_atual = int((inimigo.vida / inimigo.vida_max) * barra_largura)
                    pygame.draw.rect(TELA, (255, 0, 0), (x, y, vida_atual, barra_altura))
                    # borda
                    pygame.draw.rect(TELA, (255, 255, 255), (x, y, barra_largura, barra_altura), 2)
                    texto_boss = font.render("BOSS", True, (255, 255, 255))
                    TELA.blit(texto_boss, (x + barra_largura // 2 - texto_boss.get_width() // 2, y - 25))
                    break

    elif estado == "pausado":
        # Overlay de pausa
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        TELA.blit(overlay, (0, 0))
        
        fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 80)
        fonte_titulo.set_bold(True)

        fonte_opcao = pygame.font.Font(CAMINHO_FONTE, 50)
        
        titulo = fonte_titulo.render("PAUSADO", True, (255, 255, 0))
        TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2 - 120))

        cor_continuar = (255, 255, 0) if opcao_pausa == 0 else (255, 255, 255)
        cor_sair = (255, 255, 0) if opcao_pausa == 1 else (255, 255, 255)

        texto_continuar = fonte_opcao.render(
            "► CONTINUAR" if opcao_pausa == 0 else "  CONTINUAR", True, cor_continuar
        )
        texto_sair = fonte_opcao.render(
            "► SAIR" if opcao_pausa == 1 else "  SAIR", True, cor_sair
        )

        TELA.blit(texto_continuar, (LARGURA // 2 - 120, ALTURA // 2))
        TELA.blit(texto_sair, (LARGURA // 2 - 120, ALTURA // 2 + 70))

    elif estado == "game_over":
        # Tela de Game Over
        fonte_grande = pygame.font.Font(CAMINHO_FONTE, 72)
        fonte_media = pygame.font.Font(CAMINHO_FONTE, 40)
        texto_gameover = fonte_grande.render("GAME OVER", True, (255, 0, 0))
        texto_pontos = fonte_media.render(f"Pontuação: {pontos}", True, (255, 255, 255))
        texto_restart = fonte_media.render(
            "Aperte ESPAÇO para voltar ao menu", True, (0, 255, 255)
        )

        # overlay escuro
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        TELA.blit(overlay, (0, 0))

        TELA.blit(
            texto_gameover,
            (LARGURA // 2 - texto_gameover.get_width() // 2, ALTURA // 2 - 120),
        )
        TELA.blit(
            texto_pontos,
            (LARGURA // 2 - texto_pontos.get_width() // 2, ALTURA // 2 - 40),
        )
        TELA.blit(
            texto_restart,
            (LARGURA // 2 - texto_restart.get_width() // 2, ALTURA // 2 + 40),
        )

    elif estado == "transicao_caos":
        # Tela de Transição para Fase Secreta
        fonte_enorme = pygame.font.Font(CAMINHO_FONTE, 60)
        
        # Texto principal
        texto_parabens = fonte_enorme.render("PARABÉNS!", True, (255, 215, 0))
        texto_desbloqueio = fonte_enorme.render("VOCÊ DESBLOQUEOU A", True, (255, 255, 255))
        texto_fase_secreta = fonte_enorme.render("FASE SECRETA", True, (255, 0, 255))
        
        # Overlay escuro
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        TELA.blit(overlay, (0, 0))
        
        # Efeito de pulsação no texto
        pulso = abs(int((timer_transicao_caos % 60) - 30)) / 30
        alpha = int(150 + 105 * pulso)
        
        texto_parabens.set_alpha(alpha)
        texto_desbloqueio.set_alpha(255)
        texto_fase_secreta.set_alpha(alpha)
        
        TELA.blit(texto_parabens, (LARGURA//2 - texto_parabens.get_width()//2, ALTURA//2 - 150))
        TELA.blit(texto_desbloqueio, (LARGURA//2 - texto_desbloqueio.get_width()//2, ALTURA//2 - 50))
        TELA.blit(texto_fase_secreta, (LARGURA//2 - texto_fase_secreta.get_width()//2, ALTURA//2 + 50))

    elif estado == "vitoria":
        # Tela de Vitória
        fonte_grande = pygame.font.Font(CAMINHO_FONTE, 72)
        fonte_media = pygame.font.Font(CAMINHO_FONTE, 40)
        fonte_pequena = pygame.font.Font(CAMINHO_FONTE, 28)
        
        # Mensagem especial se completou a Fase do Caos
        if fase_caos_desbloqueada:
            texto_vitoria = fonte_grande.render("MESTRE DO CAOS!", True, (255, 0, 255))
            texto_extra = fonte_media.render("Você dominou a Fase Secreta!", True, (0, 255, 255))
        else:
            texto_vitoria = fonte_grande.render("VITÓRIA!", True, (0, 255, 0))
            texto_extra = None
            
        texto_pontos = fonte_media.render(f"Pontuação: {pontos}", True, (255, 255, 255))
        texto_restart = fonte_pequena.render(
            "Aperte ESPAÇO para voltar ao menu", True, (255, 255, 0)
        )

        # overlay escuro
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        TELA.blit(overlay, (0, 0))
        
        TELA.blit(texto_vitoria, (LARGURA//2 - texto_vitoria.get_width()//2, ALTURA//2 - 180))
        if texto_extra:
            TELA.blit(texto_extra, (LARGURA//2 - texto_extra.get_width()//2, ALTURA//2 - 80))
        TELA.blit(texto_pontos, (LARGURA//2 - texto_pontos.get_width()//2, ALTURA//2 - 20))
        TELA.blit(texto_restart, (LARGURA//2 - texto_restart.get_width()//2, ALTURA//2 + 40))

    # Fade overlay global (para todas as transições)
    if fade_alpha > 0:
        fade_overlay = pygame.Surface((LARGURA, ALTURA))
        fade_overlay.fill((0, 0, 0))
        fade_overlay.set_alpha(fade_alpha)
        TELA.blit(fade_overlay, (0, 0))

    pygame.display.flip()

pygame.quit()
