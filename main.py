import random
import pygame

from config import config, quitGame
from classes.intro import play_intro
from classes.menu import Menu
from classes.Jeff import JeffGame
from classes.PauseMenu import PauseMenu

WINDOW_SIZE = (480,720)
cfg = config(*WINDOW_SIZE)

def main():
  play_intro(cfg.w, cfg.h, cfg.display)

  menu = Menu(WINDOW_SIZE,cfg.display, cfg.clock)

  while not menu.start:
    menu.update()

  del menu

  game = JeffGame(WINDOW_SIZE, cfg.display, cfg.clock)
  pauseMenu = PauseMenu(WINDOW_SIZE, cfg.display, cfg.clock)

  while not game.restart:
    if game.pause:
      answer = pauseMenu.update()
      match answer:
        case "play":
          game.pause = False
        case "restart":
          # TODO
          pass
        case "":
          pass
    else:
      game.play_step()

  return "continue"

if __name__ == '__main__':

  msg = "continue"
  while msg == "continue":
    msg = main()
  
  quitGame()  