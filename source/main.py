import pygame

from source.animal_factory import AnimalFactory
from source.corn import Corn
from source.environment import Environment

FPS = 30
WIDTH = 1000
HEIGHT = 600
CELL_COUNT = 200
COLOR_NUM = 2
NUM_OF_UNIT_TYPES = 3 # nest, ant, corn

selected_number = 0
selected_color = 0
start_sim = False

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ant Sim")

clock = pygame.time.Clock()


background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


red_ant_image_raw = pygame.image.load("assets/red_ant.png").convert_alpha()
blue_ant_image_raw = pygame.image.load("assets/blue_ant.png").convert_alpha()


red_ant_image = pygame.transform.scale(red_ant_image_raw, (AnimalFactory.ANT_STATS[3] * 15, AnimalFactory.ANT_STATS[3] * 15))
blue_ant_image = pygame.transform.scale(blue_ant_image_raw, (AnimalFactory.ANT_STATS[3] * 15, AnimalFactory.ANT_STATS[3] * 15))

animal_factory = AnimalFactory(FPS)

environment = Environment(WIDTH, HEIGHT, FPS, CELL_COUNT, COLOR_NUM, animal_factory)

Corn.load_image()

# Game loop
running = True
while running:



    screen.blit(background, (0, 0))  # Draw the background
    #pygame.display.flip()
    #screen.fill((0, 100, 0))

    if start_sim:
        environment.simulate()



    for pheromone in environment.get_pheromones():
        pheromone.draw(screen)


    for nest in environment.get_nests():
        nest.draw(screen)



    for food in environment.get_food():
        food.draw(screen)

    for animal in environment.get_animals():
        animal.draw(screen)

    pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                selected_color = (selected_color + 1) % COLOR_NUM
            elif event.y < 0:
                selected_color = (selected_color - 1) % COLOR_NUM

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos

                #summon object
                environment.summon_object(selected_color, selected_number, x, y, FPS)





        elif event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_9:
                selected_number = ((event.key - pygame.K_1) % NUM_OF_UNIT_TYPES)
            elif pygame.K_SPACE:
                start_sim = True

    clock.tick(FPS)

