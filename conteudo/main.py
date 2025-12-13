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

# Cores para o menu
COR_FUNDO_MENU = (20, 15, 30)       # Roxo bem escuro
COR_TITULO_1 = (255, 160, 50)       # Laranja
COR_TITULO_2 = (50, 150, 255)       # Azul
COR_BOTAO_BG = (40, 40, 70)         # Azul acinzentado escuro
COR_BOTAO_HOVER = (60, 60, 100)     # Azul um pouco mais claro
COR_TEXTO = (255, 255, 255)         # Branco
COR_BORDA_HOVER = (255, 140, 0)     # Laranja para a borda

# Classe do Botão
class Button:
    def __init__(self, text, x, y, width, height, fonte):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = COR_BOTAO_BG
        self.hovered = False
        self.fonte = fonte

    def draw(self, surface):
        # Muda cor e borda se o mouse estiver em cima
        if self.hovered:
            pygame.draw.rect(surface, COR_BOTAO_HOVER, self.rect, border_radius=8)
            pygame.draw.rect(surface, COR_BORDA_HOVER, self.rect, 3, border_radius=8)
        else:
            pygame.draw.rect(surface, COR_BOTAO_BG, self.rect, border_radius=8)
            pygame.draw.rect(surface, (20, 20, 40), self.rect, 3, border_radius=8)

        # Renderiza o texto centralizado no botão
        text_surf = self.fonte.render(self.text, True, COR_TEXTO)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Classe do Slider para controle de volume
class Slider:
    def __init__(self, x, y, width, height, label, fonte):
        self.center_x = x  # Centro horizontal
        self.rect = pygame.Rect(x - width//2, y, width, height)  # Rect ajustado para estar centralizado
        self.label = label
        self.fonte = fonte
        self.value = 1.0  # Valor entre 0 e 1 (100% por padrão)
        self.dragging = False

    def draw(self, surface):
        # Desenhar label acima do slider, centralizado
        label_surf = self.fonte.render(self.label, True, COR_TEXTO)
        label_x = self.center_x - label_surf.get_width()//2
        surface.blit(label_surf, (label_x, self.rect.y - 50))
        
        # Desenhar barra de fundo
        pygame.draw.rect(surface, (50, 50, 50), self.rect, border_radius=5)
        
        # Desenhar barra preenchida
        filled_width = int(self.rect.width * self.value)
        filled_rect = pygame.Rect(self.rect.x, self.rect.y, filled_width, self.rect.height)
        pygame.draw.rect(surface, COR_TITULO_1, filled_rect, border_radius=5)
        
        # Desenhar círculo do slider
        slider_x = self.rect.x + filled_width
        pygame.draw.circle(surface, COR_BORDA_HOVER, (slider_x, self.rect.centery), 8)
        
        # Desenhar percentual à direita
        percent_text = self.fonte.render(f"{int(self.value * 100)}%", True, COR_TEXTO)
        surface.blit(percent_text, (self.rect.right + 20, self.rect.y - 5))

    def check_hover(self, mouse_pos):
        slider_rect = pygame.Rect(
            self.rect.x - 8,
            self.rect.y - 8,
            self.rect.width + 16,
            self.rect.height + 16
        )
        return slider_rect.collidepoint(mouse_pos)

    def start_drag(self, mouse_pos):
        if self.check_hover(mouse_pos):
            self.dragging = True
            self.update(mouse_pos)  # Atualizar imediatamente ao começar o drag

    def stop_drag(self):
        self.dragging = False

    def update(self, mouse_pos):
        if self.dragging:
            # Calcular novo valor baseado na posição do mouse
            relative_x = mouse_pos[0] - self.rect.x
            self.value = max(0, min(1, relative_x / self.rect.width))



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
estado = "menu"  # menu, opcoes, jogando, pausado, game_over, vitoria, transicao_caos
fade_alpha = 255  # Começa com tela preta para fade in inicial
fade_direcao = -1  # -1 = fade in (clarear)
fase_atual = 1
estado_anterior = None  # Para rastrear de onde veio para opções
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
    1: {"nome": "Fase 1: Iniciante", "duracao": 600, "robos": ["lento", "rapido"]},
    2: {
        "nome": "Fase 2: Saltadores",
        "duracao": 700,
        "robos": ["lento", "saltador", "ziguezague"],
    },
    3: {
        "nome": "Fase 3: Caçadores",
        "duracao": 900,
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
            random.randint(100, LARGURA - 100), -40, grupo_tiros=tiros_inimigos
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

# Carregar fonte para os botões do menu
CAMINHO_FONTE_MENU = os.path.join(os.path.dirname(__file__), "assets", "fonts", "PressStart2P-Regular.ttf")
try:
    fonte_botoes_menu = pygame.font.Font(CAMINHO_FONTE_MENU, 16)
except:
    fonte_botoes_menu = pygame.font.SysFont("arial", 16, bold=True)

# Criar botões do menu
botoes_menu = [
    Button("INICIAR JOGO", LARGURA//2 - 125, 420, 250, 50, fonte_botoes_menu),
    Button("OPÇÕES", LARGURA//2 - 125, 480, 250, 50, fonte_botoes_menu),
    Button("SAIR", LARGURA//2 - 125, 540, 250, 50, fonte_botoes_menu)
]

# Criar sliders para opções
try:
    fonte_slider = pygame.font.Font(CAMINHO_FONTE_MENU, 14)
except:
    fonte_slider = pygame.font.SysFont("arial", 14, bold=True)

sliders = [
    Slider(LARGURA//2, 420, 200, 20, "VOLUME MUSICA  ", fonte_slider),
    Slider(LARGURA//2, 550, 200, 20, "VOLUME EFEITOS", fonte_slider)
]

# Botão voltar no menu de opções
botao_voltar = Button("VOLTAR", LARGURA//2 - 75, 600, 150, 50, fonte_botoes_menu)

# Criar botões do menu de pausa
botoes_pausa = [
    Button("CONTINUAR", LARGURA//2 - 125, 320, 250, 50, fonte_botoes_menu),
    Button("OPÇÕES", LARGURA//2 - 125, 380, 250, 50, fonte_botoes_menu),
    Button("SAIR", LARGURA//2 - 125, 440, 250, 50, fonte_botoes_menu)
]

# Botão voltar no game over e vitória
botao_voltar_menu = Button("VOLTAR AO MENU", LARGURA//2 - 125, 420, 250, 50, fonte_botoes_menu)

rodando = True
while rodando:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if estado == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for btn in botoes_menu:
                    if btn.is_clicked(mouse_pos):
                        if btn.text == "INICIAR JOGO":
                            resetar_jogo()
                        elif btn.text == "OPÇÕES":
                            estado = "opcoes"
                        elif btn.text == "SAIR":
                            rodando = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for slider in sliders:
                    slider.stop_drag()

        elif estado == "opcoes":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if botao_voltar.is_clicked(mouse_pos):
                    estado = estado_anterior if estado_anterior else "menu"
                    estado_anterior = None
                for slider in sliders:
                    slider.start_drag(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                for slider in sliders:
                    slider.stop_drag()
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                # Apenas atualizar sliders que estão sendo arrastados
                for i, slider in enumerate(sliders):
                    slider.update(mouse_pos)
                # Atualizar volumes em tempo real baseado em cada slider
                pygame.mixer.music.set_volume(sliders[0].value)
                SOM_LASER.set_volume(sliders[1].value)
                SOM_EXPLOSAO.set_volume(sliders[1].value)

        elif estado == "jogando":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    estado = "pausado"

        elif estado == "pausado":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for btn in botoes_pausa:
                    if btn.is_clicked(mouse_pos):
                        if btn.text == "CONTINUAR":
                            estado = "jogando"
                        elif btn.text == "OPÇÕES":
                            estado_anterior = "pausado"
                            estado = "opcoes"
                        elif btn.text == "SAIR":
                            estado = "menu"
                            opcao_menu = 0

        elif estado == "game_over" or estado == "vitoria":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if botao_voltar_menu.is_clicked(mouse_pos):
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
                boss = Boss(LARGURA // 2, -100, grupo_tiros=tiros_inimigos, jogador_alvo=jogador)
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
                    robo = RoboZigueZague(random.randint(100, LARGURA - 100), -40, grupo_tiros=tiros_inimigos)
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
       # colisão tiro jogador x robo (hitbox ajustada)
       for inimigo in inimigos:
        for tiro in tiros:
            hitbox_tiro = tiro.rect.inflate(-8, -8)

            if hitbox_tiro.colliderect(inimigo.rect):
                tiro.kill()

                if isinstance(inimigo, Boss):
                    morreu, dropar_powerup = inimigo.receber_dano()
                    if morreu:
                        explosao = Explosao(inimigo.rect.centerx, inimigo.rect.centery)
                        todos_sprites.add(explosao)
                        pontos += 1000
                        boss_ativo = False
                        SOM_EXPLOSAO.play()
                else:
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
        # Menu com botões - usando background do jogo
        TELA.blit(BACKGROUND, (0, 0))
        
        # Overlay escuro para melhor legibilidade do texto
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(80)
        overlay.fill((0, 0, 0))
        TELA.blit(overlay, (0, 0))
        
        # Carregar fonte para título
        CAMINHO_FONTE = os.path.join(os.path.dirname(__file__), "assets", "fonts", "PressStart2P-Regular.ttf")
        try:
            fonte_titulo_grande = pygame.font.Font(CAMINHO_FONTE, 45)
        except:
            fonte_titulo_grande = pygame.font.SysFont("arial", 45, bold=True)
        
        # Desenhar título com estilo de duas cores
        titulo1 = fonte_titulo_grande.render("JORNADA COSMICA", True, COR_TITULO_1)
        TELA.blit(titulo1, (LARGURA//2 - titulo1.get_width()//2, ALTURA//2 - 100))
        
        # Atualizar e desenhar botões
        mouse_pos = pygame.mouse.get_pos()
        for btn in botoes_menu:
            btn.check_hover(mouse_pos)
            btn.draw(TELA)
    
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
            fonte_caos = pygame.font.Font(CAMINHO_FONTE, 20)
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
        
        fonte_titulo = pygame.font.Font(CAMINHO_FONTE, 40)
        fonte_titulo.set_bold(True)
        
        titulo = fonte_titulo.render("PAUSADO", True, (255, 255, 0))
        TELA.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, ALTURA // 2 - 150))
        
        # Desenhar botões de pausa
        mouse_pos = pygame.mouse.get_pos()
        for btn in botoes_pausa:
            btn.check_hover(mouse_pos)
            btn.draw(TELA)

    elif estado == "game_over":
        # Tela de Game Over
        fonte_grande = pygame.font.Font(CAMINHO_FONTE, 36)
        fonte_media = pygame.font.Font(CAMINHO_FONTE, 20)
        texto_gameover = fonte_grande.render("GAME OVER", True, (255, 0, 0))
        texto_pontos = fonte_media.render(f"Pontuação: {pontos}", True, (255, 255, 255))

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
        
        # Desenhar botão voltar
        mouse_pos = pygame.mouse.get_pos()
        botao_voltar_menu.check_hover(mouse_pos)
        botao_voltar_menu.draw(TELA)

    elif estado == "transicao_caos":
        # Tela de Transição para Fase Secreta
        fonte_enorme = pygame.font.Font(CAMINHO_FONTE, 30)
        
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

    elif estado == "opcoes":
        # Menu de opções
        TELA.blit(BACKGROUND, (0, 0))
        
        # Overlay escuro
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(80)
        overlay.fill((0, 0, 0))
        TELA.blit(overlay, (0, 0))
        
        # Título
        CAMINHO_FONTE = os.path.join(os.path.dirname(__file__), "assets", "fonts", "PressStart2P-Regular.ttf")
        try:
            fonte_titulo_opcoes = pygame.font.Font(CAMINHO_FONTE, 45)
        except:
            fonte_titulo_opcoes = pygame.font.SysFont("arial", 45, bold=True)
        
        titulo_opcoes = fonte_titulo_opcoes.render("OPÇÕES", True, COR_TITULO_1)
        TELA.blit(titulo_opcoes, (LARGURA//2 - titulo_opcoes.get_width()//2, ALTURA//2-125))
        
        # Desenhar sliders
        for slider in sliders:
            slider.draw(TELA)
        
        # Desenhar botão voltar
        mouse_pos = pygame.mouse.get_pos()
        botao_voltar.check_hover(mouse_pos)
        botao_voltar.draw(TELA)

    elif estado == "vitoria":
        # Tela de Vitória
        fonte_grande = pygame.font.Font(CAMINHO_FONTE, 36)
        fonte_media = pygame.font.Font(CAMINHO_FONTE, 20)
        
        # Mensagem especial se completou a Fase do Caos
        if fase_caos_desbloqueada:
            texto_vitoria = fonte_grande.render("MESTRE DO CAOS!", True, (255, 0, 255))
            texto_extra = fonte_media.render("Você dominou a Fase Secreta!", True, (0, 255, 255))
        else:
            texto_vitoria = fonte_grande.render("VITÓRIA!", True, (0, 255, 0))
            texto_extra = None
            
        texto_pontos = fonte_media.render(f"Pontuação: {pontos}", True, (255, 255, 255))

        # overlay escuro
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        TELA.blit(overlay, (0, 0))
        
        TELA.blit(texto_vitoria, (LARGURA//2 - texto_vitoria.get_width()//2, ALTURA//2 - 180))
        if texto_extra:
            TELA.blit(texto_extra, (LARGURA//2 - texto_extra.get_width()//2, ALTURA//2 - 80))
        TELA.blit(texto_pontos, (LARGURA//2 - texto_pontos.get_width()//2, ALTURA//2 - 20))
        
        # Desenhar botão voltar
        mouse_pos = pygame.mouse.get_pos()
        botao_voltar_menu.check_hover(mouse_pos)
        botao_voltar_menu.draw(TELA)

    # Fade overlay global (para todas as transições)
    if fade_alpha > 0:
        fade_overlay = pygame.Surface((LARGURA, ALTURA))
        fade_overlay.fill((0, 0, 0))
        fade_overlay.set_alpha(fade_alpha)
        TELA.blit(fade_overlay, (0, 0))

    pygame.display.flip()

pygame.quit()
