import pygame
import random
import einstellungsdaten as cfg
from sprites1 import *
from os import path

HS_FILE = "higscore.txt"
SPRITESHEET = "Cowboy4_walk without gun_0.png"
Hintergrund = pygame.image.load("western_valley.png")
START = pygame.image.load("sunset desert.png")
pygame.init()

class Game:
    def __init__(self):
        #Game Fenster
        pygame.mixer.init()
        self.screen = pygame.display.set_mode([480,600])
        pygame.display.set_caption(cfg.main_settings["title"])
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font('arial')
        self.load_data()
    
    
    #highscoreladen
    def load_data(self):
        #highscore laden
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        #load sounds
        self.sound_dir = path.join(self.dir, 'snd')
        self.jump_sound = pygame.mixer.Sound("sprung.wav")
        
        
    
    def new(self):
        #start a new game
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.plattformen = pygame.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in (cfg.plattfrom_list):
            p = Plattform(*plat)
            self.all_sprites.add(p)
            self.plattformen.add(p)
        pygame.mixer.music.load("western.ogg")
        self.run()
    def run(self):
        #Game loop
        pygame.mixer.music.play(loops=-1)
        self.clock.tick(cfg.main_settings["FPS"])
        self.playing = True
        while self.playing:
            self.clock.tick(cfg.main_settings["FPS"])
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)
    def update(self):
        #Game loop update
        self.all_sprites.update()
        #Überprüfen ob Spieler eine Plattofrm berührt - nur wenn man fällt
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.plattformen, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.y < lowest.rect.centery:
                    self.player.pos.y = lowest.rect.top
                    self.player.vel.y = 0
        #wenn Spieler das oberere Viertel erreicht
        if self.player.rect.top <= 600 / 4:
            self.player.pos.y += max(abs(self.player.vel.y),2)
            for plat in self.plattformen:
                plat.rect.y += max(abs(self.player.vel.y),2)
                if plat.rect.top >= 600:
                    plat.kill()
                    self.score += 10
        #tot
        if self.player.rect.bottom > 600:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.plattformen) == 0:
            self.playing = False
        #neue Plattformen spawnen
        while len(self.plattformen) < 6:
            width = random.randrange( 50, 100)
            p = Plattform(random.randrange(0, 480-width),
                          random.randrange(-75, -30),
                          width, 20)
            self.plattformen.add(p)
            self.all_sprites.add(p)


    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def draw(self):
        #Game loop zeichnen
        self.screen.blit(Hintergrund,(0,0))
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, (255,255,255), 480 / 2, 15)
        #nach dem zeichnen flip display
        pygame.display.flip()
    def show_start_screen(self):
        #game start screen
        pygame.mixer.music.load("Once Upon A Time.ogg")
        pygame.mixer.music.play(loops=-1)
        self.screen.blit(START, (0,0))
        self.draw_text("Western Redemption", 48,(cfg.colors["red"]), 480 / 2, 600 / 4)
        self.draw_text("a und d zum laufen, space zum springen",22, (cfg.colors["black"]),480 / 2, 600 / 2)
        self.draw_text("Taste drücken zum spielen", 22, (cfg.colors["black"]), 480 / 2, 600 * 3 / 4)
        self.draw_text("High Score:" + str(self.highscore), 22, (cfg.colors["black"]), 480 / 2, 15)
        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)
    def show_go_screen(self):
        #game over screen
        if not self.running:
            return
        pygame.mixer.music.load("rdr2.ogg")
        pygame.mixer.music.play(loops=-1)
        self.screen.fill(cfg.colors["black"])
        self.draw_text("YOU DIED!", 48, (cfg.colors["red"]), 480 / 2, 600 / 4)
        self.draw_text("Score:" + str(self.score),22, (cfg.colors["red"]),480 / 2, 600 / 2)
        if self.score < self.highscore:
            self.highscore = self.score
            self.draw_text("!New Highscore!", (cfg.colors["red"]),22, 480 / 2,600 / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score:" + str(self.highscore), 22, (cfg.colors["red"]), 480 / 2, 600 / 2 + 40)
        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(500)
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False
    #schriftart einstellungen
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)



g = Game()
g.show_start_screen()
g.new()
while True:
    g.draw()
    g.show_go_screen()

pygame.quit()
