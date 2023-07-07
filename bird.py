import pygame as pg
from settings import *
from collections import deque

# Create the Bird class as a subclass of pg.sprite.Sprite
class Bird(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_images_group)
        self.game = game
        self.image = game.bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = BIRD_POS
        self.images = deque(game.bird_images)
        self.mask = pg.mask.from_surface(self.game.bird_mask)
        self.bird_event = pg.USEREVENT + 1
        pg.time.set_timer(self.bird_event, BIRD_AN)

        self.falling_velocity = 0
        self.first_jump = False

    def animation(self):
        # Rotate through the bird images for animation
        self.images.rotate(-1)
        self.image = self.images[0]

    def rotation(self):
        # Rotate the bird image based on the falling velocity
        if self.first_jump:
            if self.falling_velocity < -JUMP * 0.3:
                self.angle = BIRD_ANGLE
            else:
                self.angle += - self.falling_velocity - BIRD_ANGLE * 0.3
            self.image = pg.transform.rotate(self.image, self.angle)
            mask_rot = pg.transform.rotate(self.game.bird_mask, self.angle)
            self.mask = pg.mask.from_surface(mask_rot)

    def check_events(self, event):
        # Check for bird events and handle them
        if event.type == self.bird_event:
            self.animation()
            self.rotation()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.first_jump = True
                self.game.sounds.wing_sound.play()
                self.falling_velocity = JUMP

    def use_gravity(self):
        # Apply gravity to the bird
        if self.first_jump:
            self.falling_velocity += GRAVITY
            self.rect.y += self.falling_velocity + 0.5 * GRAVITY

    def check_collisions(self):
        # Check for collisions with pipes, ground, and ceiling
        hit = pg.sprite.spritecollide(self, self.game.all_pipes, dokill=False, collided=pg.sprite.collide_mask)
        if hit or self.rect.bottom > GROUND_Y or self.rect.top < -self.image.get_height():
            self.game.sounds.hit_sound.play()
            pg.time.wait(1000)
            self.game.new_game()

    def update(self):
        # Update the bird
        self.check_collisions()
        self.use_gravity()
