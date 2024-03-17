import random
#import time
import os
from PIL import Image, ImageDraw
from helper import HexGridHelper, HexGeometry
import imageio

# Constants
ROWS = 20
COLS = 20
CELL_RADIUS = 20
GENERATIONS = 30
RESURRECT_AFTER = 6
RANDOM_LIFE_AFTER = 4

# Colors
COLORS = {
    'dead': (255, 255, 255),   # white
    'alive': (0, 0, 0),        # black
    'resurrected': (255, 0, 0) # red
}

# Game of Life rules
def apply_rules(grid, neighbors, generation):
    new_grid = [[False] * COLS for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            live_neighbors = sum(grid[n_row][n_col] for n_row, n_col in neighbors[row][col])
            if grid[row][col]:  # Cell is alive
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[row][col] = False  # Dies by underpopulation or overpopulation
                else:
                    new_grid[row][col] = True  # Survives
            else:  # Cell is dead
                if live_neighbors == 3:
                    new_grid[row][col] = True  # Born by reproduction
                elif generation % RESURRECT_AFTER == 0:
                    new_grid[row][col] = True  # Resurrected
    return new_grid

def get_initial_grid():
    return [[random.choice([True, False]) for _ in range(COLS)] for _ in range(ROWS)]

def draw_grid(image, grid):
    draw = ImageDraw.Draw(image)
    for row in range(ROWS):
        for col in range(COLS):
            color = COLORS['alive'] if grid[row][col] else COLORS['dead']
            hexagon_vertices = HexGeometry.hexagon(row, col, CELL_RADIUS)
            draw.polygon(hexagon_vertices, fill=color, outline=(0, 0, 0))

def save_image(image, generation):
    image.save(f"generation_{generation}.png")

def create_gif():
    images = []
    for i in range(1, GENERATIONS + 1):
        image_path = f"generation_{i}.png"
        if os.path.exists(image_path):
            images.append(imageio.imread(image_path))
            #os.remove(image_path)  # Remove the image file after adding it to the GIF
    imageio.mimsave("game_of_life.gif", images, duration=3)  # Duration is in seconds

def main():
    grid_helper = HexGridHelper(ROWS, COLS)
    grid = get_initial_grid()
    image = Image.new("RGB", (COLS * CELL_RADIUS * 2, ROWS * int(1.5 * CELL_RADIUS)), COLORS['dead'])
    for generation in range(1, GENERATIONS + 1):
        neighbors = [[grid_helper.get_neighbors(row, col) for col in range(COLS)] for row in range(ROWS)]
        grid = apply_rules(grid, neighbors, generation)
        if generation % RANDOM_LIFE_AFTER == 0:
            x = random.choice(range(ROWS))
            y = random.choice(range(COLS))
            if not grid[x][y]:
                grid[x][y] = True
        draw_grid(image, grid)
        save_image(image, generation)
    create_gif()

if __name__ == "__main__":
    main()
