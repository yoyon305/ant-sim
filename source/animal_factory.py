import pygame

from source.ant import Ant


class AnimalFactory:


    #health, damage, speed, size, attack_cooldown, attack_range, rotation_speed
    ANT_STATS = [100, 30, 60, 8, 1.5, 10, 3]




    def __init__(self, fps):
        self._fps = fps



    def create_animal(self, color, x, y, name):

        if name == "Ant":

            return Ant(color, x, y, self._fps, *AnimalFactory.ANT_STATS)


