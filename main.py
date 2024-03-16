#!/usr/bin/env python3
"""
Main file
"""
from cube import Cube
from solver import solve


def main() -> None:
    """main function"""
    cube = Cube()
    cube.mix()
    solve(cube)


if __name__ == "__main__":
    main()
