import math
import random

class HexGridHelper:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def get_neighbors(self, row, col):
        """Get the neighbors of a cell."""
        neighbors = []
        directions = [(0, -1), (0, 1), (-1, -1), (-1, 0), (1, -1), (1, 0)]
        for (dr, dc) in directions:
            (r, c) = (row + dr, col + dc)
            if 0 <= r < self.rows and 0 <= c < self.cols:
                neighbors.append((r, c))
        return neighbors

    def get_random_cell(self):
        """Get a random cell in the grid."""
        return random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)

    def is_within_grid(self, row, col):
        """Check if the given cell is within the grid."""
        return 0 <= row < self.rows and 0 <= col < self.cols

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
