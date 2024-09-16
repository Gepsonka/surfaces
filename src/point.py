import numpy as np
from OpenGL.GL import *


class Color:
    def __init__(self, red, green, blue) -> None:
        self._red = red
        self._blue = blue
        self._green = green

    def set_color(self, red, blue, green):
        self.__init__(red, blue, green)

    def get_color_tuple(self) -> tuple[int, int, int]:
        return (self._red, self._green, self._blue)


class Point:
    def __init__(self, x: float | int, y: float | int, z: float | int, color: Color | None = None, size = 1) -> None:
        self._x = x
        self._y = y
        self._z = z
        self._color = color
        self._size = size
        self._is_active = False # for later use when selecting points

    def get_coords(self):
        # For computational convenience when dealing with curves
        return np.array([self._x, self._y, self._z]).T

    def draw_point(self):
        '''Only works in GL_POINTS mode'''
        if self._color != None:
            glColor3f(*self._color.get_color_tuple())

        glPointSize(self._size)
        glVertex3f(self._x, self._z, self._y)
