from typing import Callable
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from camera import camera
from menu import Menu
from surface import surface

WINDOW_SIZE = (1200, 800)
WINDOW_POSITION = (50, 50)
WINDOW_TITLE = b"Surfaces"


def optionClick(x):
    print(x)


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
        glutReshapeFunc(resizeFunc)
    if glutKeyboardFunc is not None:
        glutKeyboardFunc(keyboardFunc)
    if glutSpecialFunc is not None:
        glutSpecialFunc(specialFunc)

    glClearColor(0.0, 0.0, 0.0, 1.0)

    Menu(optionClick)

    glutMainLoop()


def resizeFunction(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w / h, 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def displayFunction():
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glClear(int(GL_COLOR_BUFFER_BIT) | int(GL_DEPTH_BUFFER_BIT))
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()

    camera.init_camera()

    surface.draw()

    glutSwapBuffers()
