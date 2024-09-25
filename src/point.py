import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *


class Color:
    def __init__(self, red: float | int, green: float | int, blue: float | int) -> None:
        self._red = red
        self._blue = blue
        self._green = green

    def set_color(self, red, blue, green):
        self.__init__(red, blue, green)

    def get_color_tuple(self) -> tuple[int | float, int | float, int | float]:
        return (self._red, self._green, self._blue)


DEFAULT_COLOR = Color(1.0, 1.0, 1.0) # black


class Arrow:
    CONE_BASE_RADIUS = 2
    CONE_HEIGHT = 3
    POINT_LENGTH = 10
    LINE_WIDTH = 2

    def __init__(self, point_window_coords):
        self._point_window_coords = point_window_coords



    def draw_arrows(self):
        self._draw_x_arrow()
        # self._draw_y_arrow()
        # self._draw_z_arrow()

        glLineWidth(1.0)

    def _draw_x_arrow(self):
        # Draw cone
        glPushMatrix()

        glColor3f(1.0, .0, .0)

        glTranslatef(self._point_window_coords[0], self._point_window_coords[1], self._point_window_coords[2])
        glTranslatef(self.POINT_LENGTH, 0.0, 0.0)
        glRotatef(90, 0, 1, 0)

        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, GL_TRUE)
        gluCylinder(quadric, self.CONE_BASE_RADIUS, 0.0, self.CONE_HEIGHT, 32, 32)

        glPopMatrix()

        # Draw line
        glPushMatrix()

        # glColor3f(1.0, .0, .0)
        glLineWidth(self.LINE_WIDTH)

        glTranslatef(self._point_window_coords[0], self._point_window_coords[1], self._point_window_coords[2])

        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(self.POINT_LENGTH, 0, 0)
        glEnd()
        glPopMatrix()

    def _draw_y_arrow(self):
        # Draw cone
        glPushMatrix()

        glColor3f(0.0, .0, 1.0)

        glTranslatef(self._point_window_coords[0], self._point_window_coords[1], self._point_window_coords[2])
        glTranslatef(self.POINT_LENGTH, 0.0, 0.0)

        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, GL_TRUE)
        gluCylinder(quadric, self.CONE_BASE_RADIUS, 0.0, self.CONE_HEIGHT, 32, 32)

        glPopMatrix()

        # Draw line
        glPushMatrix()

        glColor3f(1.0, .0, .0)
        glLineWidth(self.LINE_WIDTH)

        glTranslatef(self._point_window_coords[0], self._point_window_coords[1], self._point_window_coords[2])

        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, self.POINT_LENGTH, 0)
        glEnd()
        glPopMatrix()

    def _draw_z_arrow(self):
        # Draw cone
        glPushMatrix()

        glColor3f(1.0, .0, .0)

        glTranslatef(self._point_window_coords[0], self._point_window_coords[1], self._point_window_coords[2])
        glTranslatef(self.POINT_LENGTH, 0.0, 0.0)
        glRotatef(90, 0, 0, 1)

        quadric = gluNewQuadric()
        gluQuadricNormals(quadric, GLU_SMOOTH)
        gluQuadricTexture(quadric, GL_TRUE)
        gluCylinder(quadric, self.CONE_BASE_RADIUS, 0.0, self.CONE_HEIGHT, 32, 32)

        glPopMatrix()

        # Draw line
        glPushMatrix()

        glColor3f(1.0, .0, .0)
        glLineWidth(self.LINE_WIDTH)

        glTranslatef(self._point_window_coords[0], self._point_window_coords[1], self._point_window_coords[2])

        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, self.POINT_LENGTH)
        glEnd()
        glPopMatrix()



class Point:
    def __init__(self, x: float | int, y: float | int, z: float | int, color: Color = DEFAULT_COLOR) -> None:
        self._x = x
        self._y = y
        self._z = z
        self._color = color
        self._is_active = True # for later use when selecting points


    def get_coords_numerical(self):
        # For computational convenience when dealing with curves
        return np.array([self._x, self._y, self._z])

    def get_coords_tuple(self):
        return (self._x, self._y, self._z)

    def set_point_color(self, color: Color | None = None):
        if color is not None:
            glColor3f(*color.get_color_tuple())
        else:
            glColor3f(*self._color.get_color_tuple())

    def draw(self):
        glVertex3f(*self.get_coords_tuple())

    def _draw_axis_arrows(self):
        pass

    def toggle_selected(self):
        self._is_active = not self._is_active

    def _get_transformed_point_coords(self):
        modelview_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        projection_matrix = glGetFloatv(GL_PROJECTION_MATRIX)
        modelview_matrix = np.array(modelview_matrix).reshape(4, 4)
        projection_matrix = np.array(projection_matrix).reshape(4, 4)

        original_point = np.array([*self.get_coords_tuple(),  1.0])

        mvp_matrix = modelview_matrix.dot(projection_matrix)
        transformed_point = mvp_matrix.dot(original_point)


        # if transformed_point[3] != 0:
        #     transformed_point /= transformed_point[3]


        return transformed_point

    def draw_arrows(self):
        # if not self._is_active:
        #     return

        arrow = Arrow(self._get_transformed_point_coords())
        arrow.draw_arrows()


    def __str__(self):
        return str(self.get_coords_tuple())
