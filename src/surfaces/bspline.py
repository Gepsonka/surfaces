from surfaces.surface import SurfaceModel
from surfaces.constants import DEFAULT_CONTROL_POINTS, DEFAULT_STEP
import numpy as np

class BsplineSurfaceModel(SurfaceModel):
    def __init__(
        self,
        control_points=DEFAULT_CONTROL_POINTS,
        step=DEFAULT_STEP,
        degree_u=3,
        degree_v=3,
    ):
        super().__init__(control_points, step)
        # h/k piece of knots in the each direction must hold: h = m + p + 1 (p is the degree)

        self._m = len(self.control_polyhedron.get_control_points()) - 1
        self._n = len(self.control_polyhedron.get_control_points()[0]) - 1

        self._degree_u = degree_u  # degree in u direction
        self._degree_v = degree_v  # degree in v direction

        # onlt needed for bspline
        self._knot_u = self._generate_uniform_knot_vector(self._m + 1, self._degree_u)
        self._knot_v = self._generate_uniform_knot_vector(self._n + 1, self._degree_v)

        # if len(self._knot_u) != self._m + self._degree_u + 2:
        #     raise ValueError(f"Bad u knot vector: len(knot_u) = {len(self._knot_u)}, should be {self._m + self._degree_u + 2}")
        # if len(self._knot_v) != self._n + self._degree_v + 2:
        #     raise ValueError(f"Bad v knot vector: len(knot_v) = {len(self._knot_v)}, should be {self._n + self._degree_v+ 2}")


        # for efficiency....later it needs to be calculated frequently, when controls are added
        self._calculate_surface_points()

    def _calculate_surface_point(self, u, v):
        surface_point = np.zeros(3)

        for i in range(self._m + 1):
            for j in range(self._n + 1):
                basis_u = self._surface_function(u, i, self._degree_u, self._knot_u)
                basis_v = self._surface_function(v, j, self._degree_v, self._knot_v)

                surface_point += basis_u * basis_v * (self.control_polyhedron.get_control_points()[i][j].get_coords_numerical())

        if surface_point == np.zeros(3):
            print('u', u)
            print('v', v)


        return surface_point

    def _surface_function(self, t, index, n, knot: list[float] = []):
        """
        B-spline basis function
        t - function parameter, range -> [0, 1]
        index - index of current point
        n - degree
        knot - knot vector when calculating bsplines
        """
        epsilon = 1e-6  # Tolerance for floating-point precision

        # Base case: degree 0
        if n == 0:
            # Handle boundary case when t is very close to the last knot
            if knot[index] <= t < knot[index + 1] or (abs(t - knot[-1]) < epsilon and index == len(knot) - 2):
                return 1.0
            else:
                return 0.0

        # guard against zero divison
        if knot[index + n] == knot[index]:
            first_term = 0
        else:
            first_term = ((t - knot[index]) / (knot[index + n] - knot[index])) * \
                            self._surface_function(t, index, n - 1, knot)

        if index + 1 >= len(knot) - n:
            second_term = 0
        else:
            if knot[index + n + 1] == knot[index + 1]:
                second_term = 0
            else:
                second_term = ((knot[index + n + 1] - t) / (knot[index + n + 1] - knot[index + 1])) * \
                                self._surface_function(t, index + 1, n - 1, knot)

        return first_term + second_term

    def _generate_uniform_knot_vector(self, num_control_points, degree):
        num_knots = num_control_points + degree + 1
        knot_vector = []

        knot_vector.extend([0] * (degree + 1))

        num_internal_knots = num_knots - 2 * (degree + 1)
        for i in range(1, num_internal_knots + 1):
            knot_vector.append(i / (num_internal_knots + 1))

        knot_vector.extend([1] * (degree + 1))
        print(knot_vector)
        return knot_vector
        # n = num_control_points - 1
        # m = n + degree + 1  # Total

        # knot_vector = [0] * (degree + 1)  # Start with p+1 zeros

        # for i in range(1, m - 2 * degree):
        #     knot_vector.append(i)

        # knot_vector += [m - 2 * degree] * (degree + 1)  # End with p+1 values of m-2p

        # return knot_vector
