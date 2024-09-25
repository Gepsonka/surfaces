from point import Color, Point
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from surfaces.surface import SurfaceModel
from surfaces.bezier import BezierSurfaceModel


class SurfaceDisplay:
    def __init__(self, surface_model: SurfaceModel, mesh_color = (0.0, 0.0, 0.0)) -> None:
        self._surface_model = surface_model
        self._mesh_color = mesh_color

        self._rotate_angle_x = -120
        self._rotate_angle_y = 0
        self._rotate_angle_z = 0
        # Controls
        self._show_surface: bool = True
        self._show_surface_points: bool = True

    def draw(self):
        bounding_polyhedron_center_point = (
            self._surface_model.control_polyhedron.get_bounding_box_center()
        )

        glRotatef(self._rotate_angle_z, 0, 0, 1)
        glRotatef(self._rotate_angle_y, 0, 1, 0)
        glRotatef(self._rotate_angle_x, 1, 0, 0)
        glRotatef(50, 0, 1, -1)
        glTranslatef(
            -bounding_polyhedron_center_point.get_coords_tuple()[0],
            -bounding_polyhedron_center_point.get_coords_tuple()[1],
            -bounding_polyhedron_center_point.get_coords_tuple()[1],
        )

        self._surface_model.control_polyhedron.draw()

        if self._show_surface:
            self._draw_surface_mesh()

        if self._show_surface_points:
            self._draw_surface_points()


    def _draw_surface_points(self):
        if len(self._surface_model._mesh_points) == 0:
            return

        glColor3f(0.0, 0.0, 1.0)
        glPointSize(3)
        glBegin(GL_POINTS)
        for i, surface_point_list in enumerate(self._surface_model._mesh_points):
            for j, _ in enumerate(surface_point_list):
                glVertex3f(*self._surface_model._mesh_points[i][j].get_coords_tuple())
        glEnd()

    def _draw_surface_mesh(self):
        if len(self._surface_model._mesh_points) == 0:
            return

        glColor3f(*self._mesh_color)
        glBegin(GL_LINES)
        for i, surface_point_list in enumerate(self._surface_model._mesh_points):
            for j, _ in enumerate(surface_point_list):
                if j < len(self._surface_model._mesh_points[i]) - 1:
                    glVertex3f(
                        *self._surface_model._mesh_points[i][j].get_coords_tuple()
                    )
                    glVertex3f(
                        *self._surface_model._mesh_points[i][j + 1].get_coords_tuple()
                    )

                if i < len(self._surface_model._mesh_points) - 1:
                    glVertex3f(
                        *self._surface_model._mesh_points[i][j].get_coords_tuple()
                    )
                    glVertex3f(
                        *self._surface_model._mesh_points[i + 1][j].get_coords_tuple()
                    )
        glEnd()

    def swich_surface_model(self, surface_model: SurfaceModel):
        self._surface_model = surface_model


    def toggle_surface_visibility(self):
        self._show_surface = not self._show_surface

    def toggle_surface_points_visiblity(self):
        self._show_surface_points = not self._show_surface_points


global surface
surface = SurfaceDisplay(BezierSurfaceModel())
