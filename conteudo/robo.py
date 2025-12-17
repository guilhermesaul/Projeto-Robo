import pygame
import math
import os
import random
from entidade import Entidade
from config import LARGURA, ALTURA


class TiroInimigo(Entidade):
    """
    Classe base para tiros de inimigos
    Demonstra: Herança, Encapsulamento, Polimorfismo
    """
    def __init__(self, x, y, velocidade, vx=0):
        super().__init__(x, y, velocidade)
        self._vx = vx  # Encapsulamento
        self._carregar_imagem()
    
    def _carregar_imagem(self):
        """Método privado para carregar imagem (pode ser sobrescrito)"""
        CAMINHO_IMAGEM = os.path.join(
            os.path.dirname(__file__), 
            "assets", 
            "images", 
            "shot_exp1.png"
        )
        imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
        self.image = pygame.transform.rotate(imagem_original, -90)
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def update(self):
        """Atualiza o tiro (Polimorfismo)"""
        self.rect.y += self._velocidade
        if self.rect.y > ALTURA:
            self.kill()


class TiroRobo(TiroInimigo):
    """
    Tiro padrão dos robôs
    Demonstra: Herança de TiroInimigo
    """
    def __init__(self, x, y, velocidade=6):
        super().__init__(x, y, velocidade)


class TiroBoss(TiroInimigo):
    """
    Tiro do Boss (maior e com movimento diagonal)
    Demonstra: Herança, Polimorfismo
    """
    def __init__(self, x, y, vy, vx=0):
        super().__init__(x, y, vy, vx)
    
    def _carregar_imagem(self):
        """Sobrescreve para criar tiro maior (Polimorfismo)"""
        CAMINHO_IMAGEM = os.path.join(
            os.path.dirname(__file__), 
            "assets", 
            "images", 
            "shot_exp1.png"
        )
        imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
        self.image = pygame.transform.rotate(imagem_original, -90)
        self.image = pygame.transform.scale(self.image, (74, 74))
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def update(self):
        """Atualiza com movimento diagonal (Polimorfismo)"""
        self.rect.y += self._velocidade
        self.rect.x += self._vx
        
        if (self.rect.top > ALTURA or 
            self.rect.right < -50 or 
            self.rect.left > LARGURA + 50):
            self.kill()


# ROBO BASE
class Robo(Entidade):
    """
    Classe base para todos os robôs
    Demonstra: Herança (de Entidade), Encapsulamento, Polimorfismo
    Classe abstrata que define comportamento base dos robôs
    """
    def __init__(self, x, y, velocidade, grupo_tiros=None):
        super().__init__(x, y, velocidade)
        self.image.fill((255, 255, 255))
        
        # Atributos privados (encapsulamento)
        self._grupo_tiros = grupo_tiros
        self._tiro_timer = random.randint(40, 160)
        self._vel_tiro = 6
    
    # Propriedades para encapsulamento
    @property
    def grupo_tiros(self):
        return self._grupo_tiros
    
    @property
    def vel_tiro(self):
        return self._vel_tiro

    def atualizar_posicao(self):
        """Método abstrato para atualizar posição (Polimorfismo)"""
        raise NotImplementedError("Subclasses devem implementar atualizar_posicao()")

    def tentar_atirar(self):
        """Sistema de tiro dos robôs (Polimorfismo - pode ser sobrescrito)"""
        if self._grupo_tiros is None:
            return
        
        self._tiro_timer -= 1
        if self._tiro_timer <= 0:
            x, y = self.ponto_de_tiro()
            tiro = TiroRobo(x, y, velocidade=self._vel_tiro)
            self._grupo_tiros.add(tiro)
            self._tiro_timer = random.randint(50, 180)

    def ponto_de_tiro(self):
        """Define de onde o tiro sai (Polimorfismo - pode ser sobrescrito)"""
        return (self.rect.centerx, self.rect.bottom - 10)
    
    def update(self):
        """Atualiza o robô (Polimorfismo)"""
        self.atualizar_posicao()
        self.tentar_atirar()
        
        # Remove se sair da tela
        if self.rect.y > ALTURA:
            self.kill()


# ROBO LENTO
class RoboLento(Robo):
    """
    Robô Lento - desce verticalmente
    Demonstra: Herança, Polimorfismo
    """
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade=1.5, grupo_tiros=grupo_tiros)
        self._carregar_sprite()
    
    def _carregar_sprite(self):
        """Método privado para carregar sprite (encapsulamento)"""
        CAMINHO_IMAGEM = os.path.join(
            os.path.dirname(__file__),
            "assets", 
            "images", 
            "roboLento.png"
        )
        try:
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (56, 100))
        except:
            pass
        self.rect = self.image.get_rect(center=self.rect.center)

    def atualizar_posicao(self):
        """Implementação do movimento (Polimorfismo)"""
        self.rect.y += self._velocidade


# ROBO RAPIDO
class RoboRapido(Robo):
    """
    Robô Rápido - desce verticalmente mais rápido
    Demonstra: Herança, Polimorfismo
    """
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade=3, grupo_tiros=grupo_tiros)
        self._carregar_sprite()
    
    def _carregar_sprite(self):
        """Método privado para carregar sprite (encapsulamento)"""
        CAMINHO_IMAGEM = os.path.join(
            os.path.dirname(__file__),
            "assets", 
            "images", 
            "roboRapido.png"
        )
        try:
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (64, 115))
        except:
            pass
        self.rect = self.image.get_rect(center=self.rect.center)

    def atualizar_posicao(self):
        """Implementação do movimento (Polimorfismo)"""
        self.rect.y += self._velocidade


# ROBO ZIGUEZAGUE
class RoboZigueZague(Robo):
    """
    Robô ZigueZague - se move horizontalmente e verticalmente
    Demonstra: Herança, Polimorfismo, Encapsulamento
    """
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade=2, grupo_tiros=grupo_tiros)
        self._direcao = 1  # Encapsulamento
        self._carregar_sprite()
    
    def _carregar_sprite(self):
        """Método privado para carregar sprite (encapsulamento)"""
        CAMINHO_IMAGEM = os.path.join(
            os.path.dirname(__file__),
            "assets", 
            "images", 
            "roboZigue.png"
        )
        try:
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (64, 100))
        except:
            pass
        self.rect = self.image.get_rect(center=self.rect.center)

    def atualizar_posicao(self):
        """Implementação do movimento ziguezague (Polimorfismo)"""
        self.rect.y += self._velocidade
        self.rect.x += self._direcao * 3

        # Inverte direção nas bordas
        if self.rect.left <= 0 or self.rect.right >= LARGURA:
            self._direcao *= -1


# ROBO CICLICO
class RoboCiclico(Robo):
    """
    Robô Cíclico - se move em círculos
    Demonstra: Herança, Polimorfismo, Encapsulamento
    """
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade=0, grupo_tiros=grupo_tiros)
        self._carregar_sprite()
        
        # Atributos privados para movimento circular (encapsulamento)
        self._centro_x = x
        self._centro_y = y
        self._raio = 60
        self._angulo = 0
        self._vel_angular = 0.05
        self._vel_descida = 1
    
    def _carregar_sprite(self):
        """Método privado para carregar sprite (encapsulamento)"""
        CAMINHO_IMAGEM = os.path.join(
            os.path.dirname(__file__),
            "assets", 
            "images", 
            "roboCiclico.png"
        )
        try:
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self.image = pygame.transform.rotate(imagem_original, -90)
            self.image = pygame.transform.scale(self.image, (45, 90))
        except:
            self.image = pygame.Surface((45, 90))
            self.image.fill((200, 50, 200))
        self.rect = self.image.get_rect(center=self.rect.center)

    def atualizar_posicao(self):
        """Implementação do movimento circular (Polimorfismo)"""
        self._angulo += self._vel_angular
        self._centro_y += self._vel_descida

        self.rect.x = self._centro_x + math.cos(self._angulo) * self._raio
        self.rect.y = self._centro_y + math.sin(self._angulo) * self._raio

    def update(self):
        """Sobrescreve update para remover quando sair da tela (Polimorfismo)"""
        self.atualizar_posicao()
        self.tentar_atirar()

        if self.rect.top > ALTURA + 60:
            self.kill()


# ROBO SALTADOR
class RoboSaltador(Robo):
    """
    Robô Saltador - teleporta aleatoriamente
    Demonstra: Herança, Polimorfismo, Encapsulamento
    """
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade=2, grupo_tiros=grupo_tiros)
        self._carregar_sprite()
        
        # Atributos privados para teleporte (encapsulamento)
        self._velocidade_vertical = self._velocidade
        self._gravidade = 0.3
        self._posicao_y = float(y)
        self._tempo_teleporte = 0
        self._intervalo_teleporte_minimo = 50
        self._intervalo_teleporte_maximo = 140
        self._proximo_teleporte = random.randint(
            self._intervalo_teleporte_minimo, 
            self._intervalo_teleporte_maximo
        )
        self._flash_duracao = 10
        self._flash_timer = 0
    
    def _carregar_sprite(self):
        """Método privado para carregar sprite (encapsulamento)"""
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
        self.rect = self.image.get_rect(center=self.rect.center)

    def atualizar_posicao(self):
        """Implementação do movimento com teleporte (Polimorfismo)"""
        # Contador para teleporte
        self._tempo_teleporte += 1
        if self._tempo_teleporte >= self._proximo_teleporte:
            novo_x = random.randint(40, LARGURA - 40)
            novo_y = random.randint(0, ALTURA // 2)
            self.rect.x = novo_x
            self._posicao_y = float(novo_y)
            self.rect.y = novo_y
            self._tempo_teleporte = 0
            self._proximo_teleporte = random.randint(
                self._intervalo_teleporte_minimo, 
                self._intervalo_teleporte_maximo
            )
            self._flash_timer = self._flash_duracao

        # Atualização da posição vertical (descida leve)
        self._velocidade_vertical += self._gravidade
        if self._velocidade_vertical > 4:
            self._velocidade_vertical = 4
        self._posicao_y += self._velocidade_vertical
        self.rect.y = int(self._posicao_y)

    def update(self):
        """Sobrescreve update (Polimorfismo)"""
        self.atualizar_posicao()
        self.tentar_atirar()
        # Mata apenas se sair muito acima da tela
        if self.rect.y < -60:
            self.kill()


# ROBO CAÇADOR
class RoboCacador(Robo):
    """
    Robô Caçador - persegue o jogador
    Demonstra: Herança, Polimorfismo, Encapsulamento
    """
    def __init__(self, x, y, jogador, grupo_tiros=None):
        super().__init__(x, y, velocidade=2, grupo_tiros=grupo_tiros)
        self._jogador = jogador  # Encapsulamento
        self._carregar_sprite()
    
    def _carregar_sprite(self):
        """Método privado para carregar sprite (encapsulamento)"""
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
        self.rect = self.image.get_rect(center=self.rect.center)

    def atualizar_posicao(self):
        """Implementação do movimento de perseguição (Polimorfismo)"""
        diferenca_x = self._jogador.rect.centerx - self.rect.centerx
        diferenca_y = self._jogador.rect.centery - self.rect.centery
        distancia = math.hypot(diferenca_x, diferenca_y)
        
        if distancia > 0:
            normal_x = diferenca_x / distancia
            normal_y = diferenca_y / distancia
            self.rect.x += normal_x * self._velocidade * 2
            self.rect.y += normal_y * self._velocidade
        else:
            self.rect.y += self._velocidade


# EXPLOSAO
class Explosao(pygame.sprite.Sprite):
    """
    Efeito de explosão animado
    Demonstra: Sprites, Animação
    """
    def __init__(self, x, y):
        super().__init__()
        
        self._frames = []  # Encapsulamento
        self._carregar_frames()
        
        self._frame_atual = 0
        self.image = self._frames[self._frame_atual]
        self.rect = self.image.get_rect(center=(x, y))
        
        self._tempo_animacao = 60  # ms
        self._ultimo_update = pygame.time.get_ticks()
    
    def _carregar_frames(self):
        """Método privado para carregar frames da animação (encapsulamento)"""
        base_path = os.path.join(
            os.path.dirname(__file__),
            "assets", "images"
        )
        
        for i in range(1, 7):
            imagem = pygame.image.load(
                os.path.join(base_path, f"explosao_{i}.png")
            ).convert_alpha()
            imagem = pygame.transform.smoothscale(imagem, (80, 80))
            self._frames.append(imagem)

    def update(self):
        """Atualiza a animação"""
        agora = pygame.time.get_ticks()
        
        if agora - self._ultimo_update >= self._tempo_animacao:
            self._ultimo_update = agora
            self._frame_atual += 1
            
            if self._frame_atual >= len(self._frames):
                self.kill()
            else:
                self.image = self._frames[self._frame_atual]


# BOSS
class Boss(Robo):
    """
    Chefe final do jogo
    Demonstra: Herança, Polimorfismo, Encapsulamento
    """
    def __init__(self, x, y, grupo_tiros=None):
        super().__init__(x, y, velocidade=1, grupo_tiros=grupo_tiros)
        
        # Atributos privados (encapsulamento)
        self._piscando = 0
        self._vida_max = 250
        self._vida = self._vida_max
        self._direcao = 1
        self._vel_horizontal = 4
        self._tiro_timer = 60
        self._vel_tiro = 10
        self._pos_y_alvo = ALTURA // 4
        self._descendo = True
        
        self._carregar_sprite()
    
    def _carregar_sprite(self):
        """Método privado para carregar sprite (encapsulamento)"""
        try:
            CAMINHO_IMAGEM = os.path.join(
                os.path.dirname(__file__),
                "assets",
                "images",
                "boss.png"
            )
            imagem_original = pygame.image.load(CAMINHO_IMAGEM).convert_alpha()
            self._image_original = pygame.transform.rotate(imagem_original, 180)
            self._image_original = pygame.transform.scale(self._image_original, (250, 250))
        except:
            self._image_original = pygame.Surface((250, 250))
            self._image_original.fill((80, 0, 80))
        
        self.image = self._image_original.copy()
        self.rect = self.image.get_rect(center=self.rect.center)
    
    # Propriedades para encapsulamento
    @property
    def vida(self):
        return self._vida
    
    @vida.setter
    def vida(self, valor):
        self._vida = max(0, valor)
    
    @property
    def vida_max(self):
        return self._vida_max
    
    @property
    def max_vida(self):
        """Alias para compatibilidade"""
        return self._vida_max

    def atualizar_posicao(self):
        """Implementação do movimento do Boss (Polimorfismo)"""
        # Desce até posição alvo, depois fica se movendo lateralmente
        if self._descendo:
            if self.rect.centery < self._pos_y_alvo:
                self.rect.y += self._velocidade * 2
            else:
                self._descendo = False
        else:
            # Movimento lateral
            self.rect.x += self._direcao * self._vel_horizontal
            
            # Mantém o Boss sempre dentro da tela
            if self.rect.left <= 0:
                self.rect.left = 0
                self._direcao *= -1
            elif self.rect.right >= LARGURA:
                self.rect.right = LARGURA
                self._direcao *= -1
   
    def tentar_atirar(self):
        """Boss atira 5 tiros espalhados (Polimorfismo)"""
        if self._grupo_tiros is None:
            return
       
        self._tiro_timer -= 1
        if self._tiro_timer <= 0:
            # 5 tiros espalhados
            for offset in [-60, -30, 0, 30, 60]:
                tiro = TiroBoss(
                    self.rect.centerx + offset, 
                    self.rect.bottom, 
                    self._vel_tiro
                )
                self._grupo_tiros.add(tiro)
           
            self._tiro_timer = random.randint(60, 120)

    def update(self):
        """Atualiza o Boss (Polimorfismo)"""
        self.atualizar_posicao()
        self.tentar_atirar()

        if self._piscando > 0:
            self._piscando -= 1
            self.image = self._image_original.copy()
            self.image.set_alpha(160)  # Mais transparente (efeito dano)
        else:
            self.image = self._image_original.copy()
            self.image.set_alpha(255)  # Normal

    def receber_dano(self, quantidade=1):
        """Recebe dano (Polimorfismo - sobrescreve método da classe pai)"""
        self._vida -= quantidade
        self._piscando = 8  # Quantidade de frames do efeito

        deve_dropar_powerup = random.random() < 0.05

        if self._vida <= 0:
            self.kill()
            return True, deve_dropar_powerup

        return False, deve_dropar_powerup

