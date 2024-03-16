#!/usr/bin/env python3
"""
Main file
"""
from cube import Cube


def main() -> None:
    """main function"""
    cube = Cube()
    cube.mix()
    print(cube)


if __name__ == "__main__":
    main()
