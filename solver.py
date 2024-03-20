"""
This module is for automatic solving of the cube
"""

from cube import Cube, Tile


def solve(cube: Cube):
    """This function solves a rubik's cube"""
    print(cube)
    print(cube.layout["left"].get_piece(cube.layout["left"].index(Tile.WHITE)))
