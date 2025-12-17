import pygame


class Entidade(pygame.sprite.Sprite):
    """
    Classe base para todas as entidades do jogo
    Demonstra: Herança, Encapsulamento
    """
    def __init__(self, x, y, velocidade):
        super().__init__()
        self._velocidade = velocidade  # Encapsulamento com atributo privado
        self.image = pygame.Surface((40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self._vida = 1  # Vida padrão encapsulada
    
    # Propriedade para encapsulamento da velocidade
    @property
    def velocidade(self):
        """Getter da velocidade (encapsulamento)"""
        return self._velocidade
    
    @velocidade.setter
    def velocidade(self, valor):
        """Setter da velocidade com validação (encapsulamento)"""
        if valor >= 0:
            self._velocidade = valor
    
    # Propriedade para encapsulamento da vida
    @property
    def vida(self):
        """Getter da vida (encapsulamento)"""
        return self._vida
    
    @vida.setter
    def vida(self, valor):
        """Setter da vida com validação (encapsulamento)"""
        self._vida = max(0, valor)  # Vida nunca pode ser negativa

    def mover(self, dx, dy):
        """Move a entidade por um delta x e y"""
        self.rect.x += dx
        self.rect.y += dy
    
    def esta_vivo(self):
        """Verifica se a entidade está viva"""
        return self._vida > 0
    
    def receber_dano(self, quantidade=1):
        """
        Recebe dano (Polimorfismo - pode ser sobrescrito)
        Retorna True se morreu, False caso contrário
        """
        self._vida -= quantidade
        return self._vida <= 0