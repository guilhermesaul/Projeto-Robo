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
        self.image = pygame.Surface((16, 24))
        self.image.fill((255, 50, 50))
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
            self.image = pygame.transform.scale(self.image, (128, 128))
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


# ROBO RAPIDO
class RoboRapido(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade = 3, grupo_tiros=grupo_tiros)
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__),"assets", "images", "roboRapido.png")
        try:
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (128, 128))
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


# ROBO ZIGUEZAGUE
class RoboZigueZague(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade = 2, grupo_tiros=grupo_tiros)
        self.direcao = 1
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__),"assets", "images", "roboZigue.png")
        try:
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (128, 128))
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


# ROBO CICLICO
class RoboCiclico(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade = 1, grupo_tiros=grupo_tiros)
        CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__),"assets", "images", "roboCiclico.png")
        try:
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (128, 128))
        except:
            pass
        self.rect = self.image.get_rect(center=(x, y))
        self.centro_x = x
        self.angulo = 0

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        self.angulo += 0.1
        self.rect.x = self.centro_x + math.sin(self.angulo) * 60

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()
        if self.rect.y > ALTURA:
            self.kill()


# ROBO SALTADOR
class RoboSaltador(Robo):
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade=4, grupo_tiros=grupo_tiros)
        try:
            CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__), "assets", "images", "roboSaltador.png")
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (128, 128))
        except:
            self.image.fill((100, 100, 255))
        
        self.rect = self.image.get_rect(center=(x, y))
        self.estado = "caindo"
        self.timer_salto = 0

    def atualizar_posicao(self):
        if self.estado == "caindo":
            self.rect.y += self.velocidade
            if random.randint(0, 100) < 2:
                self.estado = "parando"
                self.timer_salto = 40
        elif self.estado == "parando":
            self.timer_salto -= 1
            if self.timer_salto <= 0:
                self.estado = "caindo"

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()
        if self.rect.y > ALTURA:
            self.kill()


# ROBO CAÇADOR
class RoboCacador(Robo):
    def __init__(self, x, y, jogador, grupo_tiros=None):
        super().__init__(x, y, velocidade=2.5, grupo_tiros=grupo_tiros)
        self.jogador = jogador
        try:
            CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__), "assets", "images", "roboCacador.png")
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (128, 128))
        except:
            self.image.fill((255, 165, 0))

        self.rect = self.image.get_rect(center=(x, y))

    def atualizar_posicao(self):
        self.rect.y += self.velocidade
        
        if self.jogador:
            dx = self.jogador.rect.centerx - self.rect.centerx
            if dx > 0:
                self.rect.x += 1
            elif dx < 0:
                self.rect.x -= 1

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()
        if self.rect.y > ALTURA:
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


# BOSS FINAL
class Boss(Robo):
    def __init__(self, x, y, grupo_tiros=None, jogador_alvo=None):
        super().__init__(x, y, velocidade=2, grupo_tiros=grupo_tiros)
        
        self.jogador_alvo = jogador_alvo
        
        try:
            CAMINHO_IMAGEM = os.path.join(os.path.dirname(__file__), "assets", "images", "boss.png")
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image_original = pygame.transform.rotate(imagem_original, 180)
            self.image_original = pygame.transform.scale(self.image_original, (250, 250))
        except:
            self.image_original = pygame.Surface((220, 160))
            self.image_original.fill((80, 0, 80))
            pygame.draw.rect(self.image_original, (150, 0, 150), (20, 20, 180, 120))

        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(center=(x, y))
        
        self.max_vida = 500
        self.vida = self.max_vida
        self.rage_mode = False
        
        self.estado = "ENTRANDO"
        self.y_base = 120
        self.movendo_direita = True
        self.hover_timer = 0
        
        self.dash_cooldown = 0
        self.dash_delay = 300
        self.velocidade_mergulho = 12
        
        self.tiro_timer = 60 

    def verificar_rage_mode(self):
        if self.vida <= (self.max_vida * 0.5) and not self.rage_mode:
            self.rage_mode = True
            tint = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            tint.fill((100, 0, 0, 100))
            self.image_original.blit(tint, (0,0), special_flags=pygame.BLEND_ADD)
            self.image = self.image_original.copy()

    def atualizar_posicao(self):
        self.verificar_rage_mode()
        self.hover_timer += 0.1

        if self.estado == "ENTRANDO":
            self.rect.y += 3
            if self.rect.centery >= self.y_base:
                self.rect.centery = self.y_base
                self.estado = "PATRULHANDO"

        elif self.estado == "PATRULHANDO":
            vel_atual = 5 if self.rage_mode else 2
            
            if self.movendo_direita:
                self.rect.x += vel_atual
                if self.rect.right >= LARGURA - 10:
                    self.movendo_direita = False
            else:
                self.rect.x -= vel_atual
                if self.rect.left <= 10:
                    self.movendo_direita = True
            
            flutuacao = math.sin(self.hover_timer) * 10
            self.rect.centery = self.y_base + flutuacao

            if self.rage_mode:
                self.dash_cooldown += 1
                if self.dash_cooldown > self.dash_delay:
                    self.estado = "MERGULHANDO"
                    self.dash_cooldown = 0
                    if self.jogador_alvo:
                        if self.jogador_alvo.rect.centerx > self.rect.centerx:
                             self.movendo_direita = True
                        else:
                             self.movendo_direita = False

        elif self.estado == "MERGULHANDO":
            self.rect.y += self.velocidade_mergulho
            self.rect.x += random.choice([-2, 2]) 
            
            if self.rect.bottom >= ALTURA - 50:
                self.estado = "RETORNANDO"

        elif self.estado == "RETORNANDO":
            self.rect.y -= (self.velocidade_mergulho - 4)
            if self.rect.centery <= self.y_base:
                self.rect.centery = self.y_base
                self.estado = "PATRULHANDO"
                self.dash_delay = random.randint(180, 400)

    def tentar_atirar(self):
        if self.grupo_tiros is None or self.estado == "ENTRANDO":
            return

        self.tiro_timer -= 1
        
        cooldown_tiro = 35 if self.rage_mode else 55
        
        if self.tiro_timer <= 0:
            cx, cy = self.rect.centerx, self.rect.bottom - 20
            vel_tiro = 7 if not self.rage_mode else 9
            
            tiro_mid = TiroBoss(cx, cy, vy=vel_tiro, vx=0)
            
            tiro_left = TiroBoss(cx - 20, cy - 10, vy=vel_tiro * 0.9, vx=-3)
            tiro_right = TiroBoss(cx + 20, cy - 10, vy=vel_tiro * 0.9, vx=3)
            
            self.grupo_tiros.add(tiro_mid, tiro_left, tiro_right)
            
            if self.rage_mode:
                tiro_ext_left = TiroBoss(cx - 40, cy - 20, vy=vel_tiro * 0.8, vx=-5)
                tiro_ext_right = TiroBoss(cx + 40, cy - 20, vy=vel_tiro * 0.8, vx=5)
                self.grupo_tiros.add(tiro_ext_left, tiro_ext_right)

            self.tiro_timer = cooldown_tiro

    def receber_dano(self):
        self.vida -= 10
        dropar = (self.vida % 80 == 0)
        return self.vida <= 0, dropar

    def update(self):
        self.atualizar_posicao()
        self.tentar_atirar()