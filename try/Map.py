import pygame, sys
from settings_TM import *
from debug_TM import debug
from player import Player




class Map:

    def __init__(self):
        self.player_displacement = player_displacement# + VEC(WIDTH/2, HEIGHT/2)

    def load(self):
        for x in range(int((self.player_displacement.x - player_render_dist)//tile_size), int((self.player_displacement.x + player_render_dist)//tile_size)):
            for y in range(int((self.player_displacement.y - player_render_dist)//tile_size), int((self.player_displacement.y + player_render_dist)//tile_size)):
                if not (x, y) in Tile.tiles:
                    Tile.tiles[(x, y)] = Tile(MAP_GRID[(x, y)], self.player_displacement)

    def deload(self):
        for i in Tile.isinstances:
            if (i.pos - VEC(WIDTH/2, HEIGHT/2)).magnitude() > player_deload_dist :
                i.deload()
                
    def draw(self):
        for i in Tile.isinstances:
            i.draw()

    def color_change(self):
        for i in Tile.isinstances:
            i.color_change()

    def move(self):
        self.player_displacement = player_displacement # spawn the tiles in the right pos accounting for the players displacement
        for i in Tile.isinstances:
            i.move()

    def run(self):
        self.move()
        self.load()
        self.deload()
        self.color_change()
        self.draw()


class Tile:
    isinstances = []
    tiles = {}

    def __init__(self, tile_info, displacement):
        __class__.isinstances.append(self)
        self.display_surf = pygame.display.get_surface()
        self.size = tile_size
        self.grid_pos = tile_info['pos']
        self.time_ = tile_info['time']


        # pos on the screen
        self.pos = VEC(WIDTH/2, HEIGHT/2) + VEC(self.grid_pos) * self.size - displacement
        #           bc. (0,0) topleft       



        # testing
        if (self.grid_pos[0] + self.grid_pos[1]) % 2 == 0:
            self.color = (0, 100, self.time_)
        else:
            self.color = (100, 0, self.time_)
        
        #no need
        self.current_time = pygame.time.get_ticks()



    

    def move(self):
        self.pos -= get_P_direction()

    def deload(self): 
        # update the dict of the map
        #.......
        MAP_GRID[self.grid_pos]['time'] = self.color[2]
        
        del __class__.tiles[self.grid_pos]
        __class__.isinstances.remove(self)
        del self

    def color_change(self):
        # no need
        self.delta_time = pygame.time.get_ticks() - self.current_time
        self.current_time = pygame.time.get_ticks()

        if self.color[2] < 255:
            self.color = (self.color[0], self.color[1], self.color[2] + 1)
        else:
            self.color = (self.color[0], self.color[1], 0)




    def draw(self):
        pygame.draw.rect(self.display_surf, self.color, pygame.rect.Rect((self.pos), (self.size, self.size)))
