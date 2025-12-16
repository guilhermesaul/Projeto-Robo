import pygame
import math
import os
import random
from entidade import Entidade
from config import LARGURA, ALTURA

# Classe para os tiros do Boss (maiores e com ângulo)
class TiroBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, vy, vx=0):
        super().__init__()
        # Tiro do Boss maior: 16x24
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__), "assets", "images", "shot_exp1.png")
        imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
        self.image = pygame.transform.rotate(imagem_original, -90)
        self.image = pygame.transform.scale(self.image, (74, 74))
        self.rect = self.image.get_rect(center=(x, y))
        self.vy = vy
        self.vx = vx

    def update(self):
        self.rect.y += self.vy
        self.rect.x += self.vx
        if (self.rect.top > ALTURA or 
            self.rect.right < -50 or 
            self.rect.left > LARGURA + 50):
            self.kill()

# ROBO BASE
class Robo(Entidade):
    def __init__(self, x, y, velocidade, grupo_tiros=None):
        super().__init__(x, y, velocidade)
        self.image.fill((255, 255, 255))
        self.grupo_tiros = grupo_tiros
        self.tiro_timer = random.randint(40, 160)
        self.vel_tiro = 6

    def atualizar_posicao(self):
        raise NotImplementedError

    def tentar_atirar(self):
        if self.grupo_tiros is None:
            return
        
        self.tiro_timer -= 1
        if self.tiro_timer <= 0:
            x, y = self.ponto_de_tiro()
            tiro = TiroRobo(x, y, velocidade=self.vel_tiro)
            self.grupo_tiros.add(tiro)
            self.tiro_timer = random.randint(50, 180)

    def ponto_de_tiro(self):
        return (self.rect.centerx, self.rect.bottom - 10)
    

# TIRO DO ROBO
class TiroRobo(Entidade):
    def __init__(self, x, y, velocidade=6):
        super().__init__(x, y, velocidade)
        self.image = pygame.Surface((10, 18))
        self.image.fill((255, 0, 0))
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__), "assets", "images", "shot_exp1.png")
        imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
        self.image = pygame.transform.rotate(imagem_original, -90)
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.y > ALTURA:
            self.kill()

# ROBO LENTO
class RoboLento(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade = 1.5, grupo_tiros=grupo_tiros)
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__),"assets", "images", "roboLento.png")
        try:
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (56,100 ))
        except:
            pass
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = (x, y)

    def atualizar_posicao(self):
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()
        if self.rect.y > ALTURA:
            self.kill()
        # Saída pela base é tratada no loop principal


# ROBO RAPIDO
class RoboRapido(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade = 3, grupo_tiros=grupo_tiros)
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__),"assets", "images", "roboRapido.png")
        try:
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (64, 115))
        except:
            pass
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = (x, y)

    def atualizar_posicao(self):
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()
        # Saída pela base é tratada no loop principal


# ROBO ZIGUEZAGUE
class RoboZigueZague(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade = 2, grupo_tiros=grupo_tiros)
        self.direcao = 1
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__),"assets", "images", "roboZigue.png")
        try:
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (64, 100))
        except:
            pass
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center = (x, y)

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao * 3

        if self.rect.left <= 0 or self.rect.right >= LARGURA:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()
        if self.rect.y > ALTURA:
            self.kill()
        # Saída pela base é tratada no loop principal


# ROBO CICLICO
class RoboCiclico(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade=0, grupo_tiros=grupo_tiros)

        CAMINHO_IMAGEM = os.path.join(
            os.path.dirname(__file__),
            "assets", "images", "roboCiclico.png"
        )

        try:
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (45, 90))
        except:
            self.image = pygame.Surface((45, 90))
            self.image.fill((200, 50, 200))

        self.rect = self.image.get_rect(center=(x, y))

        # Dados do movimento circular
        self.centro_x = x
        self.centro_y = y
        self.raio = 60
        self.angulo = 0
        self.vel_angular = 0.05
        self.vel_descida = 1

    def atualizar_posicao(self):
        self.angulo += self.vel_angular
        self.centro_y += self.vel_descida

        self.rect.x = self.centro_x + math.cos(self.angulo) * self.raio
        self.rect.y = self.centro_y + math.sin(self.angulo) * self.raio

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()

        # remove quando sair da tela
        if self.rect.top > ALTURA + 60:
            self.kill()

# ROBO SALTADOR
class RoboSaltador(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade=2, grupo_tiros=grupo_tiros)

        try:
            CAMINHO_IMAGEM = os.path.join(
                os.path.dirname(__file__),
                "assets", "images", "roboSaltador.png"
            )
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (55, 110))
        except:
            self.image = pygame.Surface((55, 110))
            self.image.fill((100, 100, 255))

        self.rect = self.image.get_rect(center=(x, y))

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
            novo_x = random.randint(40, LARGURA - 40)
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

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()
        # Mata apenas se sair muito acima da tela; saída inferior é tratada no loop principal
        if self.rect.y < -60:
            self.kill()

# ROBO CAÇADOR
class RoboCacador(Robo):
    def __init__(self, x, y, jogador, grupo_tiros=None):
        super().__init__(x, y, velocidade=2, grupo_tiros=grupo_tiros)
        
        try:
            CAMINHO_IMAGEM = os.path.join(
                os.path.dirname(__file__),
                "assets", "images", "roboCacador.png"
            )
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (64, 128))
        except:
            self.image = pygame.Surface((64, 128))
            self.image.fill((255, 165, 0))

        self.rect = self.image.get_rect(center=(x, y))
        self.jogador = jogador


    def atualizar_posicao(self):
        diferenca_x = self.jogador.rect.centerx - self.rect.centerx
        diferenca_y = self.jogador.rect.centery - self.rect.centery
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
        self.tentar_atirar()
        if self.rect.top > ALTURA:
            self.kill()
# EXPLOSAO
class Explosao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.tamanho = 10
        self.image = pygame.Surface((self.tamanho * 2, self.tamanho * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.vida_util = 20
        
    def update(self):
        self.vida_util -= 1
        self.tamanho += 2
        
        tamanho_atual = int(self.tamanho)
        self.image = pygame.Surface((tamanho_atual * 2, tamanho_atual * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.rect.center)
        
        alpha = max(0, min(255, int(255 * (self.vida_util / 20))))
        cor = (255, random.randint(0, 150), 0, alpha)
        
        pygame.draw.circle(self.image, cor, (tamanho_atual, tamanho_atual), tamanho_atual)
        
        if self.vida_util <= 0:
         self.kill()

# BOSS
class Boss(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade=1, grupo_tiros=grupo_tiros)
        self.piscando = 0
        try:
            CAMINHO_IMAGEM = os.path.join(
                os.path.dirname(__file__),
                "assets",
                "images",
                "boss.png"
            )
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()

            self.image_original = pygame.transform.rotate(imagem_original, 180)
            self.image_original = pygame.transform.scale(self.image_original, (250, 250))

        except:
            self.image_original = pygame.Surface((250, 250))
            self.image_original.fill((80, 0, 80))

        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(center=(x, y))

        self.vida = 250  # vida do boss
        self.vida_max = 250
        self.direcao = 1
        self.vel_horizontal = 4  # mais rápido
        self.tiro_timer = 60  # intervalo inicial de tiro
        self.vel_tiro = 10  # tiros mais rápidos
        self.pos_y_alvo = ALTURA // 4  # fica no topo da tela
        self.descendo = True

    def atualizar_posicao(self):
        # desce até posição alvo, depois fica se movendo lateralmente
        if self.descendo:
            if self.rect.centery < self.pos_y_alvo:
                self.rect.y += self.velocidade * 2
            else:
                self.descendo = False
        else:
            # movimento lateral
            self.rect.x += self.direcao * self.vel_horizontal
            # Mantém o Boss sempre dentro da tela
            if self.rect.left <= 0:
                self.rect.left = 0
                self.direcao *= -1
            elif self.rect.right >= LARGURA:
                self.rect.right = LARGURA
                self.direcao *= -1
   
    def tentar_atirar(self):
        # Boss atira 5 tiros espalhados
        if self.grupo_tiros is None:
            return
       
        self.tiro_timer -= 1
        if self.tiro_timer <= 0:
            # 5 tiros espalhados
            for offset in [-60, -30, 0, 30, 60]:
                tiro = TiroBoss(self.rect.centerx + offset, self.rect.bottom, self.vel_tiro)
                self.grupo_tiros.add(tiro)
           
            self.tiro_timer = random.randint(60, 120)

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()

        if self.piscando > 0:
            self.piscando -= 1
            self.image = self.image_original
            self.image.set_alpha(160)  # mais transparente (efeito dano)
        else:
            self.image = self.image_original
            self.image.set_alpha(255)  # normal

       
    def receber_dano(self):
        self.vida -= 1
        self.piscando = 8  # quantidade de frames do efeito

        deve_dropar_powerup = random.random() < 0.05

        if self.vida <= 0:
            self.kill()
            return True, deve_dropar_powerup

        return False, deve_dropar_powerup

