import math
import random
import imageio
from PIL import Image, ImageDraw

# Constants
ROWS = 20
COLS = 20
CELL_RADIUS = 20
GENERATIONS = 30
RESURRECT_AFTER = 6
RANDOM_LIFE_AFTER = 4

# Colors
COLORS = {
    'dead': (255, 255, 255),    # white
    'alive': (0, 0, 0),        # black
    'resurrected': (255, 0, 0) # red
}

class HexGridHelper:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def get_neighbors(self, row, col):
        """Get the neighbors of a cell."""
        directions = [(0, -1), (0, 1), (-1, -1), (-1, 0), (1, -1), (1, 0)]
        neighbors = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbors.append((nr, nc))
        return neighbors

class HexGeometry:
    @staticmethod
    def hexagon(row, col, radius):
        """Generate hexagon vertices."""
        root = math.sqrt(3)
        hexagon = [
            (0, 0),
            (0, radius),
            (0.5 * root * radius, 1.5 * radius),
            (root * radius, radius),
            (root * radius, 0),
            (0.5 * root * radius, -0.5 * radius)
        ]
        odd_even_offset = -0.5 * (row % 2) * HexGeometry.cell_width(radius)
        r = row * HexGeometry.cell_height(radius)
        c = col * HexGeometry.cell_width(radius) + odd_even_offset

        return [(c + c_hex, r + r_hex) for c_hex, r_hex in hexagon]

    @staticmethod
    def cell_height(radius):
        """Get the height of a hexagon cell."""
        return 1.5 * radius

    @staticmethod
    def cell_width(radius):
        """Get the width of a hexagon cell."""
        return math.sqrt(3) * radius

def get_initial_grid():
    """Initialize the grid with random cell states."""
    return [[random.choice([True, False]) for _ in range(COLS)] for _ in range(ROWS)]

def apply_rules(grid, neighbors):
    """Apply modified Game of Life rules to the grid."""
    new_grid = [[False] * COLS for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            alive_neighbors = sum(grid[nr][nc] for nr, nc in neighbors[row][col])
            if grid[row][col]:
                # Cell is alive
                if alive_neighbors < RESURRECT_AFTER:
                    new_grid[row][col] = False  # Die due to underpopulation
                else:
                    new_grid[row][col] = True   # Survive
            else:
                # Cell is dead
                if alive_neighbors >= RANDOM_LIFE_AFTER:
                    new_grid[row][col] = True   # Resurrect
    return new_grid

def visualize_grid(grid):
    """Create an image representation of the grid."""
    img_width = int(1.5 * COLS * CELL_RADIUS)
    img_height = int(1.5 * ROWS * CELL_RADIUS)
    img = Image.new("RGB", (img_width, img_height), COLORS['dead'])
    draw = ImageDraw.Draw(img)

    hex_helper = HexGridHelper(ROWS, COLS)
    for row in range(ROWS):
        for col in range(COLS):
            hex_vertices = HexGeometry.hexagon(row, col, CELL_RADIUS)
            cell_color = COLORS['alive'] if grid[row][col] else COLORS['dead']
            draw.polygon(hex_vertices, fill=cell_color)

    return img

def main():
    grid = get_initial_grid()
    hex_helper = HexGridHelper(ROWS, COLS)
    images = []  # Collect images for GIF

    for generation in range(GENERATIONS):
        neighbors = [[hex_helper.get_neighbors(row, col) for col in range(COLS)] for row in range(ROWS)]
        grid = apply_rules(grid, neighbors)
        img = visualize_grid(grid)
        images.append(img)

    # Save as GIF
    imageio.mimsave("hexagonal_automaton.gif", images, duration=0.5)  # Adjust duration as needed

if __name__ == "__main__":
    main()
