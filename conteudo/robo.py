from entidade import Entidade
from config import LARGURA, ALTURA


# ROBO BASE
class Robo(Entidade):
    def __init__(self, x, y, velocidade):
        super().__init__(x, y, velocidade)
        self.image.fill((255, 255, 255))  # branco

    def atualizar_posicao(self):
        raise NotImplementedError

# ROBO LENTO
class RoboLento(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade = 1.5)
        self.image.fill((255, 0, 111))
    
    def atualizar_posicao(self):
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

# ROBO LENTO
class RoboRapido(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade = 3)
        self.image.fill((255, 0, 0))
    
    def atualizar_posicao(self):
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

# ROBO EXEMPLO — ZigueZague
class RoboZigueZague(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade = 2)
        self.direcao = 1

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao * 3

        if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()