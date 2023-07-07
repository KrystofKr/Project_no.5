import pygame as pg
from settings import *

# Create the Score class
class Score:
    def __init__(self, game):
        # Initialize the font
        pg.font.init()
        self.game = game
        self.font = pg.font.Font("assets/font/doom.ttf", 150)
        self.font_pos = WIDTH // 2, HEIGHT // 8

    def draw(self):
        # Draw the score on the screen
        score = self.game.pipes.points
        self.text = self.font.render(f"{score}", True, "white")
        self.game.screen.blit(self.text, self.font_pos)


# Create the Background class
class Background:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.y = 0
        self.image = self.game.bg
        self.speed = SCROLL_SPEED - 2

    def update(self):
        # Move the background horizontally
        self.x = (self.x - self.speed) % -WIDTH

    def draw(self):
        # Draw the background on the screen
        self.game.screen.blit(self.image, (self.x, self.y))
        self.game.screen.blit(self.image, (WIDTH + self.x, self.y))


# Create the Ground class as a subclass of Background
class Ground(Background):
    def __init__(self, game):
        super().__init__(game)
        self.y = GROUND_Y
        self.image = self.game.ground
        self.speed = SCROLL_SPEED


# Create the Sounds class
class Sounds:
    def __init__(self):
        # Initialize the mixer
        pg.mixer.init()
        self.wing_sound = pg.mixer.Sound('assets/sound/wing.wav')
        self.point_sound = pg.mixer.Sound('assets/sound/point.wav')
        self.hit_sound = pg.mixer.Sound('assets/sound/hit.wav')
        self.theme = pg.mixer.music.load("assets/sound/theme.mp3")
        pg.mixer.music.play(-1)
