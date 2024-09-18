import numpy as np
from OpenGL.GL import *


class Color:
    def __init__(self, red: float | int, green: float | int, blue: float | int) -> None:
        self._red = red
        self._blue = blue
        self._green = green

    def set_color(self, red, blue, green):
        self.__init__(red, blue, green)

    def get_color_tuple(self) -> tuple[int | float, int | float, int | float]:
        return (self._red, self._green, self._blue)


DEFAULT_COLOR = Color(1.0, 1.0, 1.0) # black

class Point:
    def __init__(self, x: float | int, y: float | int, z: float | int, color: Color = DEFAULT_COLOR) -> None:
        self._x = x
        self._y = y
        self._z = z
        self._color = color
        self._is_active = False # for later use when selecting points

    def get_coords_numerical(self):
        # For computational convenience when dealing with curves
        return np.array([self._x, self._y, self._z]).T

    def get_coords_tuple(self):
        return (self._x, self._y, self._z)


    def set_point_color(self, color: Color | None = None):
        if color is not None:
            glColor3f(*color.get_color_tuple())
        else:
            glColor3f(*self._color.get_color_tuple())

    def draw_vertex(self):
        glVertex3f(*self.get_coords_tuple())

    def _draw_axis_arrows(self):
        pass
