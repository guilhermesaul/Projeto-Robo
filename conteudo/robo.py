import pygame
import math
import os
import random
from entidade import Entidade
from config import LARGURA, ALTURA

# ROBO BASE
class Robo(Entidade):
    def __init__(self, x, y, velocidade, grupo_tiros=None):
        super().__init__(x, y, velocidade)
        self.image.fill((255, 255, 255))  # branco
        # grupo onde os tiros dos robôs serão adicionados (deve ser um pygame.sprite.Group)
        self.grupo_tiros = grupo_tiros
        # timer aleatório para atirar (em frames)
        self.tiro_timer = random.randint(40, 160)
        # velocidade dos tiros dos robôs (valor positivo -> vai para baixo)
        self.vel_tiro = 6

    def atualizar_posicao(self):
        raise NotImplementedError

    def tentar_atirar(self):
        # decrementa e, quando chega a zero, dispara e reseta o timer
        if self.grupo_tiros is None:
            return
        
        self.tiro_timer -= 1
        if self.tiro_timer <= 0:
            x, y = self.ponto_de_tiro()
            tiro = TiroRobo(x, y, velocidade=self.vel_tiro)
            self.grupo_tiros.add(tiro)
            # reseta timer com variação para não ficar previsível
            self.tiro_timer = random.randint(50, 180)

    def ponto_de_tiro(self):
        # ponto de saída do tiro na parte inferior da nave
        return (self.rect.centerx, self.rect.bottom - 10)
    

# TIRO DO ROBO
class TiroRobo(Entidade):
    def __init__(self, x, y, velocidade=6):
        super().__init__(x, y, velocidade)
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__),"assets", "images", "roboCiclico.png")
        imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
        self.image = pygame.transform.rotate(imagem_original, -90)
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(center=self.rect.center)
        # usa superfície menor para ficar mais parecido com um tiro
        self.image = pygame.Surface((6, 12))
        self.image.fill((255, 0, 0))  # vermelho
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
        imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
        self.image = pygame.transform.rotate(imagem_original, -90)
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(center=self.rect.center)

    def atualizar_posicao(self):
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()
        if self.rect.y > ALTURA:
            self.kill()


# ROBO RAPIDO
class RoboRapido(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade = 3, grupo_tiros=grupo_tiros)
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__),"assets", "images", "roboRapido.png")
        imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
        self.image = pygame.transform.rotate(imagem_original, -90)
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(center=self.rect.center)

    def atualizar_posicao(self):
        self.rect.y += self.velocidade

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()
        if self.rect.y > ALTURA:
            self.kill()


# ROBO EXEMPLO — ZigueZague
class RoboZigueZague(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade = 2, grupo_tiros=grupo_tiros)
        self.direcao = 1
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__),"assets", "images", "roboZigue.png")
        imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
        self.image = pygame.transform.rotate(imagem_original, -90)
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(center=self.rect.center)

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.rect.x += self.direcao * 3

        if self.rect.x <= 0 or self.rect.x >= LARGURA - 40:
            self.direcao *= -1

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()
        if self.rect.y > ALTURA:
            self.kill()


# ROBO CICLICO
class RoboCiclico(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade = 1, grupo_tiros=grupo_tiros)
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__),"assets", "images", "roboCiclico.png")
        imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
        self.image = pygame.transform.rotate(imagem_original, -90)
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(center=self.rect.center)
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
        self.tentar_atirar()
        if self.rect.y > ALTURA:
            self.kill()


# ROBO SALTADOR — faz "pulos" aleatórios
class RoboSaltador(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade = 2, grupo_tiros=grupo_tiros)
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__),"assets", "images", "roboCiclico.png")
        imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
        self.image = pygame.transform.rotate(imagem_original, -90)
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(center=self.rect.center)
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

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()
        # se sair por baixo ou bater no topo, mata
        if self.rect.y > ALTURA or self.rect.y < -60:
            self.kill()


# ROBO CAÇADOR — segue o jogador
class RoboCacador(Robo):
    def __init__(self, x, y, alvo, grupo_tiros=None):
        super().__init__(x, y, velocidade = 2.2, grupo_tiros=grupo_tiros)
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__),"assets", "images", "roboCacador.png")
        imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
        self.image = pygame.transform.rotate(imagem_original, -90)
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(center=self.rect.center)
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
        self.tentar_atirar()
        if self.rect.y > ALTURA + 80 or self.rect.y < -80:
            self.kill()
# BOSS
class Boss(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade=1, grupo_tiros=grupo_tiros)
        self.image = pygame.Surface((120, 120))
        self.image.fill((255, 255, 255))  # branco
        self.rect = self.image.get_rect(center=(x, y))
        self.vida = 50
        self.direcao = 1
        self.vel_horizontal = 3
        self.tiro_timer = 20  # atira mais rápido
        self.vel_tiro = 8
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
            if self.rect.left <= 0 or self.rect.right >= LARGURA:
                self.direcao *= -1

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()
        
    def receber_dano(self):
        self.vida -= 1
        # efeito visual de dano (pisca)
        if self.vida % 2 == 0:
            self.image.fill((255, 200, 200))
        else:
            self.image.fill((255, 255, 255))
        
        if self.vida <= 0:
            self.kill()
            return True
        
        return False
         


class Explosao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.frames = []
        self.frame_atual = 0

        for i in range(12):
            img = pygame.Surface((80, 80), pygame.SRCALPHA)

            # tamanho da explosão
            raio = 28 - i * 2
            if raio < 0:
                raio = 0

            cx, cy = 40, 40

            # cor e transparência
            cor = (180, 0, 255)
            alpha = max(220 - i * 15, 0)

            # forma irregular
            largura = raio * 2 + random.randint(-8, 8)
            altura  = raio * 2 + random.randint(-8, 8)

            pygame.draw.ellipse(
                img,
                (*cor, alpha),
                (cx - largura//2, cy - altura//2, largura, altura)
            )

            # pequenas partículas
            for _ in range(14):
                px = cx + random.randint(-raio // 2, raio // 2)
                py = cy + random.randint(-raio // 2, raio // 2)

                tamanho = random.randint(1, 2)
                alpha_p = max(130 - i * 15, 0)

                pygame.draw.circle(
                    img,
                    (200, 0, 255, alpha_p),
                    (px, py),
                    tamanho
                )

            self.frames.append(img)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.frame_atual += 0.6

        # remove quando acabar
        if self.frame_atual >= len(self.frames):
            self.kill()
            return

        self.image = self.frames[int(self.frame_atual)]

