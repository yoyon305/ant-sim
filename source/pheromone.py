import pygame

from game_object import GameObject



class Pheromone(GameObject):

    PHEROMONE_TYPE_NUM = 2
    PHEROMONE_TIME = 40
    PHEROMONE_SIZE = 8
    T1_IMAGE = None
    T2_IMAGE = None

    
    def __init__(self, color, x, y, fps, strength, time, type):

        super().__init__(x, y, fps)
        self._color = color
        self._strength = strength
        self._type = type #0 is searching for food, 1 is found food
        self._time = time
        self.load_image()

        if type == 0:
            self._image = Pheromone.T1_IMAGE
        elif type == 1:
            self._image = Pheromone.T2_IMAGE




    @classmethod
    def load_image(cls):
        if cls.T1_IMAGE is None or cls.T2_IMAGE is None:

            t1_image_raw = pygame.image.load("assets/green_pheromone.png").convert_alpha()
            t2_image_raw = pygame.image.load("assets/orange_pheromone.png").convert_alpha()

            cls.T1_IMAGE = pygame.transform.scale(t1_image_raw, (cls.PHEROMONE_SIZE * 1.3, cls.PHEROMONE_SIZE * 1.3))
            cls.T2_IMAGE = pygame.transform.scale(t2_image_raw, (cls.PHEROMONE_SIZE * 1.3, cls.PHEROMONE_SIZE * 1.3))
        
    def update(self):
        if self._time > 0:
            self._time -= 1
        if self._strength > 0:
            self._strength -= 0.1
        
    def get_strength(self):
        return self._strength
    
    def get_color(self):
        return self._color
    
    def get_type(self):
        return self._type

    def get_time(self):
        return self._time

    def draw(self, screen):

        #if self._type == 0:
        #    pygame.draw.circle(screen, (255, 165, 0),
        #                   [self._x, self._y], Pheromone.PHEROMONE_SIZE, 0)
        #else:
        #    pygame.draw.circle(screen, (190, 190, 190),
        #                   [self._x, self._y], Pheromone.PHEROMONE_SIZE, 0)

        image_with_alpha = self._image.copy()


        alpha = self._time / (Pheromone.PHEROMONE_TIME * self._fps) * 256
        image_with_alpha.set_alpha(alpha)

        screen.blit(image_with_alpha, (self._x - (Pheromone.PHEROMONE_SIZE * 1.3)/ 2,
                                       self._y - (Pheromone.PHEROMONE_SIZE * 1.3) / 2))

        
        
        
        

