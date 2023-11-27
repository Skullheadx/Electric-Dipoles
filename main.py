from setup import *
from particle import PointParticle

is_running = True
clock = pygame.Clock()
delta = 0

particles = [PointParticle((SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2), 1.6e-19),
             PointParticle((SCREEN_WIDTH * 2 / 3, SCREEN_HEIGHT / 2), -1.6e-19)]

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    for particle in particles:
        particle.update(delta, particles)

    screen.fill((255, 255, 255))
    for particle in particles:
        particle.draw_field_lines(screen)
    for particle in particles:
        particle.draw(screen)

    pygame.display.flip()
    delta = clock.tick(60)
