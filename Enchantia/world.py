import pygame

import constants
from items import Item
from character import Character


class World:
    def __init__(self):
        self.level_length = None
        self.map_tiles = []
        self.obstacles_tiles = []
        self.exit_tile = None
        self.items_list = []
        self.player = None
        self.character_list = []

    def process_data(self, data, tile_list, items_images_list, master_animation_list):
        self.level_length = len(data)

        # Iterate through each value in the level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * constants.TILE_SIZE
                image_y = y * constants.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                # Save copy of wall tiles into different lists for use in collision detection
                if tile == 7:
                    self.obstacles_tiles.append(tile_data)
                # Save copy of exit tile into a list for use in going to the next level
                elif tile == 8:
                    self.exit_tile = tile_data
                elif tile == 9:
                    # Create a coin object at the tile
                    coin = Item(image_x, image_y, 0, items_images_list[1])
                    self.items_list.append(coin)
                    tile_data[0] = tile_list[0]
                elif tile == 10:
                    # Create a health potion object at the tile
                    potion = Item(image_x, image_y, 1, [items_images_list[0]])
                    self.items_list.append(potion)
                    tile_data[0] = tile_list[0]
                elif tile == 11:
                    # Create a player object at the tile
                    player = Character(
                        image_x, image_y, 100, master_animation_list[0], False, 1, 0
                    )
                    self.player = player
                    tile_data[0] = tile_list[0]
                elif 12 <= tile <= 16:
                    # Create enemies at the tile
                    enemy = Character(
                        image_x,
                        image_y,
                        100,
                        master_animation_list[tile - 11],
                        False,
                        1,
                        tile - 11,
                    )
                    self.character_list.append(enemy)
                    tile_data[0] = tile_list[0]
                elif tile == 17:
                    # Create a boss at the tile
                    boss = Character(
                        image_x, image_y, 200, master_animation_list[6], True, 2, 6
                    )
                    self.character_list.append(boss)
                    tile_data[0] = tile_list[0]

                # Check if the tile is in the main tile list, if so, add image data to the main tile list
                if tile >= 0:
                    self.map_tiles.append(tile_data)

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]  # Update x position
            tile[3] += screen_scroll[1]  # Update y position
            tile[1].center = (tile[2], tile[3])  # Update rect

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])