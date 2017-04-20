import pygame

pygame.init()
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

size = [400,400]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Woot!")
screen.fill(WHITE)

pygame.draw.line(screen, GREEN, [0, 0], [50,30], 5)
pygame.draw.aaline(screen, GREEN, [0, 50],[50, 80], True)   
pygame.draw.ellipse(screen, RED, [225, 10, 50, 20], 2)
pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)
pygame.draw.circle(screen, BLUE, [60, 250], 40)

pygame.display.update() 
