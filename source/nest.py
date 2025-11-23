import math
from random import random

import pygame

from game_object import GameObject
import random

from source.pheromone import Pheromone


class Nest(GameObject):

    RADIUS = 25
    RADIUS_PER_LEVEL = 10

    def __init__(self, color, x, y, fps):
        super().__init__(x=x, y=y, fps=fps)

        self._x = x
        self._y = y
        self._color = color
        self._level = 1
        self._extra_food = 0
        self._xp = 0


        
    def get_color(self):
        return self._color

    def get_size(self):
        return Nest.RADIUS + Nest.RADIUS_PER_LEVEL * self._level



    #ant put food in the nest
    def get_food(self, food, environment):
        self._extra_food += food.get_value()
        while self._extra_food >= self._level + 1:
            self._xp += 1

            #create ant using the animal factory
            ant = environment.summon_object(self._color, 1, self._x, self._y, self._fps)
            ant.set_nest(self)
            ant.leave_nest()

            self._extra_food -= (self._level + 1)
        if self._xp >= self._level * 5:
            self._xp -= self._level * 5
            self._level += 1


    def update(self):
        return Pheromone(self._color, self._x, self._y, self._fps * Pheromone.PHEROMONE_TIME * 2 - 0, self._fps, 1, 0)



    def draw(self, screen):
        pygame.draw.circle(screen, (101, 67, 33),
                           [self.get_x(), self.get_y()], self.get_size(), 0)


