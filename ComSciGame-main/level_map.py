from player import Player
from player import *
from csv_loader import *

tile_size = 32

SCREEN_WIDTH = 1200
screen_height = 640

rescaled_width = 600
rescaled_height = 320


class Tiles(pygame.sprite.Sprite):
    def __init__(self, size, loc):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=loc)

    def update(self, scroll):
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]


class ground_tile(Tiles):
    def __init__(self, size, loc, img):
        super().__init__(size, loc)
        self.image = img
        self.mask = pygame.mask.from_surface(img)


class Level:


    def __init__(self, game_map, path, surface):
        self.game_map = game_map
        self.surface = surface
        self.game_map = self.load_map(path)

        self.player = pygame.sprite.GroupSingle()
        self.tiles = pygame.sprite.Group()
        self.bg_objects = pygame.sprite.Group()
        self.coin = pygame.sprite.Group()
        self.Death = pygame.sprite.Group()
        self.slopesgroup = pygame.sprite.Group()
        self.player_on_slope = False
        self.bg_imgs = pygame.sprite.Group()

        self.terrain_layout = import_csv_files(self.game_map['Grass'])
        self.terrain_sprites = self.create_sprite(self.terrain_layout, 'Grass')

        self.Gold = import_csv_files(self.game_map['Gold'])
        self.create_sprite(self.Gold, 'Gold')

        self.trees = import_csv_files(self.game_map['Trees'])
        self.create_sprite(self.trees, 'Trees')

        self.slope_layout = import_csv_files(self.game_map['Slopes'])
        self.slope_sprites = self.create_sprite(self.slope_layout, 'Slopes')

        self.spawn = import_csv_files(self.game_map['Spawn'])
        self.create_sprite(self.spawn, 'Spawn')

        self.death = import_csv_files(self.game_map['Death'])
        self.create_sprite(self.death, 'Death')

    def load_map(self, path):
        level_data = {}
        f = open(path + 'level', 'r')
        self.level = f.read()
        f.close()
        self.level = self.level.split('\n')
        for name in self.level:
            paths = path.split('/')
            level_name = paths[2]
            level_data[name] = path + level_name + '_' + name + '.csv'
        return (level_data)

    def create_sprite(self, layout, type):

        row_index = 0
        for row in layout:
            col_index = 0
            for col in row:
                if col != '-1':
                    if type == 'Grass':
                        terrain_layout = slicing_tiles('data/graphics/Terrain/Grass/Grass.png')
                        tile = terrain_layout[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tile)
                        self.tiles.add(sprite)
                    if type == 'Gold':
                        gold = slicing_tiles('data/graphics/Terrain/Coin/gold_coin.png')
                        tiles = gold[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tiles)
                        self.coin.add(sprite)
                    if type == 'Death':
                        death = slicing_tiles('data/graphics/Terrain/Death/Death.png')
                        tileset = death[int(col)]
                        sprite = ground_tile(tile_size, [col_index * 32, row_index * 32], tileset)
                        self.Death.add(sprite)
                    if type == 'Spawn':
                        player = Player([col_index * 32, row_index * 32])
                        self.player.add(player)
                    if type == 'Slopes':
                        slope_layout = slicing_tiles('data/graphics/Terrain/Slopes/Slopes.png')
                        ramps = slope_layout[int(col)]
                        sprited = ground_tile(tile_size, [col_index * 32, row_index * 32], ramps)
                        self.slopesgroup.add(sprited)
                     #  self.slope.types = ['topslopeleft', 'topsloperight','leftsteep','leftlong','rightsteep','rightlong']
                     #topsloperight id = 40, topsloperight = 42, left steep = 6, 14 left long = 20,21,29, right steep = 7, 15, rightlong = 22, 23, 30

                col_index += 1

            row_index += 1
        self.tile_sprites = self.tiles.sprites()
        self.slope_sprite = self.slopesgroup.sprites()

    def scrolling(self):
        player = self.player.sprite
        true_scroll = [0, 0]
        true_scroll[0] += (player.rect.x - true_scroll[0] - rescaled_width // 2) / 15
        true_scroll[1] += (player.rect.y - true_scroll[1] - rescaled_height // 2) / 15
        self.scroll = true_scroll.copy()
        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])

    def check_slope_collision(self):
        player = self.player.sprite
        player.x = player.rect.x
        player.x += player.movement[0]
        player.rect.x = int(player.x)
        #self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        for slopes in self.slopesgroup.sprites():
            if slopes.rect.colliderect(player.rect):
                offset = (slopes.rect.left - player.rect.left, slopes.rect.top - player.rect.top)
                return player.mask.overlap(slopes.mask, offset)
        return False


    def collision_movement(self):
        player = self.player.sprite
        player.x = player.rect.x
        player.x += player.movement[0]
        player.rect.x = int(player.x)
        self.collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.movement[0] > 0:
                    player.rect.right = tile.rect.left
                    self.collision_types['right'] = True
                if player.movement[0] < 0:
                    player.rect.left = tile.rect.right
                    self.collision_types['left'] = True
        for slopes in self.slopesgroup.sprites():
            TOP, WALKABLE = 0, 1
            slope_type = TOP
            if slopes.rect.colliderect(player.rect):
                if pygame.sprite.collide_mask(player, slopes):
                    if slopes.rect.top < player.rect.top and slope_type == TOP:
                        player.rect.top = slopes.rect.bottom
                        self.player_on_slope = True
                        player.vertical_momentum = 0
                    elif player.rect.bottom > slopes.rect.top > player.rect.top and self.player_on_slope == False:
                        player.rect.bottom = slopes.rect.top
                        self.player_on_slope = True
                    elif player.rect.left < slopes.rect.right < player.rect.right and self.player_on_slope == True:
                        player.rect.bottomleft = slopes.rect.topright
                        self.player_on_slope = False
                    elif player.rect.bottomright == slopes.rect.midleft and self.player_on_slope == True:
                        player.rect.bottomright = slopes.rect.topleft
                        self.player_on_slope = False
            else:
                self.player_on_slope = False




        for coin in self.coin.sprites():
            if coin.rect.colliderect(player.rect):
                self.coin.remove(coin)

        for death in self.Death.sprites():
            if death.rect.colliderect(player.rect):
                self.player = pygame.sprite.GroupSingle().empty()
                self.tiles = pygame.sprite.Group().empty()
                self.bg_objects = pygame.sprite.Group().empty()
                self.coin = pygame.sprite.Group().empty()
                self.Death = pygame.sprite.Group().empty()
                self.slopesgroup = pygame.sprite.Group().empty()

                self.player = pygame.sprite.GroupSingle()
                self.tiles = pygame.sprite.Group()
                self.bg_objects = pygame.sprite.Group()
                self.coin = pygame.sprite.Group()
                self.Death = pygame.sprite.Group()
                self.slopesgroup = pygame.sprite.Group()

                self.terrain_sprites = self.create_sprite(self.terrain_layout, 'Grass')
                self.slope_sprites = self.create_sprite(self.slope_layout, 'Slopes')
                self.create_sprite(self.Gold, 'Gold')
                self.create_sprite(self.trees, 'Trees')
                self.create_sprite(self.spawn, 'Spawn')
                self.create_sprite(self.death, 'Death')

        player.y = player.rect.y
        player.y += player.movement[1]
        player.rect.y = int(player.y)
        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.movement[1] > 0:
                    player.rect.bottom = tile.rect.top
                    self.collision_types['bottom'] = True
                if player.movement[1] < 0:
                    player.rect.top = tile.rect.bottom
                    self.collision_types['top'] = True

        for coin in self.coin.sprites():
            if coin.rect.colliderect(player.rect):
                self.coin.remove(coin)
        if self.collision_types['bottom']:
            player.collide_bottom = True
            player.air_timer = 0
            player.vertical_momentum = 0
        else:
            player.collide_bottom = False
            player.air_timer += 1

        if self.collision_types['top']:
            player.vertical_momentum = 0

    def button_held(self):
        player = self.player.sprite
        player.jump_held = True

    def button_released(self):
        player = self.player.sprite
        player.jump_held = False

    def draw_bg(self):

        bg_images = []
        for i in range(1, 6):
            for image in ['data/graphics/bg_images/plx-1.png', 'data/graphics/bg_images/plx-2.png',
                          'data/graphics/bg_images/plx-3.png', 'data/graphics/bg_images/plx-4.png',
                          'data/graphics/bg_images/plx-5.png']:
                bg_image = pygame.image.load(image).convert_alpha()
                bg_imagenew = pygame.transform.scale(bg_image, (rescaled_width, rescaled_height))
                bg_images.append(bg_imagenew)
        bg_width = bg_images[0].get_width()
        for x in range(5):
            bg_speed = 1
            for i in bg_images:
                self.surface.blit(i, ((x * bg_width) - 1.2 * bg_speed, 0))
                bg_speed += 0.2

    def run(self):
        # tiles
        self.scrolling()
        #background drawing
        self.tiles.update(self.scroll)
        self.tiles.draw(self.surface)
        self.slopesgroup.update(self.scroll)
        self.slopesgroup.draw(self.surface)

        self.bg_objects.update(self.scroll)
        self.bg_objects.draw(self.surface)

        self.coin.update(self.scroll)
        self.coin.draw(self.surface)

        self.Death.update(self.scroll)

        # player
        player = self.player.sprite

        self.player.update(self.scroll)
        self.player.draw(self.surface)
        self.collision_movement()





 #       collision_types_backup = self.collision_types
  #      intersection_point = self.check_slope_collision()
      #  print(intersection_point)
    #    if intersection_point:
   #        self.collision_types = collision_types_backup
