import pygame
import random
from settings import *





pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption(title)
clock = pygame.time.Clock()


all_sprites.add(player)
#Game loop
running = True
while running:
    clock.tick(FPS)
    #events
    for event in pygame.event.get():
        #Fenster schliessen
        if event.type == pygame.QUIT:
            running = False 

    #update
    all_sprites.update()
    #zeichnen
    screen.fill(black)
    all_sprites.draw(screen)
    #nach dem zeichnen flip display
    pygame.display.flip()

pygame.quit()