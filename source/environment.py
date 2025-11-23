import pygame

from pheromone import Pheromone
from source.animal_factory import AnimalFactory
from source.food import Food
from source.nest import Nest
from source.corn import Corn


class Environment:
    
    #in this program size is the radius of hitbox


    def __init__(self, width, height, fps, cell_count, color_num, animal_factory):
        
        
        self._width = width
        self._height = height
        self._cell_count = cell_count
        self._color_num = color_num
        self._fps = fps

        self._animals = []
        self._nests = []
        self._food = []
        self._cells = []
        self._pheromones = []
        self._animal_factory = animal_factory





        cell_size = self._width / self._cell_count

        for i in range(int(self._width / cell_size + 1)):
            self._cells.append([])
            for j in range(int(self._height / cell_size + 1)):
                self._cells[i].append([])

                for color in range(color_num):

                    x = cell_size * i
                    y = cell_size * j
                    for type_num in range(Pheromone.PHEROMONE_TYPE_NUM):
                        self._cells[i][j].append(Pheromone(color, x, y, self._fps, 0, 0, type_num))

    def simulate(self):

        live_animals = []
        effective_pheromones = []

        for nest in self._nests:
            action = nest.update()
            x = action.get_x()
            y = action.get_y()
            t = action.get_color() * Pheromone.PHEROMONE_TYPE_NUM + action.get_type()
            cell_size = self._width / self._cell_count
            if self._cells[int(x / cell_size)][int(y / cell_size)][int(t)].get_strength() < action.get_strength():
                self._cells[int(x / cell_size)][int(y / cell_size)][int(t)] = action


        #update animals
        for animal in self._animals:
            action = animal.update(self)


            if isinstance(action, Food):
                #animal took food
                self._food.remove(action)
            elif isinstance(action, Pheromone):

                #animal created pheromone
                self._pheromones.append(action)
                x = action.get_x()
                y = action.get_y()
                t = action.get_color() * Pheromone.PHEROMONE_TYPE_NUM + action.get_type()
                cell_size = self._width / self._cell_count
                if self._cells[int(x / cell_size)][int(y / cell_size)][int(t)].get_strength() < action.get_strength():
                    self._cells[int(x / cell_size)][int(y / cell_size)][int(t)] = action
                    

        #remove dead animals
        for animal in self._animals:
            if animal.get_health() > 0:
                live_animals.append(animal)

            elif animal.get_food():
                food = animal.get_food()
                food.set_x(animal.get_x())
                food.set_y(animal.get_y())
                self._food.append(food)

        #update animals with only living animals
        self._animals = live_animals

        #update pheromones
        for pheromone in self._pheromones:
            pheromone.update()
            if pheromone.get_time() > 0 and pheromone.get_strength() > 0:
                effective_pheromones.append(pheromone)

        #update pheromones with only effective pheromones
        self._pheromones = effective_pheromones
        cell_size = (self._width / self._cell_count)

        #update the grid of pheromones
        for i in range(int(self._width / cell_size + 1)):
            for j in range(int(self._height / cell_size + 1)):
                for color in range(self._color_num):
                    for type_num in range(Pheromone.PHEROMONE_TYPE_NUM):
                        self._cells[i][j][color * Pheromone.PHEROMONE_TYPE_NUM + (Pheromone.PHEROMONE_TYPE_NUM - type_num) - 1].update()
        


    def summon_object(self, color, number, x, y, fps):

        object = None

        if number == 0:
            #nest
            object = Nest(color, x, y, fps)
            self._nests.append(object)


        elif number == 1:
            #ant
            object = self._animal_factory.create_animal(color, x, y, "Ant")
            self._animals.append(object)

        elif number == 2:
            #corn

            object = Corn(x, y, fps)
            self._food.append(object)

        else:
            print(number)
            return

        return object

                        
    def get_width(self):
        return self._width
    
    def get_height(self):
        return self._height
    
    def get_cell_count(self):
        return self._cell_count

    def get_cells(self):
        return self._cells
    
    def get_food(self):
        return self._food
    
    def get_animals(self):
        return self._animals
    
    def get_nests(self):
        return self._nests

    def get_pheromones(self):
        return self._pheromones

    
    





