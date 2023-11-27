import math

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Electric Dipoles")


def draw_arrow(surface, color, start_pos, end_pos, width=1, head_length=10, head_angle=math.pi / 4):
    pygame.draw.line(surface, color, start_pos, end_pos, width)
    direction = (end_pos - start_pos).normalize()
    left = direction.rotate(math.degrees(head_angle))
    right = direction.rotate(-math.degrees(head_angle))
    pygame.draw.line(surface, color, end_pos, end_pos + left * head_length, width)
    pygame.draw.line(surface, color, end_pos, end_pos + right * head_length, width)
