"""
Contains the code for the internal workings of the cube
"""
from enum import Enum
from random import choice
from typing import Callable


class Tile(Enum):
    """
    Represents a single tile of the cube
    the value is the ANSI color code for this color
    """
    RED = "\x1b[48;5;196m"
    GREEN = "\x1b[48;5;118m"
    BLUE = "\x1b[48;5;27m"
    YELLOW = "\x1b[48;5;226m"
    WHITE = "\x1b[48;5;255m"
    ORANGE = "\x1b[48;5;208m"
    UNSET = "\x1b[48;5;239m"

    def __repr__(self):
        return f"{self.value}  \x1b[0m"


class Side:
    """One side of the cube"""
    def __init__(self, tile) -> None:
        self.base = tile
        self.tiles: list[list[Tile]] = [[tile] * 3, [tile] * 3, [tile] * 3]

    def __str__(self) -> str:
        """
        Shows this side as a 3x3 grid
        """
        string = ""
        for row in self.tiles:
            for tile in row:
                string += f"{tile.value:>3}  \x1b[0m"
            string += "\n"
        return string[:-1]

    def get_colors(self) -> list[str]:
        """Returns a list of colored spaces to represent its content"""
        return ["  ".join([j.value for j in i]) + "  " for i in self.tiles]

    def set_top_n(self, getter, setter):
        """Set the top neighbour"""
        self.top_g = getter
        self.top_s = setter

    def set_bottom_n(self, getter, setter):
        """Set the bottom neighbour"""
        self.bottom_g = getter
        self.bottom_s = setter

    def set_left_n(self, getter, setter):
        """Set the left neighbour"""
        self.left_g = getter
        self.left_s = setter

    def set_right_n(self, getter, setter):
        """Set the right neighbour"""
        self.right_g = getter
        self.right_s = setter

    def r_left(self):
        """Rotate left by 90°"""
        right = list(self.get_right())
        top = list(self.get_top())
        bottom = list(self.get_bottom())
        self._set_bottom(list(self.get_left()))
        self._set_top(right)
        self._set_right(bottom)
        self._set_left(top)

        left = self.left_g()
        self.left_s(list(self.top_g()))
        self.top_s(list(self.right_g()))
        self.right_s(list(self.bottom_g()))
        self.bottom_s(list(left))

    def r_right(self):
        """Rotate right by 90°"""
        left = list(self.get_left())
        self._set_left(list(self.get_bottom()))
        self._set_bottom(list(self.get_right()))
        self._set_right(list(self.get_top()))
        self._set_top(list(left))

        left = list(self.left_g())
        self.left_s(list(self.bottom_g()))
        self.bottom_s(list(self.right_g()))
        self.right_s(list(self.top_g()))
        self.top_s(left)

    def _set_top(self, insert: list[Tile]):
        """Set the top row of tiles"""
        self.tiles[0] = list(insert)

    def _set_bottom(self, insert: list[Tile]):
        """Set the bottom row of tiles"""
        self.tiles[2] = list(insert[::-1])

    def _set_left(self, insert: list[Tile]):
        """Set the left column of tiles"""
        self.tiles[2][0] = insert[0]
        self.tiles[1][0] = insert[1]
        self.tiles[0][0] = insert[2]

    def _set_right(self, insert: list[Tile]):
        """Set the right column of tiles"""
        self.tiles[0][2] = insert[0]
        self.tiles[1][2] = insert[1]
        self.tiles[2][2] = insert[2]

    def get_top(self) -> list[Tile]:
        """Get the top row of tiles"""
        return list(self.tiles[0])

    def get_bottom(self) -> list[Tile]:
        """Get the bottom row of tiles"""
        return list(self.tiles[2][::-1])

    def get_left(self) -> list[Tile]:
        """Get the left column of tiles"""
        return [i[0] for i in self.tiles[::-1]]

    def get_right(self) -> list[Tile]:
        """Get the right column of tiles"""
        return [i[2] for i in self.tiles]

    def get_gs(self, side: str) -> tuple[Callable, Callable]:
        """Get the getter and setter for the right neighbour"""
        match side:
            case "top":
                return (self.get_top, self._set_top)
            case "left":
                return (self.get_left, self._set_left)
            case "bottom":
                return (self.get_bottom, self._set_bottom)
            case "right":
                return (self.get_right, self._set_right)
            case _:
                exit(1)


class Cube:
    """
    Contains six sides of a cube
    Layout:

          ┌───┐
          │2 G│
      ┌───┼───┼───┐
      │0 O│5 Y│1 R│
      └───┼───┼───┘
          │3 B│
          ├───┤
          │4 W│
          └───┘

    """

    def __init__(self) -> None:
        self.sides = [Side(Tile)] * 6
        self.sides[0] = Side(Tile.ORANGE)
        self.sides[1] = Side(Tile.RED)
        self.sides[2] = Side(Tile.GREEN)
        self.sides[3] = Side(Tile.BLUE)
        self.sides[4] = Side(Tile.WHITE)
        self.sides[5] = Side(Tile.YELLOW)

        self.layout = {
            "left": self.sides[0],
            "right": self.sides[1],
            "back": self.sides[2],
            "front": self.sides[3],
            "down": self.sides[4],
            "up": self.sides[5],
        }

        self.sides[0].set_top_n(*self.sides[2].get_gs("left"))
        self.sides[0].set_left_n(*self.sides[4].get_gs("left"))
        self.sides[0].set_bottom_n(*self.sides[3].get_gs("left"))
        self.sides[0].set_right_n(*self.sides[5].get_gs("left"))

        self.sides[5].set_top_n(*self.sides[2].get_gs("bottom"))
        self.sides[5].set_left_n(*self.sides[0].get_gs("right"))
        self.sides[5].set_bottom_n(*self.sides[3].get_gs("top"))
        self.sides[5].set_right_n(*self.sides[1].get_gs("left"))

        self.sides[1].set_top_n(*self.sides[2].get_gs("right"))
        self.sides[1].set_left_n(*self.sides[5].get_gs("right"))
        self.sides[1].set_bottom_n(*self.sides[3].get_gs("right"))
        self.sides[1].set_right_n(*self.sides[4].get_gs("right"))

        self.sides[2].set_top_n(*self.sides[4].get_gs("bottom"))
        self.sides[2].set_left_n(*self.sides[0].get_gs("top"))
        self.sides[2].set_bottom_n(*self.sides[5].get_gs("top"))
        self.sides[2].set_right_n(*self.sides[1].get_gs("top"))

        self.sides[3].set_top_n(*self.sides[5].get_gs("bottom"))
        self.sides[3].set_left_n(*self.sides[0].get_gs("bottom"))
        self.sides[3].set_bottom_n(*self.sides[4].get_gs("top"))
        self.sides[3].set_right_n(*self.sides[1].get_gs("bottom"))

        self.sides[4].set_top_n(*self.sides[3].get_gs("bottom"))
        self.sides[4].set_left_n(*self.sides[0].get_gs("left"))
        self.sides[4].set_bottom_n(*self.sides[2].get_gs("top"))
        self.sides[4].set_right_n(*self.sides[1].get_gs("right"))

    def __str__(self) -> str:
        back = self.layout["back"].get_colors()
        front = self.layout["front"].get_colors()
        up = self.layout["up"].get_colors()
        down = self.layout["down"].get_colors()
        left = self.layout["left"].get_colors()
        right = self.layout["right"].get_colors()
        end = "\x1b[0m\n"
        out = ""
        for i in range(3):
            out += f"{' '*6}{back[i]}{end}"
        for i in range(3):
            out += f"{left[i]}{up[i]}{right[i]}{end}"
        for i in range(3):
            out += f"{' '*6}{front[i]}{end}"
        for i in range(3):
            out += f"{' '*6}{down[i]}{end}"
        return out

    def U(self):
        """Rotate the top side clockwise"""
        self.layout["up"].r_right()

    def U_(self):
        """Rotate the top side counterclockwise"""
        self.layout["up"].r_left()

    def D(self):
        """Rotate the bottom side clockwise"""
        self.layout["down"].r_right()

    def D_(self):
        """Rotate the bottom side counterclockwise"""
        self.layout["down"].r_left()

    def L(self):
        """Rotate the left side clockwise"""
        self.layout["left"].r_right()

    def L_(self):
        """Rotate the left side counterclockwise"""
        self.layout["left"].r_left()

    def R(self):
        """Rotate the right side clockwise"""
        self.layout["right"].r_right()

    def R_(self):
        """Rotate the right side counterclockwise"""
        self.layout["right"].r_left()

    def F(self):
        """Rotate the front side clockwise"""
        self.layout["front"].r_right()

    def F_(self):
        """Rotate the front side counterclockwise"""
        self.layout["front"].r_left()

    def B(self):
        """Rotate the back side clockwise"""
        self.layout["back"].r_right()

    def B_(self):
        """Rotate the back side counterclockwise"""
        self.layout["back"].r_left()

    def rLeft(self):
        """Rotate the cube by 90° along the Y-Axis"""
        tmp_side = self.layout["left"]
        self.layout["left"] = self.layout["back"]
        self.layout["back"] = self.layout["right"]
        self.layout["right"] = self.layout["front"]
        self.layout["front"] = tmp_side

    def rRight(self):
        """Rotate the cube by -90° along the Y-Axis"""
        tmp_side = self.layout["right"]
        self.layout["right"] = self.layout["back"]
        self.layout["back"] = self.layout["left"]
        self.layout["left"] = self.layout["front"]
        self.layout["front"] = tmp_side

    def mix(self, n_moves: int = 12):
        """Turn a random side of the cube n_moves times"""
        moves = [self.U, self.U_, self.D, self.D_, self.F, self.F_, self.B, self.B_, self.L, self.L_, self.R, self.R_]
        for _ in range(n_moves):
            choice(moves)()
