from surfaces.surface import SurfaceModel
from surfaces.constants import DEFAULT_CONTROL_POINTS, DEFAULT_STEP
import numpy as np
import math

class BezierSurfaceModel(SurfaceModel):
    def __init__(self, control_points=DEFAULT_CONTROL_POINTS, step=DEFAULT_STEP):
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
