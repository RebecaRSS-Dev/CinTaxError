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