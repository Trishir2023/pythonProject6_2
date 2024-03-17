import random
import math
import os
from PIL import Image, ImageDraw
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
    'dead': (255, 255, 255),  # white
    'alive': (0, 0, 0),  # black
    'resurrected': (255, 0, 0)  # red
}


class HexGridHelper:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def get_neighbors(self, row, col):
        """Get the neighbors of a cell in a hexagonal grid."""
        directions = [(0, -1), (0, 1), (-1, -1), (-1, 0), (1, -1), (1, 0)]
        neighbors = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols:
                neighbors.append((r, c))
        return neighbors

    def get_random_cell(self):
        """Get a random cell in the grid."""
        return random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)

    def is_within_grid(self, row, col):
        """Check if the given cell is within the grid."""
        return 0 <= row < self.rows and 0 <= col < self.cols


def generate_initial_grid(rows, cols):
    """Generate initial grid with random alive and dead cells."""
    grid = [[random.choice([True, False]) for _ in range(cols)] for _ in range(rows)]
    return grid


def draw_grid(image, grid):
    """Draw the grid using PIL."""
    draw = ImageDraw.Draw(image)
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            color = COLORS['alive'] if grid[row][col] else COLORS['dead']
            hexagon_vertices = HexGeometry.hexagon(row, col, CELL_RADIUS)
            draw.polygon(hexagon_vertices, fill=color)

def create_gif():
    images = []
    for i in range(1, GENERATIONS + 1):
        image_path = f"generation_{i}.png"
        if os.path.exists(image_path):
            images.append(imageio.imread(image_path))
            #os.remove(image_path)  # Remove the image file after adding it to the GIF
    imageio.mimsave("game_of_life.gif", images, duration=3)  # Duration is in seconds

def save_image(image, generation):
    """Save the image of the grid."""
    image.save(f"generation_{generation}.png")


def apply_rules(grid, neighbors):
    """Apply modified Game of Life rules to the grid."""
    new_grid = [[False] * COLS for _ in range(ROWS)]
    #last_death_2 = [[0] * COLS for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            sum = 0
            for i in neighbors:
                x = i[0]
                y = i[1]
                sum += grid[x][y]
            live_neighbors = sum
            if grid[row][col]:  # Cell is alive
                if live_neighbors < 2 or live_neighbors > 3:
                    new_grid[row][col] = False  # Dies by underpopulation or overpopulation
                else:
                    new_grid[row][col] = True  # Survives
            else:  # Cell is dead
                if live_neighbors == 3:
                    new_grid[row][col] = True  # Born by reproduction
    return new_grid

def resurrect_dead_cells(grid, generation):
    """Resurrect dead cells every 6 generations."""
    if generation % RESURRECT_AFTER == 0:
        for row in range(ROWS):
            for col in range(COLS):
                if not grid[row][col]:
                    grid[row][col] = True



def bring_random_cells_to_life(grid, generation):
    grid_helper = HexGridHelper(ROWS, COLS)
    """Bring random dead cells to life every 4 generations."""
    if generation % RANDOM_LIFE_AFTER == 0:
        row, col = grid_helper.get_random_cell()
        if not grid[row][col]:
            grid[row][col] = True


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

        return [(c + c_hex, r + r_hex) for (c_hex, r_hex) in hexagon]

    @staticmethod
    def cell_height(radius):
        """Get the height of a hexagon cell."""
        return 1.5 * radius

    @staticmethod
    def cell_width(radius):
        """Get the width of a hexagon cell."""
        return math.sqrt(3) * radius


def main():
    """Main function to run the Game of Life simulation."""
    # Initialize HexGridHelper
    grid_helper = HexGridHelper(ROWS, COLS)

    # Generate initial grid
    grid = generate_initial_grid(ROWS, COLS)

    # Create an image
    image = Image.new("RGB", (COLS * CELL_RADIUS * 2, ROWS * int(1.5 * CELL_RADIUS)), COLORS['dead'])

    # Main simulation loop
    for generation in range(1, GENERATIONS + 1):
        # Get neighbors for each cell
        neighbors = [[[grid_helper.get_neighbors(row, col) for col in range(COLS)] for row in range(ROWS)] for _ in
                     range(COLS)]

        # Apply rules to update the grid
        grid = apply_rules(grid, neighbors)

        # Resurrect dead cells every 6 generations
        resurrect_dead_cells(grid, generation)

        # Bring random dead cells to life every 4 generations
        bring_random_cells_to_life(grid, generation)

        # Draw the grid on the image
        draw_grid(image, grid)

        # Save the image for the current generation
        save_image(image, generation)

    create_gif()


if __name__ == "__main__":
    main()
