from typing import Callable
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from camera import camera
from surface_display import surface

WINDOW_SIZE = (1200, 800)
WINDOW_POSITION = (50, 50)
WINDOW_TITLE = b"Surfaces"

NEAR_CLIPPING_PLANE = 0.1
FAR_CLIPPING_PLANE = 1000.0


def initGlut(
    displayFunc: Callable[[], None],
    resizeFunc: Callable[[int, int], None] | None = None,
    keyboardFunc: Callable[[int, int, int], None] | None = None,
    specialFunc: Callable[[int, int, int], None] | None = None,
    mouseFunc: Callable[[int, int, int, int], None] | None = None
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

    if mouseFunc is not None:
        glutMouseFunc(mouseFunc)

    glShadeModel(GL_SMOOTH)

    glClearColor(0.0, 0.0, 0.0, 1.0)

    glutMainLoop()


def resizeFunction(w, h):
    WINDOW_SIZE = (w, h) # bad practice, never do this!
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w / h, NEAR_CLIPPING_PLANE, FAR_CLIPPING_PLANE)
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
