import pygame 
import einstellungsdaten as cfg
vec = pygame.math.Vector2

#variablen
player_acc = 0.5
player_friction = -0.12
player_grav = 0.8
player_jump = 20
YELLOW = (255,255,0)
class Spritesheets:
    def __init__(self):
        self.spritesheets = Spritesheets
    

    def get_image(self, x, y , width, height):
        image = pygame.Surface((width,height))
        image.blit(self.spritesheets, (0,0), (x, y, width, height))
        image = pygame.transform.scale(image, ())
        return image
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        #Spieler Ausrichtung usw.
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load('Cowboy4_walk without gun_0.png')
        self.rect = self.image.get_rect()
        self.rect.center = (40, 600 - 100)
        self.pos = vec(10 ,600 - 100)
        self.vel = vec(0,0)
        self.acc = (0,0)

    def jump(self):
        #Überprüfen ob Spieler auf Plattform steht
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.plattformen, False)
        self.rect.x -= 1
        if hits:
            self.game.jump_sound.play()
            self.vel.y = -player_jump
    def update(self):
        #Tastatur Eingabe
        self.acc = vec(0,player_grav)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acc.x = -player_acc
        if keys[pygame.K_d]:
            self.acc.x = player_acc
        
        #player friction
        self.acc.x += self.vel.x * player_friction

        #bewegungen
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #barriere rund um den screen
        if self.pos.x > (cfg.main_settings["width"]):
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x =(cfg.main_settings["width"])
 
        self.rect.midbottom = self.pos

class Plattform(pygame.sprite.Sprite):
    #Plattformen einstellungen
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ground_sand_broken.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
       
       
