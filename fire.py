# Import necessary modules
import pygame as pg
from pygame import gfxdraw
from random import randint
from settings import *

# Define the DoomFire class
class DoomFire:
    def __init__(self, app, num_of_reps):
        # Initialize the DoomFire object with the app and number of repetitions for the fire palette
        self.app = app
        self.palette = self.get_palette(num_of_reps)
        
        # Create a 2D array representing the fire and initialize it
        self.fire_array = self.get_fire_array()
        
        # Create a surface to draw the fire effect
        self.fire_surf = pg.Surface([PIXEL_SIZE * FIRE_WIDTH, HEIGHT])

        # Create a surface to store the scrolling fire effect
        self.fire_screen_surf = pg.Surface(RES)
        self.fire_screen_surf.set_colorkey('black')
        
        # Set the speed of scrolling and the initial x position
        self.speed = SCROLL_SPEED
        self.x = 0

    def do_fire(self):
        # Function to update the fire effect frame by frame
        for x in range(FIRE_WIDTH):
            for y in range(1, FIRE_HEIGHT):
                color_index = self.fire_array[y][x]
                if color_index:
                    # Randomly spread the fire upwards for the current pixel
                    rnd = randint(0, 3)
                    self.fire_array[y - 1][(x - rnd + 1) % FIRE_WIDTH] = color_index - rnd % 2
                else:
                    # If the pixel is not on fire, reduce its intensity
                    self.fire_array[y - 1][x] = 0

    def draw_fire(self):
        # Function to draw the fire effect on the fire_surf
        self.fire_surf.fill('black')
        for y, row in enumerate(self.fire_array):
            for x, color_index in enumerate(row):
                if color_index:
                    # Use gfxdraw.box to draw individual rectangles for the fire effect
                    color = self.palette[color_index]
                    gfxdraw.box(self.fire_surf, (x * PIXEL_SIZE, y * PIXEL_SIZE,
                                                  PIXEL_SIZE, PIXEL_SIZE), color)

        # Tile the fire_surf horizontally multiple times to create the scrolling effect
        for i in range(FIRE_REPS):
            self.fire_screen_surf.blit(self.fire_surf, (self.fire_surf.get_width() * i, 0))
        
        # Draw the final fire effect on the screen (depending on game_active state)
        if self.app.game_active:
            self.app.screen.blit(self.fire_screen_surf, (self.x, -GROUND_HEIGHT))
            self.app.screen.blit(self.fire_screen_surf, (WIDTH + self.x, -GROUND_HEIGHT))
        else:
            self.app.screen.blit(self.fire_screen_surf, (self.x, 0))
            self.app.screen.blit(self.fire_screen_surf, (WIDTH + self.x, 0))

    def get_fire_array(self):
        # Function to initialize the fire array with the bottom row on fire
        fire_array = [[0 for i in range(FIRE_WIDTH)] for j in range(FIRE_HEIGHT)]
        for i in range(FIRE_WIDTH):
            fire_array[FIRE_HEIGHT - 1][i] = len(self.palette) - 1
        return fire_array

    def move_fire(self):
        # Function to update the x position for scrolling the fire effect
        self.x = (self.x - self.speed) % -WIDTH

    @staticmethod
    def get_palette(num_of_reps):
        # Function to generate the fire color palette based on the number of repetitions
        palette = [(0, 0, 0)]  # Start with a black color
        for i, color in enumerate(COLORS[:-1]):
            c1, c2 = color, COLORS[i + 1]
            for step in range(num_of_reps):
                # Interpolate colors between c1 and c2 to create a smooth transition
                c = pg.Color(c1).lerp(c2, (step + 0.5) / num_of_reps)
                palette.append(c)
        return palette

    def update(self):
        # Function to update the fire effect
        self.do_fire()
        self.move_fire()

    def draw(self):
        # Function to draw the fire effect on the screen
        self.draw_fire()
