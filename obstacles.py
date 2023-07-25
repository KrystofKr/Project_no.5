# Import necessary modules
import pygame as pg
from settings import *
import random

# Define the Top_pipe class representing the top part of a pair of pipes
class Top_pipe(pg.sprite.Sprite):
    def __init__(self, app, gap_y):
        super().__init__(app.all_image_sprites, app.all_pipes)
        self.image = app.top_pipe_image
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.bottomleft = WIDTH, gap_y - HALF_GAP_BETWEEN_PIPES - GROUND_HEIGHT

    def update(self):
        # Move the pipe to the left (scrolling effect)
        self.rect.right -= SCROLL_SPEED
        if self.rect.right < 0:
            # If the pipe goes off the screen, remove it from the sprite groups
            self.kill()

# Define the Bottom_pipe class representing the bottom part of a pair of pipes
class Bottom_pipe(Top_pipe):
    def __init__(self, app, gap_y):
        super().__init__(app, gap_y)
        self.image = app.botton_pipe_image
        self.rect = self.image.get_rect()
        self.rect.topleft = WIDTH, gap_y + HALF_GAP_BETWEEN_PIPES - GROUND_HEIGHT

# Define the PipesHandler class responsible for generating and managing the pipes in the game
class PipesHandler:
    def __init__(self, game):
        self.game = game
        self.pipes_dist = DIST_BETWEEN_PIPES
        self.pipes = []
        self.passed_pipes = 0

    def score_counter(self):
        # Count the number of pipes the bird has passed and play a sound for each passed pipe
        for pipe in self.pipes:
            if BIRD_POS[0] > pipe.rect.right:
                self.game.sound.point_sound.play()
                self.passed_pipes += 1
                self.pipes.remove(pipe)

    def update(self):
        # Generate and update the pipes in the game
        self.generate_pipes()
        self.score_counter()

    @staticmethod
    def get_gap_y_position():
        # Get a random gap position (y-coordinate) for the pipes
        return random.randint(GAP_HEIGHT, HEIGHT - GAP_HEIGHT) + random.randint(-100, 100)

    def generate_pipes(self):
        # Generate new pipes and add them to the pipes list
        if self.game.bird.first_jump:
            self.pipes_dist += SCROLL_SPEED
            if self.pipes_dist > DIST_BETWEEN_PIPES:
                self.pipes_dist = 0
                gap_y = self.get_gap_y_position()

                Top_pipe(self.game, gap_y)
                pipe = Bottom_pipe(self.game, gap_y)
                self.pipes.append(pipe)
