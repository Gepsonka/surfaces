from point import Color, Point
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from surfaces.constants import DEFAULT_CONTROL_POINTS
from surfaces.control_polyhedron import ControlPolyhedron, control_polyhedron

class SurfaceModel:
    def __init__(self, control_polyhedon: ControlPolyhedron=control_polyhedron, step=0.1) -> None:
        # Making sure the step covers the whole [0,1] interval
        if (1 / step) % 1 != 0:
            raise Exception("(1 / step) % 1 must be equal to 0!")

        self._mesh_points: list[list[Point]] = []

        self.control_polyhedron: ControlPolyhedron = control_polyhedron
        self._step = step  # To step the parameters of the surface functions

    def _surface_function(self, t, index, n, knot: list[float] = []) -> float:
        """
        "virtual function" (non-existent in python, only simulating)
        """
        return 0

    def _calculate_surface_points(self):
        """Populates the _mesh_points data matrix"""
        self._mesh_points = []

        u_range, v_range = np.arange(0, 1 + self._step, self._step), np.arange(0, 1 + self._step, self._step)

        buffer_list = []

        for u in u_range:
            for v in v_range:
                numerical_point = self._calculate_surface_point(u, v)
                buffer_list.append(
                    Point(numerical_point[0], numerical_point[1], numerical_point[2])
                )
            self._mesh_points.append(buffer_list)
            buffer_list = []
            v = np.arange(0, 1 + self._step, self._step)


    def _calculate_surface_point(self, u, v):
        """Virtual function"""
        return np.zeros(3)

    def convert_mesh_points_to_tuple(self):
        buffer_list = []
        for row in self._mesh_points:
            buffer_list.append([point.get_coords_tuple() for point in row])
