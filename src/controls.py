from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
from opengl import WINDOW_SIZE
from point_click import RayPicker, pick
from surfaces.control_polyhedron import control_polyhedron
from surfaces.bezier import BezierSurfaceModel
from surfaces.bspline import BsplineSurfaceModel
from surfaces.nurbs import NURBSModel
from typing import Callable
from surface_display import surface
import numpy as np

ROTATE_SENSITIVITY_ANGLE = 5
POINT_MOVE_SENSITIVITY = 5
CONTROL_POINT_WEIGHT_CHANGE_SENSITIVITY = 5


def keyboardFunction(key, x: int, y: int):
    key = key.decode('utf-8')

    if control_polyhedron.get_selected_point_index() is not None:
        if key == ',':
            control_polyhedron.move_selected_point(0, 0, -POINT_MOVE_SENSITIVITY)
            surface._surface_model._calculate_surface_points()
            glutPostRedisplay()
        elif key == '.':
            control_polyhedron.move_selected_point(0, 0, POINT_MOVE_SENSITIVITY)
            surface._surface_model._calculate_surface_points()
            glutPostRedisplay()
        
        if type(surface._surface_model) == NURBSModel:
            if key == '+':
                surface._surface_model.change_weight_on_index(*control_polyhedron.get_selected_point_index(), CONTROL_POINT_WEIGHT_CHANGE_SENSITIVITY)
                surface._surface_model._calculate_surface_points()
                glutPostRedisplay()
            if key == '-':
                surface._surface_model.change_weight_on_index(*control_polyhedron.get_selected_point_index(), -CONTROL_POINT_WEIGHT_CHANGE_SENSITIVITY)
                surface._surface_model._calculate_surface_points()
                glutPostRedisplay()
        return

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
    if control_polyhedron.get_selected_point_index() is not None:
        if key == GLUT_KEY_LEFT:
            control_polyhedron.move_selected_point(-POINT_MOVE_SENSITIVITY, 0, 0)
            surface._surface_model._calculate_surface_points()
            glutPostRedisplay()
        elif key == GLUT_KEY_RIGHT:
            control_polyhedron.move_selected_point(POINT_MOVE_SENSITIVITY, 0, 0)
            surface._surface_model._calculate_surface_points()
            glutPostRedisplay()
        elif key == GLUT_KEY_UP:
            control_polyhedron.move_selected_point(0, POINT_MOVE_SENSITIVITY, 0)
            surface._surface_model._calculate_surface_points()
            glutPostRedisplay()
        elif key == GLUT_KEY_DOWN:
            control_polyhedron.move_selected_point(0, -POINT_MOVE_SENSITIVITY, 0)
            surface._surface_model._calculate_surface_points()
            glutPostRedisplay()

        
        return 

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


def get_screen_coordinates(point):
    # Get the current matrices and viewport
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    viewport = glGetIntegerv(GL_VIEWPORT)

    # Transform the point to window coordinates
    window_coordinates = gluProject(point[0], point[1], point[2], modelview, projection, viewport)
    return window_coordinates

def get_world_coordinates(point):
    # Get the current modelview matrix
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    
    # Transform the point to world coordinates
    point_h = np.array([*point, 1.0])  # Convert to homogeneous coordinates
    world_coords = modelview.dot(point_h)
    world_coords = world_coords / world_coords[3]  # Normalize by the homogeneous component
    
    # Return the transformed coordinates (ignore the homogeneous component)
    return world_coords[:3]

def mouseFunction(button, state, x, y):
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            ray_picker = RayPicker()
            # FOR DEBUG PURPOSES!!
            base_point = control_polyhedron.get_control_points()[0][0]
            projected_coords = get_screen_coordinates(base_point.get_coords_tuple())
            print(f"Projected coordinates: {projected_coords}")
            print(f"World coordinates: {get_world_coordinates(base_point.get_coords_tuple())}")
            print("click coords: ", x, y)
            print("corrigated click coords: ", x, WINDOW_SIZE[1] - y)



            if pick(x, y, base_point.get_coords_tuple()):
                print("point was clicked")

            for row_index, row in enumerate(control_polyhedron.get_control_points()):
                for index, point in enumerate(row):                    
                    if pick(x, y, point.get_coords_tuple()):
                        control_polyhedron.select_point(row_index, index)
                        glutPostRedisplay()
                        print(f"Point selected: {point}")
                        return
                    else:
                        control_polyhedron.deselect_point()
                        glutPostRedisplay()