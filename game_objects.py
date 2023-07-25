# Import necessary modules
import pygame as pg
from settings import * 
from os import path
from random import choice

# Define the Score class for displaying and tracking the player's score and best score
class Score:
    def __init__(self, game):
        self.game = game
        self.font_pos = WIDTH // 2, HEIGHT // 8
        self.best_score_pos = 0, 0

    def draw(self):
        # Get the current score and best score
        score = self.game.pipe_handler.passed_pipes
        best_score = self.game.high_score

        # Render the current score and display it on the screen
        self.font = pg.font.Font('assets/font/doom.ttf', 150)
        self.text = self.font.render(f'{score}', True, 'white')
        self.game.screen.blit(self.text, self.font_pos)

        # Update the best score and save it to a file if a new best score is achieved
        if score > best_score:
            with open(path.join(self.game.dir, HG_file), 'w') as hg:
                hg.write(str(score))

        # Render and display the best score on the screen
        self.font = pg.font.Font('assets/font/doom.ttf', 100)
        self.best_score_text = self.font.render(f'Best Score: {best_score}', True, 'white')
        self.game.screen.blit(self.best_score_text, self.best_score_pos)

# Define the Sound class to manage game sounds
class Sound:
    def __init__(self):
        # Load and set up game sounds
        self.hit_sound = pg.mixer.Sound('assets/sound/hit.wav')
        self.point_sound = pg.mixer.Sound('assets/sound/point.wav')
        self.wing_sound = pg.mixer.Sound('assets/sound/wing.wav')
        self.wing_sound.set_volume(0.6)

        # Load and play the game theme music
        self.theme = pg.mixer.music.load('assets/sound/theme.mp3')
        pg.mixer.music.set_volume(0.75)
        pg.mixer.music.play(-1)

# Define the Background class to manage scrolling background images
class Background:
    def __init__(self, game):
        self.game = game
        self.x = 0
        self.speed = SCROLL_SPEED - 2
        self.image_width, self.image_height = self.game.background_images[0].get_size()
        self.bg_images = self.game.background_images.copy()

    def update(self):
        # Update the x position for scrolling the background
        self.x = (self.x - self.speed) 
        if self.x <= -self.image_width:
            # If the first image goes off the screen, replace it with a new image from the background_images list
            self.bg_images.pop(0)
            new_image = choice(self.game.background_images)
            self.bg_images.append(new_image)
            self.x = 0

    def draw(self):
        # Draw the scrolling background images on the screen
        self.game.screen.blit(self.bg_images[0], (self.x, 0))
        self.game.screen.blit(self.bg_images[1], (self.x + self.image_width, 0))
        self.game.screen.blit(self.bg_images[2], (self.x + self.image_width * 2, 0))

# Define the Ground class to manage the scrolling ground image
class Ground(Background):
    def __init__(self, game):
        super().__init__(game)
        self.y = GROUND_Y
        self.speed = SCROLL_SPEED
        self.image = self.game.ground_image

    def draw(self):
        # Draw the scrolling ground image on the screen
        self.game.screen.blit(self.image, (self.x, self.y))
        self.game.screen.blit(self.image, (self.x + WIDTH, self.y))

    def update(self):
        # Update the x position for scrolling the ground
        self.x = (self.x - self.speed) % -WIDTH
