# Import necessary modules
import pygame as pg
from settings import *
from fire import *

# Define the Menu class for displaying the main menu
class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font('assets/font/doom.ttf', 75)
        self.font_pos = WIDTH // 2.8, HEIGHT // 1.2

    def draw(self):
        # Display the main menu only if the game is not active (game_active == False)
        if not self.game.game_active:
            # Draw the fire effect in the background
            self.game.menu_fire.draw()
            
            # Display the game logo on the screen
            self.game.screen.blit(self.game.logo, MENU_POS)
            
            # Render and display the text prompting the player to click the left mouse button
            self.text = self.font.render('Click LMB to continue', True, 'red')
            self.game.screen.blit(self.text, self.font_pos)

    def update(self):
        # Update the fire effect if the game is not active
        if not self.game.game_active:
            self.game.menu_fire.update()
