from typing import Callable
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

WINDOW_SIZE = (1200, 1200)
WINDOW_POSITION = (50, 50)
WINDOW_TITLE = b"Surfaces"


class Camera:
    def __init__(
        self,
        coords: tuple[float, float, float],
        looking_at: tuple[float, float, float],
        up_vec: tuple[float, float, float],
    ):
        self._coords = coords
        self._looking_at = looking_at
        self._up_vec = up_vec

    def init_camera(self):
        gluLookAt(*self._coords, *self._looking_at, *self._up_vec)


def initGlut(
    displayFunc: Callable[[], None],
    resizeFunc: Callable[[int, int], None] | None = None,
    keyboardFunc: Callable[[int, int, int], None] | None = None,
    specialFunc: Callable[[int, int, int], None] | None = None,
) -> None:
    glutInit()
    # glutInitContextVersion(4, 1)
    # glutInitContextProfile(GLUT_COMPATIBILITY_PROFILE)

    glutInitDisplayMode(int(GLUT_DOUBLE) | int(GLUT_RGBA) | int(GLUT_DEPTH))
    glutInitWindowSize(WINDOW_SIZE[0], WINDOW_SIZE[1])
    glutInitWindowPosition(WINDOW_POSITION[0], WINDOW_POSITION[1])
    glutCreateWindow(WINDOW_TITLE)

    glutDisplayFunc(displayFunc)
    if resizeFunc is not None:
        print(resizeFunc)
        glutReshapeFunc(glutReshapeFunc)
    if glutKeyboardFunc is not None:
        glutKeyboardFunc(glutKeyboardFunc)
    if glutSpecialFunc is not None:
        glutSpecialFunc(specialFunc)

    glClearColor(1.0, 1.0, 1.0, 0.0)

    glutMainLoop()


def resizeFunction(w, h):
    print("heigth: ", h, " width: ", w)
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w / h, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def displayFunction():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(int(GL_COLOR_BUFFER_BIT) | int(GL_DEPTH_BUFFER_BIT))
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()

    glFlush()
