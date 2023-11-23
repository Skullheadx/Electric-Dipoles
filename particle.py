import pygame


class PointParticle:

    def __init__(self, position, charge=1.6e-19):
        self.position = pygame.Vector2(position)
        self.mouse_offset = pygame.Vector2(0, 0)
        self.charge = charge
        self.radius = 50
        self.dragging = False
        self.colour = (255, 0, 0) if self.charge < 0 else (0, 0, 255)

    def update(self, delta):
        if pygame.mouse.get_pressed(3)[0]:
            if not self.dragging and self.position.distance_to(pygame.mouse.get_pos()) < self.radius:
                self.mouse_offset = pygame.Vector2(pygame.mouse.get_pos()) - self.position
                self.dragging = True
            if self.dragging:
                self.position = pygame.Vector2(pygame.mouse.get_pos()) - self.mouse_offset
        elif self.dragging:
            self.dragging = False

    def draw(self, surf):
        pygame.draw.circle(surf, self.colour, self.position, self.radius)
        pygame.draw.circle(surf, (0, 0, 0), self.position, self.radius, 3)
