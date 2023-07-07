import pygame as pg
from settings import *
from random import randint

# Create the TopPipe class as a subclass of pg.sprite.Sprite
class TopPipe(pg.sprite.Sprite):
    def __init__(self, game, gap_y):
        super().__init__(game.all_images_group, game.all_pipes)
        self.image = game.top_pipe
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = WIDTH, gap_y - HALF_GAP_BETWEEN_PIPES - GROUND_HEIGHT

    def update(self):
        # Move the pipe to the left
        self.rect.right -= SCROLL_SPEED
        if self.rect.right < 0:
            # Remove the pipe from the sprite groups when it goes off the screen
            self.kill()


# Create the BottomPipe class as a subclass of TopPipe
class BottomPipe(TopPipe):
    def __init__(self, game, gap_y):
        super().__init__(game, gap_y)
        self.image = game.bottom_pipe
        self.rect = self.image.get_rect()
        self.rect.topleft = WIDTH, gap_y + HALF_GAP_BETWEEN_PIPES - GROUND_HEIGHT


# Create the PipesHandler class
class PipesHandler:
    def __init__(self, game):
        self.game = game
        self.pipe_dist = DIST_BETWEEN_PIPES
        self.points = 0
        self.pipes = []

    def score_counter(self):
        # Check if the bird has passed a pipe and update the score
        for pipe in self.pipes:
            if BIRD_POS[0] > pipe.rect.right:
                self.game.sounds.point_sound.play()
                self.points += 1
                self.pipes.remove(pipe)

    @staticmethod
    def get_gap_y():
        # Get a random y-coordinate for the gap between the pipes
        return randint(GAP_HEIGHT, HEIGHT - GAP_HEIGHT)

    def update(self):
        # Update the pipes
        self.generate_pipes()
        self.score_counter()

    def generate_pipes(self):
        if self.game.bird.first_jump:
            # Move the pipes closer together as the game progresses
            self.pipe_dist += SCROLL_SPEED
            if self.pipe_dist > DIST_BETWEEN_PIPES:
                self.pipe_dist = 0
                gap_y = self.get_gap_y()

                # Create top and bottom pipes and add them to the sprite groups
                TopPipe(self.game, gap_y)
                pipe = BottomPipe(self.game, gap_y)
                self.pipes.append(pipe)
