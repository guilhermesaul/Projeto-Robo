import pygame
import math
import os
import random
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
        self.image.fill((100, 100, 255))  # azul claro

    def atualizar_posicao(self):
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA:
            self.kill()

# ROBO RAPIDO
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
            
    

#ROBO CICLICO


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

# ROBO SALTADOR — faz "pulos" aleatórios
class RoboSaltador(Robo):
    def __init__(self, x, y):
        super().__init__(x, y, velocidade = 2)
        self.cor_base = (255, 165, 0)
        self.image.fill(self.cor_base)  # laranja
        self.velocidade_vertical = self.velocidade
        self.gravidade = 0.3
        self.posicao_y = float(y)
        self.tempo_teleporte = 0
        self.intervalo_teleporte_minimo = 50
        self.intervalo_teleporte_maximo = 140
        self.proximo_teleporte = random.randint(self.intervalo_teleporte_minimo, self.intervalo_teleporte_maximo)
        self.flash_duracao = 10
        self.flash_timer = 0

    def atualizar_posicao(self):
        # contador para teleporte
        self.tempo_teleporte += 1
        if self.tempo_teleporte >= self.proximo_teleporte:
            novo_x = random.randint(0, LARGURA - 40)
            novo_y = random.randint(0, ALTURA // 2)
            self.rect.x = novo_x
            self.posicao_y = float(novo_y)
            self.rect.y = novo_y
            self.tempo_teleporte = 0
            self.proximo_teleporte = random.randint(self.intervalo_teleporte_minimo, self.intervalo_teleporte_maximo)
            self.flash_timer = self.flash_duracao

        # atualização da posição vertical (descida leve)
        self.velocidade_vertical += self.gravidade
        if self.velocidade_vertical > 4:
            self.velocidade_vertical = 4
        self.posicao_y += self.velocidade_vertical
        self.rect.y = int(self.posicao_y)

        # efeito de flash alternando cor durante o teleporte
        if self.flash_timer > 0:
            if self.flash_timer % 2 == 0:
                self.image.fill((255, 255, 255))  # flash branco
            else:
                self.image.fill(self.cor_base)
            self.flash_timer -= 1
        else:
            self.image.fill(self.cor_base)

    def update(self):
        self.atualizar_posicao()
        # se sair por baixo ou bater no topo, mata
        if self.rect.y > ALTURA or self.rect.y < -60:
            self.kill()

# ROBO CAÇADOR — segue o jogador
class RoboCacador(Robo):
    def __init__(self, x, y, alvo):
        super().__init__(x, y, velocidade = 2.2)
        self.image.fill((200, 0, 200))  # magenta
        self.alvo = alvo

    def atualizar_posicao(self):
        diferenca_x = self.alvo.rect.centerx - self.rect.centerx
        diferenca_y = self.alvo.rect.centery - self.rect.centery
        distancia = math.hypot(diferenca_x, diferenca_y)
        if distancia > 0:
            normal_x = diferenca_x / distancia
            normal_y = diferenca_y / distancia
            self.rect.x += normal_x * self.velocidade * 2
            self.rect.y += normal_y * self.velocidade
        else:
            self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        if self.rect.y > ALTURA + 80 or self.rect.y < -80:
            self.kill()

