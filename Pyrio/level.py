import pygame
from settings import screen_height, screen_width
from game_data import levels


class Level:
    def __init__(self, current_level, surface, back_to_overworld):
        # level setup
        self.display_surface = surface
        self.current_level = current_level
        level_data = levels[current_level]
        level_content = level_data['content']
        self.new_max_level = level_data['unlock']
        self.back_to_overworld = back_to_overworld

        # level display
        self.font = pygame.font.Font(None, 40)
        self.text_surf = self.font.render(level_content, True, 'red')
        self.text_rect = self.text_surf.get_rect(center=(screen_width / 2, screen_height / 2))

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.back_to_overworld(self.current_level, self.new_max_level)
        if keys[pygame.K_ESCAPE]:
            self.back_to_overworld(self.current_level, 0)

    def run(self):
        self.input()
        self.display_surface.blit(self.text_surf, self.text_rect)
