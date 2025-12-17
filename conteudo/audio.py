import os
import pygame


class GerenciadorAudio:
    """Gerencia todos os sons e músicas do jogo (Encapsulamento)"""
    
    def __init__(self, diretorio_base):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self._diretorio_base = diretorio_base
        self._volume_musica = 0.5
        self._volume_efeitos = 0.5
        self._musica_atual = None
        self._musica_fade_out = False
        self._musica_proxima = None
        self._musica_volume = 0.5
        
        # Carregar sons (encapsulamento)
        self._sons = self._carregar_sons()
        self._caminhos_musicas = self._obter_caminhos_musicas()
    
    def _carregar_sons(self):
        """Método privado para carregar sons (encapsulamento)"""
        sons = {}
        caminhos = {
            "laser": os.path.join(self._diretorio_base, "assets", "audios", "laser-shot.wav"),
            "explosao": os.path.join(self._diretorio_base, "assets", "audios", "explosao-nave.wav"),
            "vitoria": os.path.join(self._diretorio_base, "assets", "audios", "som_vitoria.mp3"),
            "derrota": os.path.join(self._diretorio_base, "assets", "audios", "som_derrota.mp3"),
        }
        
        for chave, caminho in caminhos.items():
            if os.path.exists(caminho):
                sons[chave] = pygame.mixer.Sound(caminho)
            else:
                sons[chave] = None
        
        # Configurar volumes padrão
        if sons.get("laser"):
            sons["laser"].set_volume(0.3)
        if sons.get("explosao"):
            sons["explosao"].set_volume(1.0)
        if sons.get("vitoria"):
            sons["vitoria"].set_volume(0.6)
        if sons.get("derrota"):
            sons["derrota"].set_volume(0.6)
        
        return sons
    
    def _obter_caminhos_musicas(self):
        """Método privado para obter caminhos das músicas (encapsulamento)"""
        return {
            "boss": os.path.join(self._diretorio_base, "assets", "audios", "trilha-sonora-boss.mp3"),
            "menu": os.path.join(self._diretorio_base, "assets", "audios", "menu.mp3"),
            "background": os.path.join(self._diretorio_base, "assets", "audios", "trilha-sonora-background.mp3"),
            "fase_secreta": os.path.join(self._diretorio_base, "assets", "audios", "trilha-sonora-fase-secreta.mp3"),
        }
    
    # Propriedades para encapsulamento
    @property
    def volume_musica(self):
        return self._volume_musica
    
    @volume_musica.setter
    def volume_musica(self, valor):
        self._volume_musica = max(0.0, min(1.0, valor))
        pygame.mixer.music.set_volume(self._volume_musica)
    
    @property
    def volume_efeitos(self):
        return self._volume_efeitos
    
    @volume_efeitos.setter
    def volume_efeitos(self, valor):
        self._volume_efeitos = max(0.0, min(1.0, valor))
        for chave in ["laser", "explosao", "vitoria", "derrota"]:
            if self._sons.get(chave):
                if chave == "laser":
                    self._sons[chave].set_volume(0.3 * self._volume_efeitos)
                else:
                    self._sons[chave].set_volume(self._volume_efeitos)
    
    def tocar_som(self, nome):
        """Toca um efeito sonoro"""
        if self._sons.get(nome):
            self._sons[nome].play()
    
    def tocar_musica(self, tipo, loop=-1):
        """Toca uma música específica"""
        caminho = self._caminhos_musicas.get(tipo)
        if caminho and os.path.exists(caminho):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(caminho)
            pygame.mixer.music.set_volume(self._volume_musica)
            pygame.mixer.music.play(loop)
            self._musica_atual = tipo
    
    def parar_musica(self):
        """Para a música atual"""
        pygame.mixer.music.stop()
        self._musica_atual = None
    
    def fade_out_musica(self, musica_proxima):
        """Inicia fade out da música atual"""
        self._musica_fade_out = True
        self._musica_proxima = musica_proxima
    
    def atualizar(self):
        """Atualiza o sistema de fade"""
        if self._musica_fade_out:
            self._musica_volume -= 0.02
            if self._musica_volume <= 0:
                self._musica_volume = 0
                pygame.mixer.music.stop()
                
                # Carregar e tocar próxima música
                if self._musica_proxima:
                    self.tocar_musica(self._musica_proxima)
                    self._musica_fade_out = False
                    self._musica_proxima = None
            else:
                pygame.mixer.music.set_volume(self._musica_volume)
        elif self._musica_atual == "fase_secreta" and self._musica_volume < 0.5:
            # Fade in da música da fase secreta
            self._musica_volume += 0.02
            if self._musica_volume > 0.5:
                self._musica_volume = 0.5
            pygame.mixer.music.set_volume(self._musica_volume)


# Funções legadas para compatibilidade (podem ser removidas depois)
def inicializar_audio(diretorio_base):
    gerenciador = GerenciadorAudio(diretorio_base)
    return gerenciador._sons, gerenciador._caminhos_musicas["boss"], gerenciador._caminhos_musicas["menu"]


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
