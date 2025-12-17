import os
import pygame


def inicializar_audio(base_dir):
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    caminhos = {
        "laser": os.path.join(base_dir, "assets", "audios", "laser-shot.wav"),
        "explosao": os.path.join(base_dir, "assets", "audios", "explosao-nave.wav"),
        "boss": os.path.join(base_dir, "assets", "audios", "trilha-sonora-boss.mp3"),
        "menu": os.path.join(base_dir, "assets", "audios", "menu.mp3"),
    }

    sons = {}
    for chave in ("laser", "explosao"):
        caminho = caminhos[chave]
        if os.path.exists(caminho):
            sons[chave] = pygame.mixer.Sound(caminho)
        else:
            sons[chave] = None

    # volumes padrão
    if sons.get("laser"):
        sons["laser"].set_volume(0.3)
    if sons.get("explosao"):
        sons["explosao"].set_volume(1.0)

    return sons, caminhos["boss"], caminhos["menu"]


def tocar_musica_boss(caminho_musica_boss):
    if os.path.exists(caminho_musica_boss):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(caminho_musica_boss)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


def parar_musica():
    pygame.mixer.music.stop()


def tocar_musica_menu(caminho_menu):
    if os.path.exists(caminho_menu):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(caminho_menu)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)
