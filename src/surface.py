from point import Color, Point
import numpy as np
from OpenGL.GL import *
import math


MODE_BEZIER = 1
MODE_BSPLINE = 2
MODE_NURBS = 3

DEFAULT_CONTROL_POINTS = [
    [
        (0.00, 0.00, 0.00),
        (33.16, 6.66, 119.91),
        (66.50, 13.48, 139.99),
        (100.00, 20.00, 60.00),
    ],
    [
        (6.66, 25.00, 15.83),
        (39.82, 31.66, 135.74),
        (73.16, 38.48, 155.82),
        (106.66, 45.00, 75.83),
    ],
    [
        (13.48, 50.00, 31.74),
        (46.64, 56.66, 151.65),
        (79.98, 63.48, 171.73),
        (113.48, 70.00, 91.74),
    ],
    [
        (20.00, 75.00, 47.50),
        (53.16, 81.66, 167.41),
        (86.50, 88.48, 187.49),
        (120.00, 95.00, 107.50),
    ],
    [
        (26.84, 100.00, 63.42),
        (60.00, 106.66, 183.33),
        (93.34, 113.48, 203.41),
        (126.84, 120.00, 123.42),
    ],
]


class ControlPolyhedron:
    def __init__(
        self,
        control_points=DEFAULT_CONTROL_POINTS,
        frame_color=(1.0, 0.0, 0.0),
        point_size=5,
    ) -> None:
        self._control_points: list[list[Point]] = []
        self._point_size = point_size
        self._frame_color = frame_color

        # Controls
        self._show_control_points = True
        self._show_control_points_frame = True
        self._show_center_point = True

        self._process_init_control_points(control_points)

    def draw(self):
        if self._show_control_points:
            self._draw_control_points()

        if self._show_control_points_frame:
            self._draw_control_points_frame()

    def _process_init_control_points(
        self, init_control_points: list[list[tuple[float, float, float]]]
    ):
        buffer_list = []
        for control_point_line in init_control_points:
            for control_point in control_point_line:
                buffer_list.append(
                    Point(
                        control_point[0],
                        control_point[1],
                        control_point[2],
                        Color(0.0, 0.0, 0.0),
                    )
                )

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
                if (
                    i != len(self._control_points) - 1
                    and j != len(control_point_list) - 1
                ):
                    # Draw lines in two directions
                    glVertex3f(*self._control_points[i][j].get_coords_tuple())
                    glVertex3f(*self._control_points[i + 1][j].get_coords_tuple())

                    glVertex3f(*self._control_points[i][j].get_coords_tuple())
                    glVertex3f(*self._control_points[i][j + 1].get_coords_tuple())
                elif (
                    i == len(self._control_points) - 1
                    and j != len(control_point_list) - 1
                ):
                    glVertex3f(*self._control_points[i][j].get_coords_tuple())
                    glVertex3f(*self._control_points[i][j + 1].get_coords_tuple())
                elif (
                    i != len(self._control_points) - 1
                    and j == len(control_point_list) - 1
                ):
                    glVertex3f(*self._control_points[i][j].get_coords_tuple())
                    glVertex3f(*self._control_points[i + 1][j].get_coords_tuple())
        glEnd()

    def _draw_center_point(self, point_size=10):
        glPointSize(point_size)
        glBegin(GL_POINTS)
        self.get_bounding_box_center().set_point_color()
        self.get_bounding_box_center().draw_vertex()
        glEnd()

    def toggle_control_points_frame_visibility(self):
        self._show_control_points_frame = not self._show_control_points_frame

    def toggle_control_points_visibility(self):
        self._show_control_points = not self._show_control_points

    def toggle_center_point_visibility(self):
        self._show_center_point = not self._show_center_point

    def get_control_points(self):
        return self._control_points

    def get_bounding_box_center(self):
        # TODO: Clean up code later after debug and fixing (my soul left my body)
        min_point = self._get_min_point()
        max_point = self._get_max_point()

        result = (
            min_point.get_coords_numerical() + max_point.get_coords_numerical()
        ) / 2

        return Point(result[0], result[1], result[2])

    def _get_min_point(self):
        min_coords = list(self._control_points[0][0].get_coords_tuple())
        for control_point_list in self._control_points:
            for control_point in control_point_list:
                control_point_coords = control_point.get_coords_tuple()
                if min_coords[0] > control_point_coords[0]:
                    min_coords[0] = control_point_coords[0]
                if min_coords[1] > control_point_coords[1]:
                    min_coords[1] = control_point_coords[1]
                if min_coords[2] > control_point_coords[2]:
                    min_coords[2] = control_point_coords[2]

        return Point(min_coords[0], min_coords[1], min_coords[2])

    def _get_max_point(self):
        max_coords = list(self._control_points[0][0].get_coords_tuple())
        for control_point_list in self._control_points:
            for control_point in control_point_list:
                control_point_coords = control_point.get_coords_tuple()
                if max_coords[0] < control_point_coords[0]:
                    max_coords[0] = control_point_coords[0]
                if max_coords[1] < control_point_coords[1]:
                    max_coords[1] = control_point_coords[1]
                if max_coords[2] < control_point_coords[2]:
                    max_coords[2] = control_point_coords[2]

        return Point(max_coords[0], max_coords[1], max_coords[2])


class SurfaceModel:
    def __init__(self, control_points=DEFAULT_CONTROL_POINTS, step=0.1) -> None:
        # Making sure the step covers the whole [0,1] interval
        if (1 / step) % 1 != 0:
            raise Exception("(1 / step) % 1 must be equal to 0!")

        self._mesh_points: list[list[Point]] = []

        self.control_polyhedron: ControlPolyhedron = ControlPolyhedron(control_points)
        self._step = step  # To step the parameters of the surface functions

    def _surface_function(self, t, index, n, knot: list[float] = []) -> float:
        """
        "virtual function" (non-existent in python, only simulating)
        """
        return 0

    def _calculate_surface_points(self):
        """Populates the _mesh_points data matrix"""
        u_range, v_range = np.arange(0, 1 + self._step, self._step), np.arange(
            0, 1 + self._step, self._step
        )
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


class BezierSurfaceModel(SurfaceModel):
    def __init__(self, control_points=DEFAULT_CONTROL_POINTS, step=0.1):
        super().__init__(control_points, step)

        # for efficiency....later it needs to be calculated frequently
        self._calculate_surface_points()

    def _calculate_surface_point(self, u, v):
        """Populates the _mesh_points data matrix"""
        n = len(self.control_polyhedron.get_control_points())
        m = len(self.control_polyhedron.get_control_points()[0])
        numerical_point = np.zeros(3)
        for i in range(n):
            for j in range(m):
                numerical_point += (
                    self._surface_function(u, i, n - 1)
                    * self._surface_function(v, j, m - 1)
                    * self.control_polyhedron.get_control_points()[i][j].get_coords_numerical()
                )

        return numerical_point

    def _surface_function(self, t, index, n, knot: list[float] = []):
        """
        Bernstein polynomial.
        u - function parameter, range -> [0, 1]
        index - index of current point
        n - total number of points - 1
        """
        return math.comb(n, index) * math.pow(t, index) * math.pow(1 - t, n - index)


class BsplineSurfaceModel(SurfaceModel):
    def __init__(
        self,
        control_points=DEFAULT_CONTROL_POINTS,
        step=0.1,
        degree_p=3,
        degree_q=3,
        knot_u=[0, 0, 0, 0.2, 0.2, 0.5, 0.5, 0.7, 1],
        knot_v=[0, 0, 0, 0.3, 0.3, 0.5, 0.5, 1],
    ):
        super().__init__(control_points, step)
        # h/k piece of knots in the each direction must hold: h = m + p + 1 (p is the degree)
        self._knot_u = knot_u
        self._knot_v = knot_v

        self._m = len(self.control_polyhedron.get_control_points()) - 1
        self._n = len(self.control_polyhedron.get_control_points()[0]) - 1

        # TODO: raise exeptions if the degrees are incorrect
        self._degree_p = degree_p  # degree in u direction
        self._degree_q = degree_q  # degree in v direction

        # if len(self._knot_u) - 1 == self._m + self._p + 1:
        #     raise Exception(f'''Bad u knot vector\n
        #             h =  {len(self._knot_u)}
        #             m + p + 1 = {self._m + self._p + 1}
        #         ''')

        # if len(self._knot_v) - 1 == self._n + self._q + 1:
        #     raise Exception(f'''Bad u knot vector\n
        #             h =  {len(self._knot_v)}
        #             m + p + 1 = {self._n + self._q + 1}
        #         ''')

        # for efficiency....later it needs to be calculated frequently, when controls are added
        self._calculate_surface_points()

    def _calculate_surface_point(self, u, v):
        numerical_point = np.zeros(3)
        for i in range(self._m + 1):
            for j in range(self._n + 1):
                numerical_point += (
                    self._surface_function(u, i, self._degree_p, self._knot_u)
                    * self._surface_function(v, j, self._degree_q, self._knot_v)
                    * self.control_polyhedron.get_control_points()[i][j].get_coords_numerical()
                )

        return numerical_point

    def _surface_function(self, t, index, n, knot: list[float] = []):
        """
        B-spline basis function
        t - function parameter, range -> [0, 1]
        index - index of current point
        n - degree
        knot - knot vector when calculating bsplines
        """

        if n == 0:
            if t >= knot[index] and t < knot[index + 1]:
                return 1
            else:
                return 0

        # guard against zero divison
        if knot[index + n] == knot[index]:
            first_term = 0
        else:
            first_term = (
                (t - knot[index]) / (knot[index + n] - knot[index])
            ) * self._surface_function(t, index, n - 1, knot)

        if knot[index + n + 1] == knot[index + 1]:
            second_term = 0
        else:
            second_term = (
                (knot[index + n + 1] - t) / (knot[index + n + 1] - knot[index + 1])
            ) * self._surface_function(t, index + 1, n - 1, knot)

        return first_term + second_term


global surface
surface = SurfaceDisplay(BezierSurfaceModel())
