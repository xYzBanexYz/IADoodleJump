import random
import pygame

from config import config, quitGame
from classes.intro import play_intro
from classes.menu import Menu
from classes.Jeff import JeffGame

WINDOW_SIZE = (480,720)
cfg = config(*WINDOW_SIZE)

def main():
  play_intro(cfg.w, cfg.h, cfg.display)

  menu = Menu(WINDOW_SIZE,cfg.display, cfg.clock)
  while not menu.start:
    menu.update()

  menu.reset()
  del menu 

  game = JeffGame(WINDOW_SIZE, cfg.display, cfg.clock)

  while not game.restart:
    if game.pause:
      pass
    else:
      game.play_step()

  return "continue"

if __name__ == '__main__':

  msg = "continue"
  while msg == "continue":
    msg = main()
  
  quitGame()  