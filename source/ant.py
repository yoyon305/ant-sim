import math
import random

import pygame

from animal import Animal
from pheromone import Pheromone


class Ant(Animal):


    TIME_IN_NEST = 1
    PHEROMONE_RATE = 1
    RED_IMAGE = None
    BLUE_IMAGE = None


    def __init__(self, color, x, y, fps, health, damage, speed, size, attack_cooldown, attack_range, rotation_speed, direction=None):
        super().__init__(color, x, y, fps, health, damage, speed, size, attack_cooldown, attack_range, rotation_speed, direction)
        self._food = None
        self._vision = size * 10
        self._rotation_drift = 0
        self._nest = None

        self._last_discovery = 0

        self._pheromone_rate = Ant.PHEROMONE_RATE
        self._pheromone_cooldown = 0

        self._time_in_nest = 0 #time left need to wait before leaving the nest


        self.load_image(self._size)

        if color == 0:
            self._image = Ant.RED_IMAGE
        elif color == 1:
            self._image = Ant.BLUE_IMAGE




        #self._image = pygame.transform.scale(self._image, (self._size * 15, self._size * 15))

        #add legs here:

    @classmethod
    def load_image(cls, size):
        if cls.RED_IMAGE is None or cls.BLUE_IMAGE is None:
            red_ant_image_raw = pygame.image.load("assets/red_ant.png").convert_alpha()
            blue_ant_image_raw = pygame.image.load("assets/blue_ant.png").convert_alpha()

            cls.RED_IMAGE = pygame.transform.scale(red_ant_image_raw, (size * 15, size * 15))
            cls.BLUE_IMAGE = pygame.transform.scale(blue_ant_image_raw, (size * 15, size * 15))

    def update(self, environment):

        self._last_discovery += 1

        if self._time_in_nest > 0:
            self._time_in_nest -= 1
            if self._time_in_nest <= 0:

                self.leave_nest()

            return

        if self._cooldown > 0:
            self._cooldown -= 1

            return

        closest_distance = environment.get_width() + environment.get_height()
        goal_x = None
        goal_y = None
        if not self._food:
            for food in environment.get_food():
                dist = math.dist((self._x, self._y), (food.get_x(), food.get_y()))
                if dist < self._size * 3 + food.get_size():
                    if dist < closest_distance:
                        closest_distance = dist

                        goal_x = food.get_x()
                        goal_y = food.get_y()

                    if math.dist((self._x, self._y), (food.get_x(), food.get_y())) < self._size + food.get_size():
                        #take food
                    
                        self._food = food
                        self._last_discovery = 0
                        #tells to delete the food

                        return food

            for nest in environment.get_nests():
                if nest.get_color() == self._color:
                    dist = math.dist((self._x, self._y), (nest.get_x(), nest.get_y()))
                    if dist < self._size + nest.get_size():
                        self._last_discovery = 0


            for hostile_animal in environment.get_animals():
                if hostile_animal.get_color() != self._color:
                    if math.dist((self._x, self._y), (hostile_animal.get_x(), hostile_animal.get_y())) < self._size + hostile_animal.get_size() + self._attack_range:
                        #attack hostile animal
                        
                        self.attack(hostile_animal)
                        return


        else:

            for food in environment.get_food():
                dist = math.dist((self._x, self._y), (food.get_x(), food.get_y()))
                if dist < self._size + food.get_size():
                    self._last_discovery = 0

            closest_distance = environment.get_width() + environment.get_height()
            goal_x = None
            goal_y = None
            for nest in environment.get_nests():
                if nest.get_color() == self._color:
                    dist = math.dist((self._x, self._y), (nest.get_x(), nest.get_y()))
                    if dist < self._size * 3 + nest.get_size():
                        if dist < closest_distance:
                            closest_distance = dist
                            goal_x = nest.get_x()
                            goal_y = nest.get_y()

                        if dist < self._size + nest.get_size():
                            self._x = nest.get_x()
                            self._y = nest.get_y()
                            self._nest = nest
                            self._nest.get_food(self._food, environment)
                            self._food = None
                            self._time_in_nest = Ant.TIME_IN_NEST * self._fps




        cell_size = (environment.get_width() / environment.get_cell_count())

        cell_x = int(self._x / cell_size)
        cell_y = int(self._y / cell_size)

        strongest_coord = None
        strongest_strength = 0

        type_num = 0

        if self._food:
            type_num = 1


        for i in range(max(int(cell_x - self._vision / cell_size), 0), min(int(cell_x + self._vision / cell_size), environment.get_cell_count() - 1)):
            for j in range(max(int(cell_y - self._vision / cell_size), 0), min(int(cell_y + self._vision / cell_size), int(environment.get_height() / cell_size + 1) - 1)):

                time = environment.get_cells()[i][j][self._color * Pheromone.PHEROMONE_TYPE_NUM + (Pheromone.PHEROMONE_TYPE_NUM - type_num) - 1].get_time()
                strength = environment.get_cells()[i][j][self._color * Pheromone.PHEROMONE_TYPE_NUM + (Pheromone.PHEROMONE_TYPE_NUM - type_num) - 1].get_strength()




                if 0 < time and strength > strongest_strength:

                    strongest_strength = strength
                    strongest_coord = [i, j]

        #print(weakest_strength)
        if strongest_coord or goal_x:
            #rotate to it
            self._rotation_drift = 0


            if goal_x:
                target_x = goal_x
                target_y = goal_y
            else:
                target_x = strongest_coord[0] * cell_size
                target_y = strongest_coord[1] * cell_size

            #read online
            angle = math.atan2(target_y - self._y, target_x - self._x)

            #chat gpt
            rotation = (angle - self._direction + math.pi) % (2 * math.pi) - math.pi

            if rotation != 0:
                rotation = rotation / abs(rotation) * (min(abs(rotation), self._rotation_speed / self._fps))
            self._direction += rotation
            if self._direction < 0:
                self._direction += math.pi * 2
            elif self._direction > math.pi * 2:
                self._direction -= math.pi * 2

            return self.move(environment.get_width(), environment.get_height())

        else:
            #random rotate

            #change so there is more chance the ant will rotate to the opposit direction from the rotation drift so it will do less loops of rotating the same direction
            self._rotation_drift += random.uniform((self._rotation_speed / -300 * (1 + self._rotation_drift)), (self._rotation_speed / 300 * (1 - self._rotation_drift)))

            if self._rotation_drift < -(self._rotation_speed / self._fps):
                self._rotation_drift = -(self._rotation_speed / self._fps)
            elif self._rotation_drift > (self._rotation_speed / self._fps):
                self._rotation_drift = (self._rotation_speed / self._fps)
            self._direction += self._rotation_drift / abs(self._rotation_drift) *(min(abs(self._rotation_drift), self._rotation_speed / self._fps))

            return self.move(environment.get_width(), environment.get_height())



    def move(self, environment_width, environment_height): #rads




        target_x = (math.cos(self._direction) * self._speed / self._fps) + self._x
        target_y = (math.sin(self._direction) * self._speed / self._fps) + self._y



        if target_x < 0:
            target_x = 0
        if target_x > environment_width:
            target_x = environment_width

        if target_y < 0:
            target_y = 0
        if target_y > environment_height:
            target_y = environment_height

        self._x = target_x
        self._y = target_y
        if self._pheromone_cooldown <= 0:

            self._pheromone_cooldown = self._pheromone_rate * self._fps
            return self.create_pheromone()
        self._pheromone_cooldown -= 1

    def leave_nest(self):
        if self._nest:
            self._direction = random.uniform(0.0, math.pi * 2)

            self._x = (math.cos(self._direction) * self._nest.get_size()) + self._x
            self._y = (math.sin(self._direction) * self._nest.get_size()) + self._y
            self._nest = None
            self._last_discovery = 0

    def create_pheromone(self):
        if self._food:
            return Pheromone(self._color, self._x, self._y, self._fps, self._fps * Pheromone.PHEROMONE_TIME - self._last_discovery, self._fps * Pheromone.PHEROMONE_TIME, 1)
        return Pheromone(self._color, self._x, self._y, self._fps, self._fps * Pheromone.PHEROMONE_TIME - self._last_discovery, self._fps * Pheromone.PHEROMONE_TIME, 0)

    def take_damage(self, damage):
        self._health -= damage

    def attack(self, animal):

        animal.take_damage(self._damage)
        self._cooldown = self._attack_cooldown * self._fps

    def set_nest(self, nest):
        self._nest = nest

    def get_food(self):
        return self._food

    def draw(self, screen):
        #
        # if self._time_in_nest > 0:
        #     return
        #
        #
        # target_x = (math.cos(self._direction) * self._size) * 2 + self.get_x()
        # target_y = (math.sin(self._direction) * self._size) * 2 + self.get_y()
        #
        #
        # pygame.draw.line(screen, (0, 0, 0),
        #                  [self.get_x(), self.get_y()],
        #                  [target_x, target_y], 8)
        #
        # if self._color == 0:
        #     pygame.draw.circle(screen, (0, 0, 255),
        #                        [self.get_x(), self.get_y()], self._size, 0)
        # else:
        #     pygame.draw.circle(screen, (255, 0, 0),
        #                        [self.get_x(), self.get_y()], self._size, 0)
        #

        if self._time_in_nest > 0:
            return

        rotated = pygame.transform.rotate(self._image, -math.degrees(self._direction))
        rect = rotated.get_rect(center=(self.get_x(), self.get_y()))
        screen.blit(rotated, rect)
