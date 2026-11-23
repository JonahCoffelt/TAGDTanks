import numpy as np
import pygame as pg
import random
import math
from game_code.cheat_prevention import *




class EnemyBullet:
    def __init__(self, x: float, y: float, direction: int) -> None:
        """
        Represents an enemy bullet.
        
        Args:
            x: the x position of the bullet (in grid units)
            y: the y position of the bullet (in grid units)
            direction: the direction of the bullet (in degrees)
        """
        self.x         : float = x
        self.y         : float = y
        self.direction : int   = direction


class Controller:
    def __init__(self) -> None:
        # Initialize state variables
        self.x              : float             = 0
        self.y              : float             = 0
        self.enemy_x        : float             = 0
        self.enemy_y        : float             = 0
        self.body_direction : int               = 0
        self.gun_direction  : int               = 0
        self.gun_ready      : bool              = False
        self.enemy_bullets  : list[EnemyBullet] = []
        self.map            : np.ndarray        = np.zeros((20, 15))
        self.dt             : float             = 0

        # Initialize action variables
        self.body_turn_action = None
        self.gun_turn_action  = None
        self.move_action      = None
        self.shoot_action     = False

        # DEFINE CUSTOM STATE VARIABLES (optional)



        # END DEFINE CUSTOM STATE VARIABLES (optional)

    def update(self):
        """
        Write your bot code here. This will be called every frame to determine the next action.

        Actions you can take (all methods have no arguments):
        - self.turn_body_clockwise()
        - self.turn_body_counter_clockwise()
        - self.turn_gun_clockwise()
        - self.turn_gun_counter_clockwise()
        - self.move_forward()
        - self.move_backward()
        - self.shoot()

        Values you can use:
        - self.x: the x position of the tank (in grid units)
        - self.y: the y position of the tank (in grid units)
        - self.enemy_x: the x position of the enemy tank (in grid units)
        - self.enemy_y: the y position of the enemy tank (in grid units)
        - self.body_direction: the current direction of the body (in degrees)
        - self.gun_direction: the current direction of the gun (in degrees)
        - self.gun_ready: whether the gun is ready to shoot (True or False)
        - self.enemy_bullets: a list of enemy bullets (see EnemyBullet class for more information)
        - self.map: the current map (a 20x15 numpy array, where map[x][y] == True if there is a wall, False otherwise)
        - self.dt: the time since the last frame (in seconds)
        - self.tile_x: the x tile of the tank (in grid units)
        - self.tile_y: the y tile of the tank (in grid units)
        
        Helper functions you can use:
        - raycast(): shoot a ray from the tank's barrel and retrieve the hit position.
            this can be helpful for testing hits on walls

        Notes:
            - Tank and body directions are independent. Turning the body will not affect the gun direction.

            - You cannot set your own properties, or the properties of the enemy or bullets. You can only set the action variables.
                For example:
                    self.x = 10  # WILL NOT WORK
                Use:
                    self.move_forward()  # Instead
        
            - If your code throws an error, it will be caught and your tank will be killed.

            - We will look at your code, dont cheat
        """

        # START YOUR CODE HERE
        
        self.shoot()
        # Define the grid (1 for unblocked, 0 for blocked)
        grid = list(self.map)
    
        # Define the source and destination
        src = [int(self.x),int(self.y)]
        dest = [int(self.enemy_x),int(self.enemy_y)]
    
        # Run the A* search algorithm
        a_star_search(grid, src, dest)
        
        if(random.random()*10 > 5):
            self.turn_body_clockwise() 
            self.turn_gun_clockwise() 
        else:
            self.turn_body_counter_clockwise() 
            self.turn_gun_counter_clockwise() 
        self.move_forward()
        
        '''
        'shooting function'
        
        'self.turn_body_clockwise()'
        target_dir = math.degrees(math.acos((self.x * self.enemy_x + self.y * self.enemy_y)/(math.sqrt(self.x * self.x + self.y * self.y) * math.sqrt(self.enemy_x * self.enemy_x + self.enemy_y * self.enemy_y))))
        print(target_dir - (-self.body_direction % 360))
        if(((180 + self.body_direction) % 360) > target_dir):
            self.turn_body_counter_clockwise()
        elif(((180 + self.body_direction) % 360) < target_dir):
            self.turn_body_clockwise()
            self.turn_body_clockwise() 
        pos = self.raycast()
        newPosX =  pos[0] + self.enemy_x
        newPosY =  pos[1] + self.enemy_y
        '''
        
        

        # END YOUR CODE HERE


    def turn_body_clockwise(self): 
        self.body_turn_action = "clockwise"

    def turn_body_counter_clockwise(self):
        self.body_turn_action = "counter_clockwise"
    
    def stop_turn_body(self):
        self.body_turn_action = None

    def turn_gun_clockwise(self):
        self.gun_turn_action = "clockwise"

    def turn_gun_counter_clockwise(self):
        self.gun_turn_action = "counter_clockwise"

    def stop_turn_gun(self):
        self.gun_turn_action = None

    def move_forward(self):
        self.move_action = "forward"

    def move_backward(self):
        self.move_action = "backward"

    def stop_move(self):
        self.move_action = None

    def shoot(self):
        self.shoot_action = True
        
    # ------------------------------------------------------------  
    # Helpful function Alert :O vvvvvv
    # ------------------------------------------------------------  
        
    def raycast(self) -> tuple[float, float] | None:
        """
        Shoot a ray from the tank's barrel and retrieve the hit position. 

        Returns:
            tuple[float, float]: The coordinate of the raycast hit.
            None: If no hit.
        """
        # walk the ray tile by tile
        # and anything outside the map counts as a wall
        dx = np.cos(np.deg2rad(self.gun_direction))
        dy = np.sin(np.deg2rad(self.gun_direction))

        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1

        # ray distance needed to cross one whole tile
        delta_x = abs(1 / dx) if dx != 0 else np.inf
        delta_y = abs(1 / dy) if dy != 0 else np.inf

        # ray distance to the first tile boundary
        tile_x, tile_y = self.tile_x, self.tile_y
        next_x = (tile_x + (step_x > 0) - self.x) / dx if dx != 0 else np.inf
        next_y = (tile_y + (step_y > 0) - self.y) / dy if dy != 0 else np.inf

        t = 0.0
        while 0 <= tile_x < self.map.shape[0] and 0 <= tile_y < self.map.shape[1] and not self.map[tile_x][tile_y]:
            if next_x < next_y:
                t, next_x = next_x, next_x + delta_x
                tile_x += step_x
            else:
                t, next_y = next_y, next_y + delta_y
                tile_y += step_y

        return (float(self.x + dx * t), float(self.y + dy * t))
    
    @property
    def tile_x(self) -> int:
        return int(np.floor(self.x))
    
    @property
    def tile_y(self) -> int:
        return int(np.floor(self.y))



# Define the Cell class
class Cell:
    def __init__(self):
        self.parent_i = 0  # Parent cell's row index
        self.parent_j = 0  # Parent cell's column index
        self.f = float('inf')  # Total cost of the cell (g + h)
        self.g = float('inf')  # Cost from start to this cell
        self.h = 0  # Heuristic cost from this cell to destination


# Define the size of the grid
ROW = 20
COL = 15

# Check if a cell is valid (within the grid)
def is_valid(row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL)

# Check if a cell is unblocked
def is_unblocked(grid, row, col):
    return grid[row][col] > 0

# Check if a cell is the destination
def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(row, col, dest):
    return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

# Trace the path from source to destination
def trace_path(cell_details, dest):
    path = []
    row = dest[0]
    col = dest[1]

    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    # Add the source cell to the path
    path.append((row, col))
    # Reverse the path to get the path from source to destination
    path.reverse()

# Implement the A* search algorithm
def a_star_search(grid, src, dest):
    # Check if the source and destination are valid
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        return

    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        return

    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        return

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    # Initialize the start cell details
    i = src[0]
    j = src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # For each direction, check the successors
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # If the successor is valid, unblocked, and not visited
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    # Trace and print the path from source to destination
                    trace_path(cell_details, dest)
                    found_dest = True
                    return
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j