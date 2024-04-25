import random
import pygame
from doodle import DoodleGame

# TODO Gestion des menus / Jeu principal / Mode avec IA

if __name__ == '__main__':

  game = DoodleGame()

  while game.run:
    if game.get_menu():
      game.play_menu()
      game.musicMenu()

    elif game.get_play():
      game.play_step()
    
    elif game.get_game_over():
      game.gameover()