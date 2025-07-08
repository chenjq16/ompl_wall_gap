"""
Environment for planning in a 2D grid with a wall gap.
Author: Jianqiang Chen
"""

class Env:
    def __init__(self, width=20, height=20, wall_gap=2, wall_thickness=2, wall_height=10, boundary_wall_thickness=1):
        self.x_range = (0, width)
        self.y_range = (0, height)
        self.width = width
        self.height = height
        self.wall_gap = wall_gap
        self.wall_thickness = wall_thickness
        self.wall_height = wall_height
        self.boundary_wall_thickness = boundary_wall_thickness
        self.obs_boundary = self.create_boundary()
        self.obs_wall = self.create_wall()
        self.obs_rect = []
        self.obs_circle = []

    def create_boundary(self):
        """
        Creates a boundary for the environment.
        """
        # Data format:
        # [x, y, width, height]
        # Range of x: [0, width]
        # Range of y: [0, height]
        obs_boundary = [
            [0, 0, self.boundary_wall_thickness, self.height],  # Left boundary
            [self.width - self.boundary_wall_thickness, 0, self.boundary_wall_thickness, self.height],  # Right boundary
            [0, 0, self.width, self.boundary_wall_thickness],  # Bottom boundary
            [0, self.height - self.boundary_wall_thickness, self.width, self.boundary_wall_thickness],  # Top boundary
        ]
        return obs_boundary
    
    def create_wall(self):
        """
        Creates a wall with a gap in the middle.
        """
        # Downward wall
        # Data format:
        # [x, y, width, height]
        wall_0 = [
            [self.width / 2 - self.wall_thickness / 2, 0, self.wall_thickness, self.wall_height - self.wall_gap / 2],
        ]
        # Upward wall
        wall_1 = [
            [self.width / 2 - self.wall_thickness / 2, self.wall_height + self.wall_gap / 2, self.wall_thickness, self.height - self.wall_height - self.wall_gap / 2],
        ]
        # Combine both walls
        obs_wall = wall_0 + wall_1
        return obs_wall
    
    def add_rectangles(self, x=None, y=None, width=None, height=None):
        """
        Adds rectangles to the environment.
        """
        self.obs_rect.append([x, y, width, height])

    def add_circles(self, x=None, y=None, radius=None):
        """
        Adds circles to the environment.
        """
        self.obs_circle.append([x, y, radius])

    def reset(self):
        """
        Resets the environment.
        """
        self.obs_rect = []
        self.obs_circle = []
        self.obs_boundary = self.create_boundary()
        self.obs_wall = self.create_wall()

    def get_obs_vertex(self):
        """
        Returns the vertices of the obstacles in the environment.
        """
        obs_vertex = []
        for obs in self.obs_boundary + self.obs_wall + self.obs_rect + self.obs_circle:
            if len(obs) == 4:
                x, y, w, h = obs
                obs_vertex.extend([
                    (x, y),
                    (x + w, y),
                    (x + w, y + h),
                    (x, y + h)
                ])
        return obs_vertex
    
    def get_obs(self):
        """
        Returns the obstacles in the environment.
        """
        obs = {
            "boundary": self.obs_boundary,
            "wall": self.obs_wall,
            "rect": self.obs_rect,
            "circle": self.obs_circle
        }
        return obs
    
    def get_obs_num(self):
        """
        Returns the number of obstacles in the environment.
        """
        obs_num = {
            "boundary": len(self.obs_boundary),
            "wall": len(self.obs_wall),
            "rect": len(self.obs_rect),
            "circle": len(self.obs_circle)
        }
        return obs_num
    
    def is_in_boundary(self, x, y):
        """
        Checks if a point is within the boundary of the environment.
        """
        return (self.x_range[0] <= x <= self.x_range[1]) and (self.y_range[0] <= y <= self.y_range[1])
    
    def is_in_obs_boundary(self, x, y):
        """
        Checks if a point is within the boundary obstacles.
        """
        for boundary in self.obs_boundary:
            boundary_x, boundary_y, boundary_w, boundary_h = boundary
            if boundary_x <= x <= boundary_x + boundary_w and boundary_y <= y <= boundary_y + boundary_h:
                return True
        return False

    def is_in_obs_wall(self, x, y):
        """
        Checks if a point is within any wall obstacle.
        """
        for wall in self.obs_wall:
            wall_x, wall_y, wall_w, wall_h = wall
            if wall_x <= x <= wall_x + wall_w and wall_y <= y <= wall_y + wall_h:
                return True
        return False
    
    def is_in_obs_rect(self, x, y):
        """
        Checks if a point is within any rectangle obstacle.
        """
        for rect in self.obs_rect:
            rect_x, rect_y, rect_w, rect_h = rect
            if rect_x <= x <= rect_x + rect_w and rect_y <= y <= rect_y + rect_h:
                return True
        return False
    
    def is_in_obs_circle(self, x, y):
        """
        Checks if a point is within any circle obstacle.
        """
        for circle in self.obs_circle:
            circle_x, circle_y, radius = circle
            if (x - circle_x) ** 2 + (y - circle_y) ** 2 <= radius ** 2:
                return True
        return False
    
    def is_collision(self, x, y):
        """
        Checks if a point collides with any obstacle in the environment.
        """
        return (self.is_in_obs_boundary(x, y) or
                self.is_in_obs_wall(x, y) or
                self.is_in_obs_rect(x, y) or
                self.is_in_obs_circle(x, y))


if __name__ == "__main__":
    env = Env()
    print(env.x_range[1])
    print(env.obs_boundary)
    print(env.obs_wall)
    print(env.obs_rect)
    print(env.obs_circle)
    print(env.is_collision(5, 5))  # Example collision check
