from typing import Callable

from OpenGL.GLUT import *

BEZIER_OPTION = 1
BSPLINE_OPTION = 2
NURBS_OPTION = 3


class Menu:
    def __init__(self, callback: Callable[[int], None]):
        self._callback = callback

        menu = glutCreateMenu(callback)
        glutAddMenuEntry("Bezier", BEZIER_OPTION)
        glutAddMenuEntry("B-spline", BSPLINE_OPTION)
        glutAddMenuEntry("NURBS", NURBS_OPTION)
        glutAttachMenu(GLUT_RIGHT_BUTTON)
