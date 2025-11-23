import math
import random

from game_object import GameObject
from abc import ABC, abstractmethod


class Animal(GameObject, ABC):
    def __init__(self, color, x, y, fps, health, damage, speed, size, attack_cooldown, attack_range, rotation_speed, direction=None):

        super().__init__(x, y, fps)
        self._color = color
        self._health = health
        self._damage = damage
        self._speed = speed
        self._size = size
        self._attack_cooldown = attack_cooldown
        self._attack_range = attack_range
        self._rotation_speed = rotation_speed
        self._cooldown = 0

        if not direction:
            self._direction = random.uniform(0.0, math.pi * 2)

        else:
            self._direction = direction

    def get_size(self):
        return self._size
            
    def get_color(self):
        return self._color

    def get_health(self):
        return self._health

    @abstractmethod
    def update(self, environment):
        pass
    
    @abstractmethod
    def move(self, environment_width, environment_height):
        pass

    @abstractmethod
    def attack(self, animal):
        pass

    @abstractmethod
    def take_damage(self, damage):
        pass





