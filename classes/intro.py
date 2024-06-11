import pygame

from config import WINDOW_SIZE, display

def play_intro():
    """
    Plays the introduction sequence of the game.

    This function hides the mouse cursor, loads and displays the intro with the iconic "Jeff Jump" sound in the background!
    """
    pygame.mouse.set_visible(0)
    pro_max = pygame.image.load("./content/images/pro_max_plus.png").convert_alpha()
    pro_max_rect = pro_max.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2))
    
    pygame.mixer.music.load("./content/sounds/effects/intro.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=0) 
    timer = 4000
    start_time = pygame.time.get_ticks()

    running = True
    while running and timer > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display.fill((0, 0, 0))
        display.blit(pro_max, pro_max_rect)

        timer = max(0, 4000 - (pygame.time.get_ticks() - start_time))
        pygame.display.flip()

    pygame.mouse.set_visible(True)
