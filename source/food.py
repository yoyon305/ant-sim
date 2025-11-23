from abc import ABC

from game_object import GameObject


class Food(GameObject, ABC):
    def __init__(self, x, y, fps, size, value):
        super().__init__(x, y, fps)
        self._value = value
        self._size = size
        
    def get_value(self):
        return self._value

    def get_size(self):
        return self._size

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y