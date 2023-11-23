import pygame

from particle import PointParticle

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Electric Dipoles")

is_running = True
clock = pygame.Clock()
delta = 0

particles = [PointParticle((SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))]

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    for particle in particles:
        particle.update(delta)

    screen.fill((255, 255, 255))
    for particle in particles:
        particle.draw(screen)

    pygame.display.flip()
    delta = clock.tick()
