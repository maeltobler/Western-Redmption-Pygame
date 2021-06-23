import pygame
import sys

pygame.init()
hintergrund = pygame.image.load("01.png")
screen = pygame.display.set_mode([714,339])
Clock = pygame.time.Clock()

stehen = pygame.image.load("stand.png")
sprung = pygame.image.load("sprung.png")
rechtsGehen = [pygame.image.load("rechts1.png"),pygame.image.load("rechts2.png"),pygame.image.load("rechts3.png"),pygame.image.load("rechts4.png"),pygame.image.load("rechts5.png"),pygame.image.load("rechts6.png"),pygame.image.load("rechts7.png"),pygame.image.load("rechts8.png")]
linksGehen = [pygame.image.load("links1.png"),pygame.image.load("links2.png"),pygame.image.load("links3.png"),pygame.image.load("links4.png"),pygame.image.load("links5.png"),pygame.image.load("links6.png"),pygame.image.load("links7.png"),pygame.image.load("links8.png")]
x = 300
y = 260
geschw = 5
breite = 40
hoehe = 80

def zeichnen(Liste):
    global schritteRechts, schritteLinks

    screen.blit(hintergrund,(0,0))
    if schritteRechts == 63:
        schritteRechts = 0
    if schritteLinks == 63:
        schritteLinks = 0

    if Liste[0]:
        screen.blit(linksGehen[schritteLinks//8], (x,y))
    if Liste[1]:
        screen.blit(rechtsGehen[schritteRechts//8], (x,y))
    if Liste[2]:
        screen.blit(stehen,(x,y))
    if Liste[3]:
        screen.blit(sprung,(x,y))

    pygame.display.update()

linkeWand = pygame.draw.rect(screen, (0,0,0), (-2,0,2,340), 0)
rechteWand = pygame.draw.rect(screen, (0,0,0), (715,0,2,340), 0)
go = True
sprungvar = -16
#[links,rechts,stand,sprung]
richtg = [0,0,0,0]
schritteRechts = 0
schritteLinks = 0
while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    spielerRechteck = pygame.Rect(x,y,40,80) 
    gedrueckt = pygame.key.get_pressed()
    richtg = [0,0,1,0]
    if gedrueckt[pygame.K_w] and sprungvar == -16:
        sprungvar = 15 
    if gedrueckt[pygame.K_d] and not spielerRechteck.colliderect(rechteWand):
        x += geschw
        richtg = [0,1,0,0]
        schritteRechts += 1
    if gedrueckt[pygame.K_a] and not spielerRechteck.colliderect(linkeWand):
        x -= geschw
        richtg = [1,0,0,0]
        schritteLinks += 1


    if sprungvar >= -15:
        richtg = [0,0,0,1]
        n = 1
        if sprungvar < 0:
            n = -1
        y -= (sprungvar**2)*0.17*n
        sprungvar -=1
    
    if richtg[2] or richtg[3]:
        schritteRechts = 0
        schritteLinks = 0
    
    zeichnen(richtg)
    Clock.tick(60)