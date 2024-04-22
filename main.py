import random
import pygame
from doodle import DoodleGame

# TODO Gestion des menus / Jeu principal / Mode avec IA

if __name__ == '__main__':

  game = DoodleGame()
  while True:
    game.play_step()