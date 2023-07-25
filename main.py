# Import necessary modules
import pygame as pg
import sys
from os import path
from bird import *
from obstacles import *
from game_objects import *
from settings import *
from fire import *
from menu import *


class FlappyDoom:
    def __init__(self):
        pg.init()

        # Initialize game_active flag as False to start in the main menu
        self.game_active = False

        # Create the game window and clock
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()

        # Get the path to the current directory
        self.dir = path.dirname(__file__)

        # Load game assets
        self.load_assets()

        # Initialize the sound, score, menu, and fire objects
        self.sound = Sound()
        self.score = Score(self)
        self.menu = Menu(self)
        self.fire = DoomFire(self, STEPS_BETWEEN_COLORS_GAME)
        self.menu_fire = DoomFire(self, STEPS_BETWEEN_COLORS_MENU)
        self.new_game()

        # Click counter to track how many times the player clicks the mouse
        self.click_counter = 0

    def load_assets(self):
        # Load bird images and scale them to the desired size
        self.bird_images = [pg.image.load(f"assets/bird/{i}.png").convert_alpha() for i in range(5)]
        bird_size = self.bird_images[0].get_width() * BIRD_SCALE, self.bird_images[0].get_height() * BIRD_SCALE
        self.bird_images = [pg.transform.scale(sprite, bird_size) for sprite in self.bird_images]

        # Load background images and exclude the ones that are not needed
        image_filenames = []
        for i in range(9):
            if i not in (2, 3):
                image_filenames.append(f"assets/images/d_{i + 1}.png")
        self.background_images = [pg.image.load(filename).convert() for filename in image_filenames]

        # Load ground image and scale it to the desired size
        self.ground_image = pg.image.load("assets/images/ground.png")
        self.ground_image = pg.transform.scale(self.ground_image, (WIDTH, GROUND_HEIGHT))

        # Load pipe images and flip the bottom pipe image to create pairs of pipes
        self.top_pipe_image = pg.image.load("assets/images/top_pipe.png")
        self.top_pipe_image = pg.transform.scale(self.top_pipe_image, (PIPES_WIDTH, PIPES_HEIGHT))
        self.botton_pipe_image = pg.transform.flip(self.top_pipe_image, False, True)

        # Load the bird's mask image and scale it to the desired size
        self.mask = pg.image.load('assets/bird/mask.png')
        self.mask_size = self.mask.get_width() * BIRD_SCALE, self.mask.get_height() * BIRD_SCALE
        self.mask = pg.transform.scale(self.mask, self.mask_size)

        # Load the game logo and scale it to the menu size
        self.logo = pg.image.load("assets/images/logo.png")
        self.logo = pg.transform.scale(self.logo, MENU_RES)

    def new_game(self):
        # Read the high score from the file or set it to 0 if the file is not available
        with open(path.join(self.dir, HG_file), "r") as hg:
            try:
                self.high_score = int(hg.read())
            except:
                self.high_score = 0

        # Create sprite groups and initialize game objects for a new game
        self.all_image_sprites = pg.sprite.Group()
        self.all_pipes = pg.sprite.Group()
        self.bird = Bird(self)
        self.bg = Background(self)
        self.ground = Ground(self)
        self.pipe_handler = PipesHandler(self)

    def draw(self):
        # Draw the menu and game objects depending on the game_active flag
        self.menu.draw()
        if self.game_active:
            self.bg.draw()
            self.fire.draw()
            self.all_image_sprites.draw(self.screen)
            self.ground.draw()
            self.score.draw()

        pg.display.flip()

    def update(self):
        # Update the menu and game objects depending on the game_active flag
        self.menu.update()
        if self.game_active:
            self.bg.update()
            self.ground.update()
            self.all_image_sprites.update()
            self.pipe_handler.update()
            self.fire.update()
            self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Handle quitting the game
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Increment the click_counter when the player clicks the left mouse button
                    self.click_counter += 1
                    self.game_active = True  # Start the game when the player clicks
            self.bird.check_event(event)

    def run(self):
        while True:
            # Check events, update the game state, and draw the screen
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    # Create a FlappyDoom object and run the game
    game = FlappyDoom()
    game.run()
