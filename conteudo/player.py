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


class Jogador(Entidade):
    """
    Classe do Jogador
    Demonstra: Herança (de Entidade), Encapsulamento, Polimorfismo
    """
    def __init__(self, x, y):
        super().__init__(x, y, 7)
        
        # Carregar sprite
        sprite = pygame.image.load(CAMINHO_NAVE_PLAYER).convert_alpha()
        self.image = pygame.transform.scale(sprite, TAMANHO_NAVE_PLAYER)
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.inflate(-20, -20)
        
        # Atributos privados (encapsulamento)
        self._vida = 10
        self._velocidade_base = 10
        self._velocidade = self._velocidade_base
        self._velocidade_timer = 0
        self._tiro_triplo_timer = 0
    
    # Propriedades para encapsulamento
    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self, valor):
        self._vida = max(0, min(10, valor))  # Limita entre 0 e 10
    
    @property
    def velocidade(self):
        return self._velocidade
    
    @velocidade.setter
    def velocidade(self, valor):
        self._velocidade = max(1, valor)
    
    @property
    def velocidade_timer(self):
        return self._velocidade_timer
    
    @velocidade_timer.setter
    def velocidade_timer(self, valor):
        self._velocidade_timer = max(0, valor)
    
    @property
    def tiro_triplo_timer(self):
        return self._tiro_triplo_timer
    
    @tiro_triplo_timer.setter
    def tiro_triplo_timer(self, valor):
        self._tiro_triplo_timer = max(0, valor)
    
    @property
    def tiro_triplo_ativo(self) -> bool:
        """Verifica se o tiro triplo está ativo"""
        return self._tiro_triplo_timer > 0
    
    def update(self):
        """Atualiza o jogador (Polimorfismo - sobrescreve método da classe pai)"""
        self._processar_input()
        self._limitar_posicao()
        self._atualizar_timers()
        self.hitbox.center = self.rect.center
    
    def _processar_input(self):
        """Método privado para processar input do teclado (encapsulamento)"""
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            self.mover(0, -self._velocidade)
        if keys[pygame.K_s]:
            self.mover(0, self._velocidade)
        if keys[pygame.K_a]:
            self.mover(-self._velocidade, 0)
        if keys[pygame.K_d]:
            self.mover(self._velocidade, 0)
    
    def _limitar_posicao(self):
        """Método privado para limitar posição na tela (encapsulamento)"""
        self.rect.x = max(0, min(self.rect.x, LARGURA - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, ALTURA - self.rect.height))
    
    def _atualizar_timers(self):
        """Método privado para atualizar timers de power-ups (encapsulamento)"""
        if self._velocidade_timer > 0:
            self._velocidade_timer -= 1
            if self._velocidade_timer == 0:
                self._velocidade = self._velocidade_base
        
        if self._tiro_triplo_timer > 0:
            self._tiro_triplo_timer -= 1
    
    def aplicar_powerup(self, tipo: str):
        """Aplica um power-up ao jogador"""
        if tipo == "velocidade":
            self._velocidade_timer += 600
            self._velocidade = self._velocidade_base + 4
        elif tipo == "vida":
            self.vida += 1  # Usa o setter que já limita
        elif tipo == "tiro_triplo":
            self._tiro_triplo_timer += 600
        else:
            raise ValueError(f"Power-up desconhecido: {tipo}")
    
    def receber_dano(self, quantidade=1):
        """Recebe dano (Polimorfismo - sobrescreve método da classe pai)"""
        self._vida -= quantidade
        return self._vida <= 0


class Tiro(Entidade):
    """
    Classe do Tiro do Jogador
    Demonstra: Herança (de Entidade), Encapsulamento, Polimorfismo
    """
    def __init__(self, x, y, dx=0):
        super().__init__(x, y, 10)
        self._dx = dx  # Encapsulamento
        
        # Carregar sprite do tiro
        CAMINHO_IMAGEM = os.path.join(
            os.path.dirname(__file__), 
            "assets", 
            "images", 
            "tiroJogador.png"
        )
        imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
        self.image = pygame.transform.rotate(imagem_original, +90)
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        """Atualiza o tiro (Polimorfismo - sobrescreve método da classe pai)"""
        self.rect.x += self._dx
        self.rect.y -= self._velocidade
        
        # Remove se sair da tela
        if (self.rect.y < -20 or 
            self.rect.x < -20 or 
            self.rect.x > LARGURA + 20):
            self.kill()
