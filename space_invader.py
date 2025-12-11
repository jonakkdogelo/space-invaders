import pygame
from pygame.locals import *
import numpy as np
from sys import exit
import os
import random

pygame.init()

largura_janela, altura_janela = 600, 600
tamanho = 10
linha,coluna = 5,10
dano = 10
defesas = 4
nivel = 1
score = 0
arma = 1

FPS = 10
tela = pygame.display.set_mode((largura_janela, altura_janela))
clock = pygame.time.Clock()
musica = pygame.mixer.music.load('Music-Martian_Madness.mp3')
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1)
mortealien = pygame.mixer.Sound('animated-cartoon-explosion-impact-352744.mp3')
mortealien.set_volume(0.5)

spritedict = {'a':(0,0),'b':(1,0),'c':(2,0),'d':(3,0),'e':(4,0),'f':(5,0),'g':(6,0),'h':(7,0),'i':(8,0),'j':(0,1),'k':(1,1),
              'l':(2,1),'m':(3,1),'n':(4,1),'o':(5,1),'p':(6,1),'q':(7,1),'r':(8,1),'s':(0,2),'t':(1,2),'u':(2,2),'v':(3,2),'w':(4,2),
              'x':(5,2),'y':(6,2),'z':(7,2),')':(6,8.4),'(':(5,8.4)}  #spritesheet index

def comecar():
    global vidas,tiros,alienlista,defensores,tiros_player,carregamento,alienvx,alienvy,clocking,delay,danoclock,nuvem_inferno,player,allsprites,arma,infodict
    infodict = {'b': ((0,0,200),30),'c':((200,0,0),50),'d':((200,0,200),30),'e':((200,0,200),10),'f':((0,200,200),60),'g':((250,0,0),50), ')':((0,255,0),100*nivel),'(':((0,255,0),50*nivel)}  #cor e vida
    vidas = 5
    tiros = []
    tiros_player = []
    alienlista = []
    defensores = []
    carregamento = True
    alienvx,alienvy = 10,2
    clocking,delay,danoclock,nuvem_inferno = 0,0,0,50
    allsprites = pygame.sprite.Group()
    intro = alien(largura_janela//2,altura_janela//2,spritedict['a'],(0,255,0),50,10)
    allsprites.add(intro)
    player = alien(largura_janela//2,largura_janela-10,spritedict['w'],(0,255,0),4,vidas*10)

with open("niveis.txt", "r", encoding="utf-8") as ficheiro:
    linha = ficheiro.read()
niveis = linha.strip().split('\n')
pasta_principal = os.path.dirname(__file__)
pixelsheet = pygame.image.load(os.path.join(pasta_principal, 'kindpng_1784687.png')).convert_alpha()
class alien(pygame.sprite.Sprite):
    def __init__(self,x,y,tipo,cor,size,life=1):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.size = size
        self.lifeinit = life
        self.life = life
        self.atirar = False
        pygame.sprite.Sprite.__init__(self)
        self.image = pixelsheet.subsurface((2+110*tipo[0],25+120*tipo[1]), (109,95))   # 1º bloco 1,1 112,122,
        self.image = pygame.transform.scale(self.image, (tamanho*size,tamanho*size))
        self.image.fill((255, 255, 255, 255), None, pygame.BLEND_RGB_ADD)  # torna tudo branco
        self.image.fill(cor, None, pygame.BLEND_MULT) 
        self.rect = self.image.get_rect()
        self.rect.center = (x +(tamanho/2),y +(tamanho/2))

    def atualizar(self,vx,vy,p_atirar):
        self.x += vx
        self.y += vy
        self.rect.center = (self.x +(tamanho/2),self.y +(tamanho/2))
        prob = random.randint(1,p_atirar) if p_atirar != 0 else 0
        self.atirar = True if prob == 1 else False
        
comecar()
def atualizar():
    global allsprites,alienlista,clocking,tiros,tiros_player,alienvx,alienvy,delay,danoclock,nuvem_inferno,nivel,score
    if carregamento == False and len(allsprites) == 0:
        allsprites.add(player)
        for i in range(defesas):
            criar_alien(100+i*(largura_janela-100)//defesas,largura_janela-70,')',8)
        k,i = 0,0
        for j in range(len(niveis[nivel-1])):
            if niveis[nivel-1][j] != ' ' and niveis[nivel-1][j] != '/':
                criar_alien(100 +40*(j-k),100 +25*i,niveis[nivel-1][j],2.5)
            if niveis[nivel-1][j] == '/':
                i += 1
                k += 11

    if clocking == 10:
        clocking = 0
        nuvem_inferno -= 1
        for i in range(len(alienlista)):
            if (alienlista[i].x > largura_janela-50 or alienlista[i].x < 50) and alienlista[i].tipo != (4,0):
                alienvx = -alienvx
                break
            if alienlista[i].y > altura_janela-150:
                alienvy = 0
        for i in range(len(alienlista)):
            if alienlista[i].tipo != (4,0):
                alienlista[i].atualizar(alienvx,alienvy,30 if alienlista[i].tipo != (6,0) else max(nuvem_inferno,2))
                if alienlista[i].atirar:
                    alienlista[i].atirar = False
                    vezes = 1 if alienlista[i].lifeinit == 30 else (3 if alienlista[i].lifeinit == 50 else 0)
                    for j in range(vezes):
                        criar_tiro(alienlista[i].x+j*vezes*5,alienlista[i].y,1)
                        alienlista[i].life -= 6 if alienlista[i].tipo == (3,0) else 0
        for i in range(len(tiros)):
            if i < len(tiros):
                if tiros[i].tipo == spritedict['z']:
                    deletar(tiros[i],i,tiros)           
    elif carregamento == False:
            clocking += 1
    for i in range(len(alienlista)):
        if alienlista[i].tipo == (4,0):
            alienlista[i].atualizar((abs(alienvx)/alienvx)*2,alienvy if alienlista[i].y < altura_janela-200 else 0,2)
            if alienlista[i].x > largura_janela+20:
                alienlista[i].x = -10
            if alienlista[i].x < -20:
                alienlista[i].x = largura_janela+10
            if clocking == 9 and alienlista[i].atirar:
                criar_tiro(alienlista[i].x,alienlista[i].y,1)
    
    for i in range(len(tiros)):
        if tiros[i].tipo != spritedict['z']:
            tiros[i].atualizar(0,4,0)
    for i in range(len(tiros_player)):
        tiros_player[i].atualizar(0,-8,0)
   
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT] and player.x < largura_janela:
        player.x += 10
    elif keys[K_LEFT] and player.x > 0:
        player.x -= 10
    if keys[K_SPACE] and delay == 0:
        atirou = 1
        delay += 5 if arma == 1 else(1 if arma == 2  else 10)
    else:
        atirou = 0
        delay -= 1 if delay != 0 else 0
    player.atualizar(0,0,atirou)
    if player.atirar:
        player.atirar = False
        criar_tiro(player.x,player.y -10,2)

    colisão_player = pygame.sprite.spritecollide(player, tiros, False, pygame.sprite.collide_mask)
    for i in range(len(alienlista)):
        if pygame.sprite.spritecollide(alienlista[i],tiros_player, False, pygame.sprite.collide_mask):
            alienlista[i].life -= dano if arma==1 else(dano/5 if arma == 2 else dano*2)
        if pygame.sprite.spritecollide(alienlista[i],tiros, False, pygame.sprite.collide_mask) and alienlista[i].tipo == (5,0):
            for j in range(len(tiros)):
                if pygame.sprite.spritecollide(tiros[j],alienlista, False, pygame.sprite.collide_mask) and tiros[j].x > alienlista[i].x-50 and tiros[j].x < alienlista[i].x+50:
                    tiros[j].y += 50
                    for k in range(1,random.randint(1,3)):
                        criar_tiro(alienlista[i].x +k*20,alienlista[i].y +50,1)

    for i in range(len(defensores)):
        if pygame.sprite.spritecollide(defensores[i],tiros, False, pygame.sprite.collide_mask) or pygame.sprite.spritecollide(defensores[i],tiros_player, False, pygame.sprite.collide_mask):
            defensores[i].life -= dano
    for i in range(len(tiros_player)):
        if i< len(tiros_player):
            if pygame.sprite.spritecollide(tiros_player[i],alienlista, False, pygame.sprite.collide_mask) or pygame.sprite.spritecollide(tiros_player[i],defensores, False, pygame.sprite.collide_mask) or tiros_player[i].y < 0:
                deletar(tiros_player[i],i,tiros_player)
    for i in range(len(tiros)):
        if i< len(tiros):
            noplayer = tiros[i].x > player.x -50 and tiros[i].x < player.x +50 and tiros[i].y > altura_janela-60
            if pygame.sprite.spritecollide(tiros[i],defensores, False, pygame.sprite.collide_mask) or (noplayer and colisão_player) or tiros[i].y > largura_janela: 
                deletar(tiros[i],i,tiros)

    for i in range(len(alienlista)):
        if i<len(alienlista):
           if alienlista[i].life <= 0:
                criar_tiro(alienlista[i].x,alienlista[i].y,0)
                score += alienlista[i].lifeinit
                mortealien.play()
                if alienlista[i].tipo == (3,0):
                    for j in range(random.randint(1,3)):
                        criar_alien(alienlista[i].x -j*30,alienlista[i].y,'e',2)
                deletar(alienlista[i],i,alienlista)
    for i in range(len(defensores)):
        if i< len(defensores):
            if defensores[i].life <= 50*nivel and defensores[i].tipo == spritedict[')']:
                criar_alien(defensores[i].x,defensores[i].y,'(',6)
                deletar(defensores[i],i,defensores)
            if defensores[i].life <= 0:
                deletar(defensores[i],i,defensores)
    
    if colisão_player and danoclock <= 0:
        danoclock = 20
        player.life -= dano
    else:
        danoclock -= 1 
    if danoclock > 0 and danoclock % 2 == 0:
        allsprites.remove(player)
    elif danoclock > 0:
        allsprites.add(player)

    if player.life <= 0:
        dead = True
        clock = pygame.time.Clock()
        pos1, pos2 = [-200,altura_janela//2 -30], [largura_janela+200,altura_janela//2 +30]
        while dead:
            desenhar(tela)
            clock.tick(60)
            pos1[0] += 4
            pos2[0] -= 4
            if pos1[0] > largura_janela+200:
                pos1 = [-200,altura_janela//2 -30]
            if pos2[0] < -200:
                pos2 = [largura_janela+200,altura_janela//2 +30]
            mensager('GAME',pos1,40)
            mensager('OVER',pos2,40)
            mensager('press r to retart',(largura_janela//2,altura_janela//2+100),21)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_r:
                        comecar()
                        dead = False
                        score = 0
                        break
            pygame.display.flip()
    elif (len(alienlista) == 0 and clocking == 10 and len(tiros) == 0) or (keys[K_j] and clocking == 10):
        nivel += 1
        comecar()
        for i in range(len(defensores)):
            score += 75 if defensores[i].life < 50*nivel else 225

def criar_alien(x,y,tipo,size):
    newalien = alien(x,y,spritedict[tipo],infodict[tipo][0],size,infodict[tipo][1])
    allsprites.add(newalien) 
    alienlista.append(newalien) if tipo != ')' and tipo != '(' else defensores.append(newalien)

def criar_tiro(x,y,tipo):
    tiro = alien(x,y,spritedict['y'],(0,255,255),2) if tipo == 1 else alien(x,y,spritedict['y'] if tipo != 0 else spritedict['z'],(255,255,0),(1 if arma==1 else(2 if arma==3 else 0.5))*(2.5 if tipo == 0 else 1))
    allsprites.add(tiro)
    tiros.append(tiro) if tipo == 1 or tipo == 0 else tiros_player.append(tiro)

def deletar(alien,i,conjunto):
    allsprites.remove(alien)
    del conjunto[i]

def mensager(string,pos,size):
    fonte = pygame.font.SysFont('Arial', int(size), True, True)
    texto_formatado = fonte.render(string, True, (0,200,0))
    ret_texto = texto_formatado.get_rect()
    ret_texto.center = pos
    tela.blit(texto_formatado, ret_texto) 

def desenhar(tela):
    tela.fill((0,0,0))
    allsprites.draw(tela)
    allsprites.update()
    if carregamento == False:
        mensager(f'life: {player.life/10}',(50,10),21)
        mensager(f'score: {score}',(largura_janela-120,10),21)
    else:
        mensager(f'level: {nivel}',(largura_janela//2,altura_janela-200),21)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if carregamento == True:
                    carregamento = False
                    allsprites = pygame.sprite.Group()
            if event.key == K_1 or event.key == K_2 or event.key == K_3:
                for i in range(len(tiros_player)):
                    allsprites.remove(tiros_player[i])
                tiros_player = []
                arma = 1 if event.key == K_1 else(2 if event.key == K_2 else 3)
    atualizar()
    desenhar(tela)
    clock.tick(FPS)
    pygame.display.flip()