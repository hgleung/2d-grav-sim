import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
FPS = 60
GRAVITY = 0.5
BOUNCE_FACTOR = 0.7
INITIAL_VELOCITY = 3  # Initial horizontal velocity

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Gravity Simulator")
clock = pygame.time.Clock()

class Circle:
    def __init__(self, x, y, radius, is_static=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.is_static = is_static
        self.velocity_y = 0
        self.velocity_x = 0

    def update(self, outer_circle=None):
        if self.is_static:
            return

        # Apply gravity
        self.velocity_y += GRAVITY

        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y

        if outer_circle:
            # Check collision with outer circle
            dx = self.x - outer_circle.x
            dy = self.y - outer_circle.y
            distance = math.sqrt(dx * dx + dy * dy)
            
            # If collision with outer circle
            if distance + self.radius > outer_circle.radius - 1:
                # Calculate collision normal
                nx = dx / distance
                ny = dy / distance
                
                # Position correction
                overlap = (distance + self.radius) - (outer_circle.radius - 1)
                self.x -= overlap * nx
                self.y -= overlap * ny
                
                # Velocity reflection
                dot_product = (self.velocity_x * nx + self.velocity_y * ny)
                self.velocity_x = BOUNCE_FACTOR * (-2 * dot_product * nx + self.velocity_x)
                self.velocity_y = BOUNCE_FACTOR * (-2 * dot_product * ny + self.velocity_y)

    def draw(self, screen):
        pygame.draw.circle(screen, RED if not self.is_static else WHITE, 
                         (int(self.x), int(self.y)), self.radius, 
                         1 if self.is_static else 0)

def main():
    # Create circles
    outer_circle = Circle(WIDTH // 2, HEIGHT // 2, 200, is_static=True)
    
    def reset_inner_circle():
        # Random offset from center (-150 to 150 pixels)
        x_offset = random.randint(-150, 150)
        # Create inner circle with random x position
        inner = Circle(WIDTH // 2 + x_offset, HEIGHT // 2 - 100, 20)
        # Add initial horizontal velocity in opposite direction of offset
        inner.velocity_x = -math.copysign(INITIAL_VELOCITY, x_offset)
        return inner

    inner_circle = reset_inner_circle()

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    inner_circle = reset_inner_circle()

        # Update
        inner_circle.update(outer_circle)

        # Draw
        screen.fill(BLACK)
        outer_circle.draw(screen)
        inner_circle.draw(screen)
        pygame.display.flip()

        # Cap the framerate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
