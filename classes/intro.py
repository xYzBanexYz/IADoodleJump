import pygame

def play_intro(w,h, display):
    # pygame.mouse.set_visible(False)
    pro_max = pygame.image.load("./content/images/pro_max_plus.png").convert_alpha()
    pro_max_rect = pro_max.get_rect(center=(w//2, h//2))
    
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