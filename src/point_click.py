from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np
from surfaces.control_polyhedron import control_polyhedron


class RayPicker:
    def __init__(self):
        pass
        
    def pick(self, x, y, point, threshold=0.1):
        # Get matrices and viewport
        self.modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.projection = glGetDoublev(GL_PROJECTION_MATRIX)
        self.viewport = glGetIntegerv(GL_VIEWPORT)

        print(f"Modelview: {self.modelview}")
        print(f"Projection: {self.projection}")
        print(f"Viewport: {self.viewport}")
        
        # Correct y coordinate
        y = self.viewport[3] - y      

        # Get near and far points in world coordinates
        ray_near = np.array(gluUnProject(float(x), float(y), 0.0, self.modelview, self.projection, self.viewport))
        ray_far = np.array(gluUnProject(float(x), float(y), 1.0, self.modelview, self.projection, self.viewport))
        
        # Calculate ray direction
        ray_direction = ray_far - ray_near
        ray_direction = ray_direction / np.linalg.norm(ray_direction)
        
        print(f"Ray Origin: {ray_near}")
        print(f"Ray Direction: {ray_direction}")
        
        return self.ray_intersects_point(ray_near, ray_direction, point, threshold)
    
    def unproject(self, winX, winY, winZ, modelview, projection, viewport):
        # Transformation matrices
        modelview = np.array(modelview)
        projection = np.array(projection)
        viewport = np.array(viewport)

        # Compute the inverse of the combined matrix
        mvp = np.dot(projection, modelview)
        inv_mvp = np.linalg.inv(mvp)

        # Normalize window coordinates
        winX = (winX - viewport[0]) / viewport[2] * 2.0 - 1.0
        winY = (winY - viewport[1]) / viewport[3] * 2.0 - 1.0
        winZ = 2.0 * winZ - 1.0

        # Create the normalized device coordinates
        ndc = np.array([winX, winY, winZ, 1.0])

        # Transform the normalized device coordinates back to world coordinates
        obj = np.dot(inv_mvp, ndc)
        obj = obj / obj[3]

        return obj[:3]
    
    def ray_intersects_point(self, ray_origin, ray_direction, point_coords, threshold=0.1):
        # Convert point to homogeneous coordinates
        point_h = np.array([*point_coords, 1.0])
        
        # Transform point to world coordinates if it isn't already
        if np.array_equal(self.modelview, np.eye(4)):
            point_world = point_coords
        else:
            # Transform point to world space
            point_world = np.dot(self.modelview, point_h)
            point_world = point_world[:3] / point_world[3]
            
        # Vector from ray origin to point
        origin_to_point = point_world - ray_origin
        
        # Calculate the closest point on the ray to our target point
        # This uses vector projection
        t = np.dot(origin_to_point, ray_direction)
        closest_point = ray_origin + t * ray_direction
        
        # Calculate distance from point to closest point on ray
        distance = np.linalg.norm(point_world - closest_point)
        
        print(f"Point World: {point_world}")
        print(f"Distance to ray: {distance}")
        print(f"Projection distance: {t}")
        
        # Check if point is close enough to ray and in front of camera
        return distance < threshold and t > 0
    

# temporary solution
# check if the pixel is in the threshold of a rendered point
# if it is, return the distance to the point from the click
# if it is not, return None
def pick(x, y, point, threshold=3):
    # Project point to screen coordinates
    viewport = glGetIntegerv(GL_VIEWPORT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)

    # correct y coordinate
    y = viewport[3] - y

    winX, winY, winZ = gluProject(*point, modelview, projection, viewport)

    # Check if the click is within the threshold of the point
    if abs(winX - x) < threshold and abs(winY - y) < threshold:
        # Calculate the distance between the projected point and the click
        distance = np.linalg.norm([winX - x, winY - y])
        return distance
