import pygame
import random

width = 12
height = 8
scale = 100
row = int(height / 2)
coloms = int(width / 2)
print(row)
print(coloms)

map = {}

forest_color = 'green'
desert_color = 'jelow'
mountain_color = 'blue'

for i in range(row):
    for j in range(coloms):
        map[i, j] = {'forest_strength': None, 'desert_strength': None, 'mountain_strength': None}




forest_seed_pos = (random.randint(0, row-1), random.randint(0, coloms-1))
map[forest_seed_pos]['forest_strength'] = 100
desert_seed_pos = (random.randint(0, row-1), random.randint(0, coloms-1))
map[desert_seed_pos]['desert_strength'] = 100
mountain_seed_pos = (random.randint(0, row-1), random.randint(0, coloms-1))
map[mountain_seed_pos]['mountain_strength'] = 100

print(forest_seed_pos)
print(desert_seed_pos)
print(mountain_seed_pos)


finished = False
f = 0





pygame.init()
screen = pygame.display.set_mode((width * scale, height * scale))
game_run = True
while game_run:
    for event in pygame.event.get():# event loop
        if event.type == pygame.QUIT:# checks if quit
            pygame.quit()

    screen.fill('black')

    f += 1
    finished = True
    for tile in map:
        average = 0
        n = 0
        for x in range(tile[0] - 1, tile[0] + 1):
            for y in range(tile[1] - 1, tile[1] + 1):
                if (x, y) != tile and (x, y) in map and map[(x, y)]['forest_strength'] != None:
                    average += map[(x, y)]['forest_strength']
                    n += 1
        if average != 0:
            average /= n
            map[tile]['forest_strength'] = average + random.randint(-10, 10)
        if map[tile]['forest_strength'] == None:
            finished = False
    print(finished)
    print(' ')

    for i in map:
        if map[i]['forest_strength'] != None:
            pygame.draw.rect(screen, (0, int(180 * map[i]['forest_strength'] / 100), 0), pygame.Rect((i[0]*scale, i[1]*scale), (scale, scale)))

    pygame.display.update()