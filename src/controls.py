from OpenGL.GLUT import *
from surface import BezierSurfaceModel, BsplineSurfaceModel, NURBSModel, SurfaceDisplay, surface
from typing import Callable

ROTATE_SENSITIVITY_ANGLE = 5


def keyboardFunction(key, x: int, y: int):
    key = key.decode('utf-8')
    if key == ']':
        surface._surface_model.control_polyhedron.toggle_control_points_visibility()
        glutPostRedisplay()
    elif key == '[':
        surface._surface_model.control_polyhedron.toggle_control_points_frame_visibility()
        glutPostRedisplay()
    elif key == ',':
        surface._rotate_angle_z += ROTATE_SENSITIVITY_ANGLE
        glutPostRedisplay()
    elif key == '.':
        surface._rotate_angle_z -= ROTATE_SENSITIVITY_ANGLE
        glutPostRedisplay()
    elif key == 'q':
        surface.toggle_surface_visibility()
        glutPostRedisplay()
    elif key == 'w':
        surface.toggle_surface_points_visiblity()
        glutPostRedisplay()
    elif key == '1':
        surface.swich_surface_model(BezierSurfaceModel())
        glutPostRedisplay()
    elif key == '2':
        surface.swich_surface_model(BsplineSurfaceModel())
        glutPostRedisplay()
    elif key == '3':
        surface.swich_surface_model(NURBSModel())
        glutPostRedisplay()


def specialKeyboardFunction(key, x: int, y: int):
    if key == GLUT_KEY_UP:
        surface._rotate_angle_x += ROTATE_SENSITIVITY_ANGLE
        glutPostRedisplay()
    elif key == GLUT_KEY_DOWN:
        surface._rotate_angle_x -= ROTATE_SENSITIVITY_ANGLE
        glutPostRedisplay()
    elif key == GLUT_KEY_LEFT:
        surface._rotate_angle_y += ROTATE_SENSITIVITY_ANGLE
        glutPostRedisplay()
    elif key == GLUT_KEY_RIGHT:
        surface._rotate_angle_y -= ROTATE_SENSITIVITY_ANGLE
        glutPostRedisplay()
