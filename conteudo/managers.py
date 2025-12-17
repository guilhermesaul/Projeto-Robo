"""
Gerenciadores e componentes de UI do jogo.
Inclui gerenciador de fases, menus, botões e controles deslizantes.
"""
import pygame
from config import LARGURA, ALTURA


class GerenciadorFases:
    """Gerencia dados de fases e progressão."""

    FASES = {
        1: {"nome": "Fase 1: Iniciante Orbital", "duracao": 550, "robos": ["lento", "rapido"]},
        2: {"nome": "Fase 2: Patrulha Mediana", "duracao": 650, "robos": ["lento", "saltador", "ziguezague"]},
        3: {"nome": "Fase 3: Investida Difícil", "duracao": 820, "robos": ["rapido", "cacador", "ciclico"]},
        4: {"nome": "Fase 4: Boss Insano", "duracao": 9_999_999, "robos": []},
        5: {
            "nome": "Fase Secreta: Caos Total",
            "duracao": 1650,
            "robos": ["lento", "rapido", "saltador", "ziguezague", "cacador", "ciclico"],
        },
    }

    def __init__(self):
        self._fase_atual = 1
        self._temporizador = 0
        self._boss_spawnou = False
        self._boss_ativo = False

    @property
    def fase_atual(self):
        return self._fase_atual

    @fase_atual.setter
    def fase_atual(self, valor):
        if valor in self.FASES:
            self._fase_atual = valor

    @property
    def temporizador(self):
        return self._temporizador

    @temporizador.setter
    def temporizador(self, valor):
        self._temporizador = max(0, valor)

    @property
    def boss_spawnou(self):
        return self._boss_spawnou

    @boss_spawnou.setter
    def boss_spawnou(self, valor):
        self._boss_spawnou = valor

    @property
    def boss_ativo(self):
        return self._boss_ativo

    @boss_ativo.setter
    def boss_ativo(self, valor):
        self._boss_ativo = valor

    def incrementar_temporizador(self):
        self._temporizador += 1

    def resetar(self):
        self._fase_atual = 1
        self._temporizador = 0
        self._boss_spawnou = False
        self._boss_ativo = False

    def obter_info_fase(self):
        return self.FASES.get(self._fase_atual, {})

    def verificar_progressao(self):
        info = self.obter_info_fase()
        return self._temporizador >= info.get("duracao", 0)

    def avancar_fase(self):
        if self._fase_atual < len(self.FASES):
            self._fase_atual += 1
            self._temporizador = 0
            return True
        return False


class Botao:
    """Botão de interface com aliases em português e inglês para compatibilidade."""

    def __init__(self, text, x, y, width, height, fonte):
        self._text = text
        self._rect = pygame.Rect(x, y, width, height)
        self._fonte = fonte
        self._hovered = False
        self._cor_bg = (40, 40, 70)
        self._cor_hover = (60, 60, 100)
        self._cor_texto = (255, 255, 255)
        self._cor_borda = (20, 20, 40)
        self._cor_borda_hover = (255, 140, 0)

    @property
    def text(self):
        return self._text

    @property
    def texto(self):
        return self._text

    @property
    def rect(self):
        return self._rect

    @property
    def hovered(self):
        return self._hovered

    def desenhar(self, surface):
        cor = self._cor_hover if self._hovered else self._cor_bg
        cor_borda = self._cor_borda_hover if self._hovered else self._cor_borda
        pygame.draw.rect(surface, cor, self._rect, border_radius=8)
        pygame.draw.rect(surface, cor_borda, self._rect, 3, border_radius=8)
        text_surf = self._fonte.render(self._text, True, self._cor_texto)
        text_rect = text_surf.get_rect(center=self._rect.center)
        surface.blit(text_surf, text_rect)

    def verificar_destaque(self, mouse_pos):
        self._hovered = self._rect.collidepoint(mouse_pos)
        return self._hovered

    def foi_clicado(self, mouse_pos):
        return self._rect.collidepoint(mouse_pos)

    # Aliases legados
    def draw(self, surface):
        self.desenhar(surface)

    def check_hover(self, mouse_pos):
        return self.verificar_destaque(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.foi_clicado(mouse_pos)


class ControleDeslizante:
    """Controle deslizante para volumes."""

    def __init__(self, x, y, largura, altura, rotulo, fonte):
        self._centro_x = x
        self._rect = pygame.Rect(x - largura // 2, y, largura, altura)
        self._rotulo = rotulo
        self._fonte = fonte
        self._valor = 1.0
        self._arrastando = False
        self._cor_fundo = (50, 50, 50)
        self._cor_preenchida = (255, 160, 50)
        self._cor_circulo = (255, 140, 0)
        self._cor_texto = (255, 255, 255)

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, valor):
        self._valor = max(0.0, min(1.0, valor))

    @property
    def arrastando(self):
        return self._arrastando

    def desenhar(self, superficie):
        superficie_rotulo = self._fonte.render(self._rotulo, True, self._cor_texto)
        rotulo_x = self._centro_x - superficie_rotulo.get_width() // 2
        superficie.blit(superficie_rotulo, (rotulo_x, self._rect.y - 50))
        pygame.draw.rect(superficie, self._cor_fundo, self._rect, border_radius=5)
        largura_preenchida = int(self._rect.width * self._valor)
        rect_preenchido = pygame.Rect(self._rect.x, self._rect.y, largura_preenchida, self._rect.height)
        pygame.draw.rect(superficie, self._cor_preenchida, rect_preenchido, border_radius=5)
        controle_x = self._rect.x + largura_preenchida
        pygame.draw.circle(superficie, self._cor_circulo, (controle_x, self._rect.centery), 8)
        texto_percentual = self._fonte.render(f"{int(self._valor * 100)}%", True, self._cor_texto)
        superficie.blit(texto_percentual, (self._rect.right + 20, self._rect.y - 5))

    def verificar_destaque(self, pos_mouse):
        rect_controle = pygame.Rect(self._rect.x - 8, self._rect.y - 8, self._rect.width + 16, self._rect.height + 16)
        return rect_controle.collidepoint(pos_mouse)

    def iniciar_arraste(self, pos_mouse):
        if self.verificar_destaque(pos_mouse):
            self._arrastando = True
            self.atualizar(pos_mouse)

    def parar_arraste(self):
        self._arrastando = False

    def atualizar(self, pos_mouse):
        if self._arrastando:
            x_relativo = pos_mouse[0] - self._rect.x
            self._valor = max(0, min(1, x_relativo / self._rect.width))


class GerenciadorMenu:
    """Constrói os botões e controles das telas de menu/pausa."""

    def __init__(self, fonte_botoes, fonte_controle):
        self._fonte_botoes = fonte_botoes
        self._fonte_controle = fonte_controle
        self._botoes_menu = self._criar_botoes_menu()
        self._controles = self._criar_controles()
        self._botao_voltar = Botao("VOLTAR", LARGURA // 2 - 75, 600, 150, 50, fonte_botoes)
        self._botoes_pausa = self._criar_botoes_pausa()
        self._botao_voltar_menu = Botao("VOLTAR AO MENU", LARGURA // 2 - 125, 420, 250, 50, fonte_botoes)
        self._botao_vitoria_rejogar = Botao("JOGAR NOVAMENTE", LARGURA // 2 - 280, ALTURA // 2 + 80, 290, 50, fonte_botoes)
        self._botao_vitoria_menu = Botao("MENU", LARGURA // 2 + 80, ALTURA // 2 + 80, 200, 50, fonte_botoes)

    def _criar_botoes_menu(self):
        return [
            Botao("INICIAR JOGO", LARGURA // 2 - 125, 420, 250, 50, self._fonte_botoes),
            Botao("OPÇÕES", LARGURA // 2 - 125, 480, 250, 50, self._fonte_botoes),
            Botao("SAIR", LARGURA // 2 - 125, 540, 250, 50, self._fonte_botoes),
        ]

    def _criar_controles(self):
        return [
            ControleDeslizante(LARGURA // 2, 420, 200, 20, "VOLUME MUSICA  ", self._fonte_controle),
            ControleDeslizante(LARGURA // 2, 550, 200, 20, "VOLUME EFEITOS", self._fonte_controle),
        ]

    def _criar_botoes_pausa(self):
        return [
            Botao("CONTINUAR", LARGURA // 2 - 125, 320, 250, 50, self._fonte_botoes),
            Botao("OPÇÕES", LARGURA // 2 - 125, 380, 250, 50, self._fonte_botoes),
            Botao("SAIR", LARGURA // 2 - 125, 440, 250, 50, self._fonte_botoes),
        ]

    @property
    def botoes_menu(self):
        return self._botoes_menu

    @property
    def controles(self):
        return self._controles

    @property
    def botao_voltar(self):
        return self._botao_voltar

    @property
    def botoes_pausa(self):
        return self._botoes_pausa

    @property
    def botao_voltar_menu(self):
        return self._botao_voltar_menu

    @property
    def botao_vitoria_rejogar(self):
        return self._botao_vitoria_rejogar

    @property
    def botao_vitoria_menu(self):
        return self._botao_vitoria_menu
