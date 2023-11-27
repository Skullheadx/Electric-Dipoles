from setup import *


class PointParticle:
    font = pygame.font.SysFont("arial", 75)
    signs = {'+': font.render("+", True, (0, 0, 0)),
             '−': font.render('−', True, (0, 0, 0))}

    BLUE = (0, 153, 255)
    RED = (255, 43, 0)

    field_line_colour = (12, 12, 12)

    radius = 25
    step_amount = 5
    default_num_field_lines = 64
    screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

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

        self.line_step = pygame.Vector2(self.step_amount, 0) if self.charge > 0 else pygame.Vector2(-self.step_amount,
                                                                                                    0)

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

        if self.position.x + self.radius > SCREEN_WIDTH:
            self.position.x = SCREEN_WIDTH - self.radius
        elif self.position.x - self.radius < 0:
            self.position.x = self.radius

        if self.position.y + self.radius > SCREEN_HEIGHT:
            self.position.y = SCREEN_HEIGHT - self.radius
        elif self.position.y - self.radius < 0:
            self.position.y = self.radius

        for particle in particles:
            if particle is self:
                continue
            if self.position.distance_to(particle.position) < self.radius + particle.radius:
                midpoint = (self.position + particle.position) / 2
                diff = self.position - particle.position
                self.position = midpoint + diff.normalize() * (self.radius + particle.radius) / 2
                particle.position = midpoint - diff.normalize() * (self.radius + particle.radius) / 2

        for field_line_index, angle in enumerate(self.field_line_angles):
            self.field_lines[field_line_index].clear()
            position = self.position.copy()
            direction = math.radians(angle)
            end = False
            for i in range(2000):
                position += self.line_step.copy().rotate(math.degrees(direction))

                electric_field_x_net = 0
                electric_field_y_net = 0
                for particle in particles:
                    diff = position - particle.position
                    if diff.length() < particle.radius and particle is not self:
                        end = True
                        if self.charge < 0:
                            end2 = True
                            for pt in self.field_lines[field_line_index]:
                                if not self.screen_rect.collidepoint(pt):
                                    end2 = False
                            if end2:
                                self.field_lines[field_line_index].clear()
                        break
                    if particle is self and diff.length() == 0:
                        continue
                    angle = math.atan2(diff.y, diff.x)  # radians
                    electric_field = 8.99e9 * particle.charge / pow(diff.length(), 2)
                    electric_field_x_net += electric_field * math.cos(angle)
                    electric_field_y_net += electric_field * math.sin(angle)

                direction = math.atan2(electric_field_y_net, electric_field_x_net)
                self.field_lines[field_line_index].append(position.copy())
                if not self.screen_rect.collidepoint(position):
                    end = True

                if end:
                    break

    def draw_field_lines(self, surf):
        for line in self.field_lines:
            if len(line) > 1:
                pygame.draw.lines(surf, self.field_line_colour, False, line, 3)

    def draw(self, surf):
        pygame.draw.circle(surf, self.colour, self.position, self.radius)
        pygame.draw.circle(surf, (0, 0, 0), self.position, self.radius, 3)
        surf.blit(self.sign, self.sign.get_rect(center=self.position))
