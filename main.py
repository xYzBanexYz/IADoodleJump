import pygame

from config import quitGame
from classes.intro import play_intro
from classes.menu import Menu
from classes.Jeff import JeffGame
from classes.PauseMenu import PauseMenu

import pygame

def main():
  """
  The main function of the game.
  
  This function controls the flow of the game. It initializes the menu, game, and pause menu objects,
  and enters a loop that continues until the game restarts. Within the loop, it checks if the game is
  paused or if the menu is active, and updates the corresponding objects accordingly. If neither the
  game is paused nor the menu is active, it hides the mouse cursor and advances the game by one step.
  
  Returns:
    str: The string "continue" indicating that the game should continue running or not.
  """
  
  play_intro()

  menu = Menu()
  game = JeffGame()
  pauseMenu = PauseMenu()

  while not game.restart:

    if game.pause:
      pygame.mouse.set_visible(1)
      answer = pauseMenu.update()
      match answer:
        case "play":
          game.pause = False
        case "restart":
          game.restart()
        case "menu":
          game.pause = False
          game.menu = True

    elif game.menu:
      pygame.mouse.set_visible(1)
      answer = menu.update()
      match answer:
        case "play":
          game.restartGame()
          game.menu = False
        case "exit":
          quitGame()
          pass
    else:
      pygame.mouse.set_visible(0)
      game.play_step()

  return "continue"


if __name__ == '__main__':

  msg = "continue"
  while msg == "continue":
    msg = main()
  
  quitGame()  