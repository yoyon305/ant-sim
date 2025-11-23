from abc import ABC, abstractmethod

class GameObject(ABC):

    def __init__(self, x, y, fps):
        self._x = x
        self._y = y
        self._fps = fps
    
    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y

    @abstractmethod
    def draw(self, screen):
        pass




