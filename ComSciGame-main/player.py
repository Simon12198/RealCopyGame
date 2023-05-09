import pygame, os, math
from animation import load_animations

def flip(img, boolean):
    pygame.transform.flip(img, boolean, False)

def collision_detection(rect1, rect_list):
    hit_list = []
    for rect in rect_list:
        if rect.colliderect(rect1):
            hit_list.append(rect1)
    return hit_list

class Player(pygame.sprite.Sprite):
    def __init__(self, loc):
        super().__init__()
        # player animation
        self.import_animation()
        self.frame = 0
        self.action = ''
        self.change_action('idle')
        self.flip = False
        self.collide_bottom = False

        self.image = self.animations[self.action][self.anim[self.frame]]
        self.rect = self.image.get_rect(topleft = loc)
        #debugging for slope collisions by pixel
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.DEBUG = False

        #player movement
        self.x = loc[0]
        self.y = loc[1]
        self.movement = [0, 0]
        self.air_timer = 0
        self.velocity = 0
        self.vertical_momentum = 0
        self.direction = [False, False]
        self.jump_held = False
        self.gravity_multiplier = 0.2
        self.n = 0

    def get_input(self):

        self.movement = [0, 0]
        self.keys = pygame.key.get_pressed()
        if self.keys[pygame.K_d]:
            self.DEBUG = True
        if self.keys[pygame.K_f]:
            self.DEBUG = False

        if self.DEBUG:
            if self.keys[pygame.K_RIGHT]:

                self.movement[0] += 1
                self.direction = [True, False]
                self.flip = False

            elif self.keys[pygame.K_LEFT]:
                self.movement[0] -= 1
                self.direction = [False, True]
                self.flip = True

            if self.keys[pygame.K_UP]:
                self.movement[1] = -1

            if self.keys[pygame.K_DOWN]:
                self.movement[1] = 1
        else:
            self.keys = pygame.key.get_pressed()
            if self.keys[pygame.K_RIGHT]:

                self.movement[0] += 3
                self.direction = [True, False]
                self.flip = False
                if -0.2 < self.vertical_momentum < 0.2 and self.keys[pygame.K_SPACE]:
                    self.movement[0] += 1
            elif self.keys[pygame.K_LEFT]:
                self.movement[0] -= 3
                self.direction = [False, True]
                self.flip = True
                if -0.2 < self.vertical_momentum < 0.2 and self.keys[pygame.K_SPACE]:
                    self.movement[0] -= 1
            else:
                self.direction = [False, False]
            if self.keys[pygame.K_SPACE]:
                if self.air_timer < 6:
                    self.vertical_momentum = -4

    def gravity(self):
        self.gravity_multiplier = 0.2
        if self.vertical_momentum > 0.4:
            self.gravity_multiplier = 0.5
        elif self.vertical_momentum < 0 and not(self.keys[pygame.K_SPACE]):
            self.vertical_momentum += 1
        self.movement[1] += self.vertical_momentum
        self.vertical_momentum += self.gravity_multiplier
        if self.vertical_momentum > 3:
            self.vertical_momentum = 3

    def import_animation(self):
        path = 'data/graphics/'
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
        animation_data = load_animations(path)
        self.animation_frames = animation_data[0]
        for animation in self.animations.keys():
            self.animations[animation] = animation_data[1]


    def flip(self, boolean):
        self.flip = boolean

    def change_action(self, new_action):
        if self.action == new_action:
            pass
        else:
            self.action = new_action
            self.frame = 0
            self.anim = self.animation_frames[self.action]


    def implement_anim(self, loop):
        self.frame += 1
        while self.frame >= len(self.anim):
            if loop:
                self.frame -= len(self.anim)
        image = self.animations[self.action][self.anim[self.frame]]
        self.image = pygame.transform.flip(image, self.flip, False)


    def status(self):
        if self.movement[1] < 0:
            self.change_action('jump')
        elif self.movement[1] > 1:
            self.change_action('fall')
        else:
            if self.movement[0] == 0:
                self.change_action('idle')
            if self.movement[0] > 0:
                self.change_action('run')
            if self.movement[0] < 0:
                self.change_action('run')



    def update(self, scroll):
        self.get_input()
        # gravity
        if not self.DEBUG:
            self.gravity()
        self.movement[1] += self.vertical_momentum


        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]

        self.implement_anim(True)
        self.mask = pygame.mask.from_surface(self.image.convert_alpha())
        self.status()













