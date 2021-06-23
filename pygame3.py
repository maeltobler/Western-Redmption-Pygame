import pygame
import sys

pygame.init()
hintergrund = pygame.image.load("")
screen = pygame.display.set_mode([714,339])
Clock = pygame.time.Clock()
pygame.display.set_caption("pygamenew")

x = 300
y = 300
geschw = 3
breite = 40
hoehe = 80

go = True
while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    gedrueckt = pygame.key.get_pressed()
    if gedrueckt[pygame.K_UP]:
        y -= geschw
    if gedrueckt[pygame.K_RIGHT]:
        x += geschw
    if gedrueckt[pygame.K_DOWN]:
        y += geschw
    if gedrueckt[pygame.K_LEFT]:
        x -= geschw


    screen.blit(hintergrund, (0,0))
    pygame.draw.rect(screen,(255,255,0),(x,y,breite,hoehe))
    pygame.display.update()
    Clock.tick(60)
