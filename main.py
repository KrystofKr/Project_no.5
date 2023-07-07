import pygame as pg
import sys
from settings import *
from bird import *
from game_objects import *
from doom_pipes import *
from fire import *

# Create the main application class
class App:
    def __init__(self):
        # Initialize the game window and clock
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()

        # Create instances of required game objects
        self.sounds = Sounds()
        self.score = Score(self)
        self.fire = DoomFire(self)

        # Start a new game
        self.new_game()

    def load_assets(self):
        # Load and scale bird images
        self.bird_images = [pg.image.load(f"assets/bird/{i}.png").convert_alpha() for i in range(5)]
        self.bird_image = self.bird_images[0]
        bird_scale = self.bird_image.get_width() * BIRD_SCALE, self.bird_image.get_height() * BIRD_SCALE
        self.bird_images = [pg.transform.scale(sprite, bird_scale) for sprite in self.bird_images]

        # Load and scale bird mask
        self.bird_mask = pg.image.load("assets/bird/mask.png").convert_alpha()
        bird_mask_scale = self.bird_mask.get_width() * BIRD_SCALE, self.bird_mask.get_height() * BIRD_SCALE
        self.bird_mask = pg.transform.scale(self.bird_mask, bird_mask_scale)

        # Load and scale background image
        self.bg = pg.image.load("assets/images/bg.png").convert()
        self.bg = pg.transform.scale(self.bg, RES)

        # Load and scale ground image
        self.ground = pg.image.load("assets/images/ground.png").convert()
        self.ground = pg.transform.scale(self.ground, (WIDTH, GROUND_HEIGHT))

        # Load pipes images
        self.top_pipe = pg.image.load("assets/images/top_pipe.png")
        self.top_pipe = pg.transform.scale(self.top_pipe, (PIPES_WIDTH, PIPES_HEIGHT))
        self.bottom_pipe = pg.transform.flip(self.top_pipe, False, True)

    def new_game(self):
        # Load game assets
        self.load_assets()

        # Create sprite groups
        self.all_images_group = pg.sprite.Group()
        self.all_pipes = pg.sprite.Group()

        # Create game objects
        self.bird = Bird(self)
        self.bg = Background(self)
        self.ground = Ground(self)
        self.pipes = PipesHandler(self)

    def update(self):
        # Update game objects
        self.bg.update()
        self.ground.update()
        self.all_images_group.update()
        self.pipes.update()
        self.fire.update()

        # Control the frame rate
        self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        # Draw game objects on the screen
        self.bg.draw()
        self.fire.draw()
        self.all_images_group.draw(self.screen)
        self.score.draw()
        self.ground.draw()
        pg.display.flip()

    def check_events(self):
        # Check for events and handle them
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.bird.check_events(event)

    def run(self):
        # Main game loop
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    # Create an instance of the application and run it
    app = App()
    app.run()
