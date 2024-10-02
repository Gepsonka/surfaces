from OpenGL.GL import *
from OpenGL.GLU import *
from point import Color, Point
from surfaces.constants import DEFAULT_CONTROL_POINTS


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
                point = Point(
                    control_point[0],
                    control_point[1],
                    control_point[2],
                    Color(0.0, 0.0, 0.0),
                )
                point.toggle_selected()

                buffer_list.append(point)

            self._control_points.append(buffer_list)
            buffer_list = []

    def _draw_control_points(self):
        glPointSize(self._point_size)
        for point_list in self._control_points:
            for point in point_list:
                point.set_point_color()
                point.draw()

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
        self.get_bounding_box_center().draw()
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

    def convert_to_numerical(self):
        buffer_list = []
        for row in self.get_control_points():
            buffer_list.append([point.get_coords_numerical() for point in row])

        return buffer_list

    def check_click(self):
        pass


control_polyhedron = ControlPolyhedron()
