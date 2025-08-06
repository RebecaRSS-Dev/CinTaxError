import pygame

pygame.init()

#variaveis do tamanho da teça
tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
largura, altura = tela.get_size()
pygame.display.set_caption("Tela de Login")

#classe botão
class Botao:
    def __init__(self, x, y, imagem_normal, imagem_selecionada):
        self.imagem_normal = imagem_normal
        self.imagem_selecionada = imagem_selecionada
        self.imagem_atual = self.imagem_normal 
        self.rect = self.imagem_normal.get_rect(center=(x, y))
    

    def checar_hover(self, posicao_mouse):
        if self.rect.collidepoint(posicao_mouse):
            self.imagem_atual = self.imagem_selecionada
        else:
            self.imagem_atual = self.imagem_normal
    
    def desenhar(self, tela):
        tela.blit(self.imagem_atual, self.rect)


# --- Seção de carregamento e posicionamento ---
try:
    # Imagem de fundo
    imagem_tela_start = pygame.transform.scale(pygame.image.load('Tela inicial.jpg').convert(), (largura, altura))
    
    # Imagens do Botão Start
    botao_jogar_img = pygame.image.load('Frame 2.png').convert_alpha()              
    botao_jogar_selecionado_img = pygame.image.load('Frame 14 (2).png').convert_alpha()
    
    # Imagens do botão Quit
    botao_sair_img = pygame.image.load('Frame 2 (1).png').convert_alpha()
    botao_sair_selecionado_img = pygame.image.load('Frame 13.png').convert_alpha()

except pygame.error as e:
    print (f"Erro ao carregar imagens: {e}")


#criação dos botoes
pos_y_jogar = altura * 0.80 - ((botao_jogar_img.get_height() + 20 + botao_sair_img.get_height()) / 2) + (botao_jogar_img.get_height() / 2)
pos_y_sair = altura * 0.80 + (botao_jogar_img.get_height() + 20 + botao_sair_img.get_height() / 2) - (botao_sair_img.get_height() / 2)
pos_x_botoes = largura // 2 

botao_jogar = Botao(pos_x_botoes, int(pos_y_jogar), botao_jogar_img, botao_jogar_selecionado_img)
botao_sair = Botao(pos_x_botoes, int(pos_y_sair), botao_sair_img, botao_sair_selecionado_img)


lista_de_botoes = [botao_jogar, botao_sair]

# --- Loop principal do jogo ---
rodando = True
while (rodando):
    posicao_mouse = pygame.mouse.get_pos()

    # --- Seção de Eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        ### NOVO: Lógica de clique para o botão SAIR
        if event.type == pygame.MOUSEBUTTONDOWN:
            if botao_sair.rect.collidepoint(posicao_mouse):
                rodando = False # Fecha o jogo ao clicar em SAIR
            if botao_jogar.rect.collidepoint(posicao_mouse):
                print("Clicou em JOGAR! (Aqui você mudaria para a tela do jogo)")

    # --- Seção de Desenho ---
    tela.blit(imagem_tela_start, (0,0))

    # Desenha todos os botões da lista
    for botao in lista_de_botoes:
        botao.checar_hover(posicao_mouse)
        botao.desenhar(tela)

    pygame.display.flip()

pygame.quit()