from point import Color, Point
import numpy as np
from OpenGL.GL import *
import math


MODE_BEZIER = 1
MODE_BSPLINE = 2
MODE_NURBS = 3

DEFAULT_CONTROL_POINTS = [
    [(0.00, 0.00, 0.00), (33.16, 6.66, 19.91), (66.50, 13.48, 39.99), (100.00, 20.00, 60.00)],
    [(6.66, 25.00, 15.83), (39.82, 31.66, 35.74), (73.16, 38.48, 55.82), (106.66, 45.00, 75.83)],
    [(13.48, 50.00, 31.74), (46.64, 56.66, 51.65), (79.98, 63.48, 71.73), (113.48, 70.00, 91.74)],
    [(20.00, 75.00, 47.50), (53.16, 81.66, 67.41), (86.50, 88.48, 87.49), (120.00, 95.00, 107.50)],
    [(26.84, 100.00, 63.42), (60.00, 106.66, 83.33), (93.34, 113.48, 103.41), (126.84, 120.00, 123.42)]
]


class ControlPolyhedron:
    def __init__(self, control_points = DEFAULT_CONTROL_POINTS, frame_color = (1.0, 0.0, 0.0), point_size = 5) -> None:
        self._control_points: list[list[Point]] = []
        self._point_size = point_size
        self._frame_color = frame_color

        # Controls
        self._show_control_points = True
        self._show_control_points_frame = True

        self._process_init_control_points(control_points)

    def draw(self):
        if self._show_control_points_frame:
            self._draw_control_points_frame()

        if self._show_control_points:
            self._draw_control_points()

    def _process_init_control_points(self, init_control_points: list[list[tuple[float, float, float]]]):
        buffer_list = []
        for control_point_line in init_control_points:
            for control_point in control_point_line:
                buffer_list.append(Point(control_point[0], control_point[1], control_point[2], Color(0.0, 0.0, 0.0)))

            self._control_points.append(buffer_list)
            buffer_list = []

    def _draw_control_points(self):
        glPointSize(self._point_size)
        glBegin(GL_POINTS)
        for point_list in self._control_points:
            for point in point_list:
                point.set_point_color()
                point.draw_vertex()
        glEnd()

    def _draw_control_points_frame(self):
        glColor3f(*self._frame_color)
        glBegin(GL_LINES)
        for i, control_point_list in enumerate(self._control_points):
            for j, control_point in enumerate(control_point_list):
                if i != len(self._control_points)-1 and j != len(control_point_list)-1:
                    # Draw lines in two directions
                    glVertex3f(*self._control_points[i][j].get_coords_tuple())
                    glVertex3f(*self._control_points[i+1][j].get_coords_tuple())

                    glVertex3f(*self._control_points[i][j].get_coords_tuple())
                    glVertex3f(*self._control_points[i][j+1].get_coords_tuple())
                elif i == len(self._control_points)-1 and j != len(control_point_list)-1:
                    glVertex3f(*self._control_points[i][j].get_coords_tuple())
                    glVertex3f(*self._control_points[i][j+1].get_coords_tuple())
                elif i != len(self._control_points)-1 and j == len(control_point_list)-1:
                    glVertex3f(*self._control_points[i][j].get_coords_tuple())
                    glVertex3f(*self._control_points[i+1][j].get_coords_tuple())
        glEnd()

    def set_control_points_frame_visibility(self):
        self._show_control_points_frame = not self._show_control_points_frame

    def set_control_points_visibility(self):
        self._show_control_points = not self._show_control_points

    def get_control_points(self):
        return self._control_points



# TODO: separate drawing and mathematical calculations into different classes

class Surface:
    def __init__(self, control_points = DEFAULT_CONTROL_POINTS, step = 0.1) -> None:
        # Making sure the step covers the whole [0,1] interval
        if (1 / step) % 10 != 0:
            raise Exception("(1 / step) % 10 must be equal to 0!")

        self._mesh_points: list[list[Point]] = []
        self._rotate_angle = 0
        self._control_polyeder = ControlPolyhedron(control_points)
        self._step = step # To step the parameters of the surface functions

        # Controls
        self._show_surface = False
        self._show_control_polyhedron = True

    def draw(self):
        glRotatef(self._rotate_angle, 0, 1, 0)

        if self._show_control_polyhedron:
            self._control_polyeder.draw()

        if self._show_surface:
            self._draw_surface_mesh()

    def _draw_surface_mesh(self):
        if len(self._mesh_points) == 0:
            return

        glBegin(GL_LINES)
        for i, surface_point_list in enumerate(self._mesh_points[:-1]):
            for j, _ in enumerate(surface_point_list[:-1]):
                glVertex3f(*self._mesh_points[i][j].get_coords_tuple())
                glVertex3f(*self._mesh_points[i+1][j].get_coords_tuple())

                glVertex3f(*self._mesh_points[i][j].get_coords_tuple())
                glVertex3f(*self._mesh_points[i][j+1].get_coords_tuple())
        glEnd()


    def _surface_function(self, t, index, n) -> float:
        '''
        "virtual function" (non-existent in python, only simulating)
        '''
        return 0

    def _calculate_surface_point(self, u, v):
        n = len(self._control_polyeder._control_points)
        m = len(self._control_polyeder._control_points[1])
        point = np.zeros(3)
        for i in range(n + 1):
            for j in range(m + 1):
                point += self._surface_function(u, i, n) * self._surface_function(v, j, m) * self._control_polyeder._control_points[i][j].get_coords_numerical()

        return point

    def _calculate_surface_points(self):
        '''Populates the _mesh_points data matrix'''
        u, v = 0, 0
        buffer_list = []

        while u <= 1:
            while v <= 1:
                numerical_point = self._calculate_surface_point(u, v)
                buffer_list.append(Point(numerical_point[0], numerical_point[1], numerical_point[2]))
                v+= self._step

            self._mesh_points.append(buffer_list)
            buffer_list = []
            u += self._step

    def set_surface_visibility(self):
        self._show_surface = not self._show_surface



class BezierSurface(Surface):
    def __init__(self, control_points = DEFAULT_CONTROL_POINTS, step = 0.1):
        super().__init__(control_points, step)

    def _surface_function(self, t, index, n):
        '''
        Bernstein polynomial.
        u - function parameter, range -> [0, 1]
        index - index of current point
        n - total number of points
        '''
        return math.comb(n, index) * math.pow(t, index) * math.pow(1-t, n-index)




surface = Surface()
