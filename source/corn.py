import math

import pygame

from source.food import Food



class Corn(Food):
    SIZE = 20
    IMAGE = None



    def __init__(self, x, y, fps):
        
        super().__init__(x=x, y=y, fps=fps, size=Corn.SIZE, value=1)

    @classmethod
    def load_image(cls):
        if cls.IMAGE is None:
            cls.IMAGE = pygame.image.load("assets/corn.png").convert_alpha()
            cls.IMAGE = pygame.transform.scale(cls.IMAGE, (cls.SIZE, cls.SIZE))

    def draw(self, screen):

        screen.blit(Corn.IMAGE, (self._x - Corn.SIZE / 2, self._y - Corn.SIZE / 2))

        #pygame.draw.circle(screen, (255, 255, 255),
        #        [self.get_x(), self.get_y()], self._size, 0)



