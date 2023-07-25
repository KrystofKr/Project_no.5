# Import the necessary modules
import pygame as pg
from collections import deque
from settings import *

# Define a class for the bird sprite
class Bird(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_image_sprites)
        self.game = game
        self.image = game.bird_images[0]
        self.mask = pg.mask.from_surface(game.mask)
        self.rect = self.image.get_rect()
        self.rect.center = BIRD_POS

        # Use a deque to store bird images for animation
        self.images = deque(game.bird_images)

        # Set up a timer event for bird animation
        self.animation_event = pg.USEREVENT + 0
        pg.time.set_timer(self.animation_event, BIRD_ANIMATION_TIMER)

        self.falling_velocity = 0
        self.first_jump = False

    # Function to handle bird rotation during its movement
    def rotation(self):
        if self.first_jump:
            # Rotate the bird image based on its falling velocity
            if self.falling_velocity < -BIRD_JUMP * 0.3:
                self.angle = BIRD_ANGLE
            else:
                self.angle = - BIRD_ANGLE
            self.image = pg.transform.rotate(self.image, self.angle)
            self.mask = pg.transform.rotate(self.game.mask, self.angle)
            self.mask = pg.mask.from_surface(self.mask)

    # Function to check for collisions with pipes and the ground
    def check_collision(self):
        hit = pg.sprite.spritecollide(self, self.game.all_pipes, dokill=False, collided=pg.sprite.collide_mask)
        if hit or self.rect.bottom > GROUND_Y or self.rect.top < -self.image.get_height():
            # Play a sound when the bird collides with an obstacle or goes out of bounds
            self.game.sound.hit_sound.play()
            # Wait for 1 second before starting a new game
            pg.time.wait(1000)
            self.game.new_game()

    # Function to simulate gravity on the bird's movement
    def use_gravity(self):
        if self.first_jump:
            self.falling_velocity += GRAVITY
            self.rect.y += self.falling_velocity + 0.5 * GRAVITY

    def update(self):
        # Check for collisions
        self.check_collision()
        # Apply gravity to the bird
        self.use_gravity()

    # Function to handle bird animation
    def animation(self):
        # Rotate the deque of bird images to the left, making the next image the current one
        self.images.rotate(-1)
        self.image = self.images[0]

    # Function to check events related to the bird
    def check_event(self, event):
        # Check if it's time for the bird animation event
        if event.type == self.animation_event:
            # Perform bird animation
            self.animation()
            # Rotate the bird based on its movement
            self.rotation()
        # Check if a mouse button is pressed (left click)
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.game.click_counter > 1:
                # Set first_jump to True when the player clicks the mouse
                self.first_jump = True
                # Play a wing sound to simulate the bird flapping its wings
                self.game.sound.wing_sound.play()
                # Apply an initial upward velocity to the bird to make it jump
                self.falling_velocity = BIRD_JUMP
