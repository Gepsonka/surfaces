from point import Color, Point

MODE_BEZIER = 1
MODE_BSPLINE = 2

BASE_CONTROL_POINTS = [[]]


class Surface:
    def __init__(self, control_points = BASE_CONTROL_POINTS, mode = MODE_BEZIER) -> None:
        self._mode = mode
        self._control_points = []
