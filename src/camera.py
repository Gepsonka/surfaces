from OpenGL.GLU import *


class Camera:
    '''Singleton class for handling camera'''
    def __init__(
        self,
        coords: tuple[float, float, float],
        looking_at: tuple[float, float, float],
        up_vec: tuple[float, float, float],
    ):
        self._coords = coords
        self._looking_at = looking_at
        self._up_vec = up_vec

    def init_camera(self):
        gluLookAt(*self._coords, *self._looking_at, *self._up_vec)


camera = Camera((25.0, 25.0, 70.0), (25.0, 25.0, 0.0), (0.0, 1.0, 0.0))
