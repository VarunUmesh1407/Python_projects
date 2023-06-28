from os import walk
import pygame


def import_folder(path):
    surface_list = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            img_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(img_surf)
    return surface_list
