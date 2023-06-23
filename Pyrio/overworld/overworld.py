import pygame
from game_data import levels



class Node(pygame.sprite.Sprite):
    def __init__(self, position, status, player_speed):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        if status == 'unlocked':
            self.image.fill('red')
        else:
            self.image.fill('grey')
        self.rect = self.image.get_rect(center=position)

        self.detection_zone = pygame.Rect(self.rect.centerx - (player_speed / 2),
                                          self.rect.centery - (player_speed / 2), player_speed, player_speed)


class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = position
        self.image = pygame.Surface((20, 20))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.center = self.position


class Overworld:
    def __init__(self, start_level, max_level, surface, create_level):
        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        # movement logic
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.moving = False

        # sprites
        self.setup_nodes()
        self.setup_player()

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for idx, node_item in enumerate(levels.values()):
            if idx <= self.max_level:
                node_sprite = Node(node_item['node_pos'], 'unlocked', self.speed)
            else:
                node_sprite = Node(node_item['node_pos'], 'locked', self.speed)
            self.nodes.add(node_sprite)

    def draw_paths(self):
        points = [node_item['node_pos'] for idx, node_item in enumerate(levels.values()) if idx <= self.max_level]
        pygame.draw.lines(self.display_surface, 'red', False, points, 6)

    def setup_player(self):
        self.player = pygame.sprite.GroupSingle()
        player_sprite = Player(self.nodes.sprites()[self.current_level].rect.center)
        self.player.add(player_sprite)

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.moving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target is 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    def update_player_postion(self):
        # self.player.sprite.rect.center = self.nodes.sprites()[self.current_level].rect.center
        if self.moving and self.move_direction:
            self.player.sprite.position += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.player.sprite.position):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def run(self):
        self.input()
        self.update_player_postion()
        self.player.update()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.player.draw(self.display_surface)
