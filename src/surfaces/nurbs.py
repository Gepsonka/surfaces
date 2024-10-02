from surfaces.bspline import BsplineSurfaceModel
from surfaces.constants import DEFAULT_CONTROL_POINTS, DEFAULT_DEGREE_U, DEFAULT_DEGREE_V, DEFAULT_STEP, DEFAULT_U_KNOT_VECTOR, DEFAULT_V_KNOT_VECTOR
import numpy as np

class NURBSModel(BsplineSurfaceModel):
    def __init__(self, control_points=DEFAULT_CONTROL_POINTS, step=DEFAULT_STEP, degree_u=DEFAULT_DEGREE_U, degree_v=DEFAULT_DEGREE_V, knot_u=DEFAULT_U_KNOT_VECTOR, knot_v=DEFAULT_V_KNOT_VECTOR):
        # Had to do this because of the cross dependencies of variables
        self.weights = self._generate_weights(len(control_points), len(control_points[0]))
        self.weights[3][3] = 10

        self._m = len(control_points)
        self._n = len(control_points[0])

        super().__init__(control_points, step, degree_u, degree_v)

    def _generate_weights(self, x, y):
        return np.ones((x,y))

    def _calculate_surface_point(self, u, v):
        surface_point = np.zeros(3)

        for i in range(self._m + 1):
            for j in range(self._n + 1):
                surface_point += self._nurbs_general_form(u, v, i, j) * self.control_polyhedron.get_control_points()[i][j].get_coords_numerical()

        return surface_point

    def _nurbs_general_form(self, u, v, i, j):
        '''
        R_{i,j} (u, v)
        '''
        numerator = self._surface_function(u, i, self._degree_u, self._knot_u) * \
                    self._surface_function(v, j, self._degree_v, self._knot_v) * \
                    self.weights[i][j]
        denominator = 0
        for k in range(self._m + 1):
            for l in range(self._n + 1):
                denominator += (
                    self._surface_function(u, k, self._degree_u, self._knot_u) *
                    self._surface_function(v, l, self._degree_v, self._knot_v) *
                    self.weights[k][l]
                )
        return numerator / denominator if denominator != 0 else 0
