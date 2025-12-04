import random
import pygame

from config import ALTURA
from entidade import Entidade


class PowerUp(Entidade):
    TIPOS = ("velocidade", "vida", "tiro_triplo")

    def __init__(self, x: int, y: int, tipo: str):
        super().__init__(x, y, velocidade=2)
        if tipo not in self.TIPOS:
            raise ValueError(f"Tipo de power-up inválido: {tipo}")
        self.tipo = tipo
        self.image = self._criar_imagem(tipo)
        self.rect = self.image.get_rect(center=self.rect.center)

    def _criar_imagem(self, tipo: str) -> pygame.Surface:
        """Cria uma marcação simples por tipo para facilitar o reconhecimento."""
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
        self.rect.y += self.velocidade
        if self.rect.y > ALTURA + 40:
            self.kill()


def gerar_tipo_powerup() -> str:
    """Escolhe um tipo com pesos simples."""
    return random.choices(
        PowerUp.TIPOS, weights=(0.45, 0.2, 0.35), k=1  # velocidade, vida, tiro triplo
    )[0]
