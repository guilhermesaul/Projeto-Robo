import random
import pygame

from config import ALTURA
from entidade import Entidade


class PowerUp(Entidade):
    """
    Classe PowerUp
    Demonstra: Herança (de Entidade), Encapsulamento, Polimorfismo
    """
    TIPOS = ("velocidade", "vida", "tiro_triplo")

    def __init__(self, x: int, y: int, tipo: str):
        super().__init__(x, y, velocidade=2)
        
        if tipo not in self.TIPOS:
            raise ValueError(f"Tipo de power-up inválido: {tipo}")
        
        self._tipo = tipo  # Encapsulamento
        self.image = self._criar_imagem(tipo)
        self.rect = self.image.get_rect(center=self.rect.center)
    
    # Propriedade para encapsulamento do tipo
    @property
    def tipo(self):
        """Getter do tipo (encapsulamento - somente leitura)"""
        return self._tipo

    def _criar_imagem(self, tipo: str) -> pygame.Surface:
        """
        Método privado para criar imagem (encapsulamento)
        Cria uma marcação simples por tipo para facilitar o reconhecimento
        """
        cores = {
            "velocidade": (0, 200, 255),
            "vida": (0, 220, 0),
            "tiro_triplo": (255, 180, 0),
        }
        letras = {
            "velocidade": "S",  # Speed
            "vida": "+",
            "tiro_triplo": "T",
        }
        
        surface = pygame.Surface((28, 28), pygame.SRCALPHA)
        pygame.draw.rect(surface, cores[tipo], surface.get_rect(), border_radius=6)
        
        fonte = pygame.font.SysFont(None, 22)
        texto = fonte.render(letras[tipo], True, (15, 15, 15))
        texto_rect = texto.get_rect(center=surface.get_rect().center)
        surface.blit(texto, texto_rect)
        
        return surface

    def update(self):
        """Atualiza o power-up (Polimorfismo - sobrescreve método da classe pai)"""
        self.rect.y += self._velocidade
        
        # Remove se sair da tela
        if self.rect.y > ALTURA + 40:
            self.kill()


class FabricaPowerUp:
    """
    Factory para criação de PowerUps
    Demonstra: Padrão de Projeto Factory, Encapsulamento
    """
    _PESOS = (0.45, 0.2, 0.35)  # velocidade, vida, tiro triplo
    
    @classmethod
    def gerar_tipo(cls) -> str:
        """Escolhe um tipo de power-up com pesos definidos"""
        return random.choices(PowerUp.TIPOS, weights=cls._PESOS, k=1)[0]
    
    @classmethod
    def criar(cls, x: int, y: int) -> PowerUp:
        """Cria um power-up aleatório na posição especificada"""
        tipo = cls.gerar_tipo()
        return PowerUp(x, y, tipo)


# Função legada para compatibilidade (pode ser removida depois)
def gerar_tipo_powerup() -> str:
    """Escolhe um tipo com pesos simples."""
    return FabricaPowerUp.gerar_tipo()
