import pygame
import math


class PointParticle:
    font = pygame.font.SysFont("arial", 75)
    signs = {'+': font.render("+", True, (0, 0, 0)),
             '−': font.render('−', True, (0, 0, 0))}

    BLUE = (0, 153, 255)
    RED = (255, 43, 0)

    radius = 25
    step_amount = 10
    default_num_field_lines = 16

    def __init__(self, position, charge=1.6e-19):
        self.position = pygame.Vector2(position)
        self.mouse_offset = pygame.Vector2(0, 0)
        self.charge = charge
        self.dragging = False
        self.colour = self.RED if self.charge < 0 else self.BLUE
        self.sign = self.signs['−' if self.charge < 0 else '+']

        self.num_field_lines = int(abs(self.charge) / 1.6e-19 * self.default_num_field_lines)
        self.field_line_angles = list(range(0, 360, math.ceil(360 / self.num_field_lines)))  # List of angles
        self.field_lines = [[] for _ in range(self.num_field_lines)]

        self.line_step = pygame.Vector2(self.step_amount, 0) if self.charge > 0 else pygame.Vector2(-self.step_amount, 0)

        # Only if the field lines do not connect to the particle, then they are stored here
        self.extra_field_lines = [[] for _ in range(self.num_field_lines)]

    def update(self, delta, particles):
        if self.dragging or not (True in [p.dragging for p in particles]):
            if pygame.mouse.get_pressed(3)[0]:
                if not self.dragging and self.position.distance_to(pygame.mouse.get_pos()) < self.radius:
                    self.mouse_offset = pygame.Vector2(pygame.mouse.get_pos()) - self.position
                    self.dragging = True
                if self.dragging:
                    self.position = pygame.Vector2(pygame.mouse.get_pos()) - self.mouse_offset
            elif self.dragging:
                self.dragging = False

        for field_line_index, angle in enumerate(self.field_line_angles):
            self.field_lines[field_line_index].clear()
            self.extra_field_lines[field_line_index].clear()
            position = self.position.copy()
            direction = math.radians(angle)
            end = False
            for i in range(1000):
                position += self.line_step.copy().rotate(math.degrees(direction))

                electric_field_x_net = 0
                electric_field_y_net = 0
                for particle in particles:
                    diff = position - particle.position
                    if diff.length() < particle.radius and particle is not self:
                        end = True
                        break
                    if particle is self and diff.length() == 0:
                        continue
                    angle = math.atan2(diff.y, diff.x)  # radians
                    electric_field = 8.99e9 * particle.charge / pow(diff.length(), 2)
                    electric_field_x_net += electric_field * math.cos(angle)
                    electric_field_y_net += electric_field * math.sin(angle)

                direction = math.atan2(electric_field_y_net, electric_field_x_net)
                self.field_lines[field_line_index].append(position.copy())
                if math.hypot(electric_field_x_net, electric_field_y_net) > 1.5e-11 or (i==1000-1 and self.charge < 0):
                    self.extra_field_lines[field_line_index] = self.field_lines[field_line_index].copy()
                    end = True
                    break

                if end:
                    break
    def draw_field_lines(self, surf):
        if self.charge > 0:
            for line in self.field_lines:
                if len(line) > 1:
                    pygame.draw.lines(surf, self.colour, False, line, 5)
        else:
            for line in self.extra_field_lines:
                if len(line) > 1:
                    pygame.draw.lines(surf, self.colour, False, line, 5)
    def draw(self, surf):
        pygame.draw.circle(surf, self.colour, self.position, self.radius)
        pygame.draw.circle(surf, (0, 0, 0), self.position, self.radius, 3)
        surf.blit(self.sign, self.sign.get_rect(center=self.position))
