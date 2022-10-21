import pygame
from tiles import Tile
from player import Player
from settings import tile_size


class Level:
    def __init__(self, level_data, surface):
        # level setup
        self.display_surface = surface
        self.level_setup(level_data)
        self.world_shift = 0

    def level_setup(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_idx, row in enumerate(layout):
            for col_idx, col in enumerate(row):
                x = col_idx * tile_size
                y = row_idx * tile_size
                if col == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if col == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def run(self):
        # level tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        # player
        self.player.update()
        self.player.draw(self.display_surface)
