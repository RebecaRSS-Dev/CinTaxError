class Transicoes:
    def irParaHub(self, ObjNivel, ObjetosNiveis, nivelAtual, teleporte_cooldown):
        if ObjNivel.player.mudarFase:
            nivelAtual = 'Hub'
            ObjNivel.player.mudarFase = False
            ObjNivel = ObjetosNiveis[nivelAtual]
            ObjNivel.player.rect.center = ObjNivel.player_pos
            teleporte_cooldown = 100
            return ObjNivel, nivelAtual, ObjNivel.player.vidas, ObjNivel.player.pontuacao, ObjNivel.player.efeito, ObjNivel.player.fragmentos, teleporte_cooldown

        return ObjNivel, nivelAtual, None, None, None, None, teleporte_cooldown
