import random

import pygame
import math

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 4
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE

# Particle Types
EMPTY = 0
SAND = 1

# Colors
EMPTY_COLOR = (0, 0, 0)
RAINBOW_COLORS = [#rainbow colors
    (255, 0, 0),      # Red
    (255, 127, 0),    # Orange
    (255, 255, 0),    # Yellow
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (75, 0, 130),     # Indigo
    (148, 0, 211)     # Violet
]



def interpolate_color(t, index):

    return (
        int(RAINBOW_COLORS[index % 6][0] * (1 - t) + RAINBOW_COLORS[(index + 1) % 6][0] * t),
        int(RAINBOW_COLORS[index % 6][1] * (1 - t) + RAINBOW_COLORS[(index + 1) % 6][1] * t),
        int(RAINBOW_COLORS[index % 6][2] * (1 - t) + RAINBOW_COLORS[(index + 1) % 6][2] * t)
    )

def update_grid():
    for y in range(GRID_HEIGHT - 1, -1, -1):
        for x in range(GRID_WIDTH):
            if grid[y][x][0] == SAND:
                if y + 1 < GRID_HEIGHT and grid[y + 1][x][0] == EMPTY:
                    grid[y + 1][x] = grid[y][x]
                    grid[y][x] = (EMPTY, EMPTY_COLOR)
                elif (y + 1 < GRID_HEIGHT and x - 1 >= 0 and grid[y + 1][x - 1][0] == EMPTY):
                    grid[y + 1][x - 1] = grid[y][x]
                    grid[y][x] = (EMPTY, EMPTY_COLOR)
                elif (y + 1 < GRID_HEIGHT and x + 1 < GRID_WIDTH and grid[y + 1][x + 1][0] == EMPTY):
                    grid[y + 1][x + 1] = grid[y][x]
                    grid[y][x] = (EMPTY, EMPTY_COLOR)

def draw_grid(screen, t):
    """Draw the grid with colors interpolated between START_COLOR and END_COLOR."""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x][0] == SAND:
                # Use the stored color for sand particles
                color = grid[y][x][1]
            else:
                # Draw empty cells with the background color
                color = EMPTY_COLOR
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    running = True
    mouse_held = False
    t = 0.0  # Time variable for interpolation
    index = 0

    # Initialize grid with empty cells
    global grid
    grid = [[(EMPTY, EMPTY_COLOR) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_held = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

        if mouse_held:
            mx, my = pygame.mouse.get_pos()
            mx //= GRID_SIZE
            my //= GRID_SIZE
            matrix = 7
            extent = math.floor(matrix/2)
            t += 0.01
            if t > 1.0:
                if index == 5:
                    index = 0
                else:
                    index += 1
                t = 0.0
            for i in range(-extent, extent):
                for j in range(-extent, extent):
                    if (0 <= (mx + i) < GRID_WIDTH-i and 0 <= (my + j) < GRID_HEIGHT-j) and (0 <= (mx + i) < GRID_WIDTH+i and 0 <= (my + j) < GRID_HEIGHT+j):
                        if random.random() > 0.75:
                            color = interpolate_color(t, index)
                            grid[my+j][mx+i] = (SAND, color)

        update_grid()

        # Update the interpolation factor


        screen.fill(EMPTY_COLOR)  # Fill the screen with black before drawing the grid
        draw_grid(screen, t)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()