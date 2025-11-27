import math
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

#ROBO CÍCLICO


class RoboCiclico(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade = 1)
        self.image.fill((0, 128, 255))  
        self.angulo = 0
        self.raio = 60

        self.centro_x = x
        self.centro_y = y

        self.direcao = 1
        self.vel_horizontal = 2  # velocidade do movimento para os lados

    def atualizar_posicao(self):
        # centro do círculo se move para os lados
        self.centro_x += self.direcao * self.vel_horizontal

        # se bater nas bordas, troca direção
        if self.centro_x <= 0 + self.raio or self.centro_x >= LARGURA - self.raio:
            self.direcao *= -1

        # movimento circular
        self.rect.x = self.centro_x + math.cos(self.angulo) * self.raio
        self.rect.y = self.centro_y + math.sin(self.angulo) * self.raio

        # avanço do círculo
        self.angulo += 0.1

        # o centro desce com o tempo
        self.centro_y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()
