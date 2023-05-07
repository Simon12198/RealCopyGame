from csv import reader
import pygame

global tile_size

def import_csv_files(path):
    game_map = []
    with open(path) as map:
        level = reader(map, delimiter= ',')
        for row in level:
            game_map.append(list(row))
        return game_map

def slicing_tiles(path, tile_size = (32, 32)):
    image = pygame.image.load(path).convert_alpha()
    tile_x = int(image.get_size()[0] / tile_size[0])
    tile_y = int(image.get_size()[1] / tile_size[1])
    tiles = []
    for row in range(tile_y):
        for col in range(tile_x):
            x = col * tile_size[0]
            y = row * tile_size[1]
            surface = pygame.Surface((tile_size[0], tile_size[1]))
            surface.set_colorkey((0, 0, 0))
            surface.blit(image, (0, 0), pygame.Rect(x, y, tile_size[0], tile_size[1]))
            tiles.append(surface)

    return tiles


