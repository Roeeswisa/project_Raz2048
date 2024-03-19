import random
import pygame
 
pygame.init()


WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Roee Swisa: 2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold', 24)
run = True