import numpy as np
from heapq import heappush, heappop
import math
import matplotlib.pyplot as plt
from constants.constants import Paths


def load_occupancy_map(npy_path):
    """
    Load the occupancy map from a .npy file.
    Returns a 2D numpy array where 0=free, 1=obstacle.
    """
    nav_map = np.load(npy_path)
    if len(nav_map.shape) != 2:
        raise ValueError("Occupancy map must be a 2D array.")
    return nav_map


def is_valid(x, y, nav_map):
    """
    Check if (x, y) is within bounds and not an obstacle.
    """
    h, w = nav_map.shape
    if 0 <= x < w and 0 <= y < h and nav_map[y, x] == 0:
        return True
    return False


def heuristic(a, b):
    """
    Heuristic function for A* — using Euclidean distance
    a, b are (x, y) tuples.
    """
    return math.dist(a, b)


def astar(nav_map, start, goal):
    """
    Performs A* pathfinding on the given nav_map from start to goal.
    nav_map: 2D array with 0=free, 1=obstacle
    start: (sx, sy)
    goal: (gx, gy)
    Returns: list of (x, y) from start to goal if path is found, else [].
    """
    (sx, sy) = start
    (gx, gy) = goal

    # Validate start/goal
    if not is_valid(sx, sy, nav_map):
        print("Start position is invalid or blocked.")
        return []
    if not is_valid(gx, gy, nav_map):
        print("Goal position is invalid or blocked.")
        return []

    # Data structures for A*
    open_set = []
    heappush(open_set, (0, (sx, sy)))  # (fscore, (x, y))

    came_from = {}  # to reconstruct path
    gscore = {(sx, sy): 0}
    fscore = {(sx, sy): heuristic((sx, sy), (gx, gy))}

    # 4-directional neighbors
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while open_set:
        # Pop the cell with lowest fscore
        current_f, current_pos = heappop(open_set)
        (cx, cy) = current_pos

        # If we reached the goal
        if (cx, cy) == (gx, gy):
            return reconstruct_path(came_from, current_pos)

        # Check all neighbors
        for dx, dy in neighbors:
            nx, ny = cx + dx, cy + dy
            if is_valid(nx, ny, nav_map):
                tentative_g = gscore[(cx, cy)] + 1  # cost=1 for each step
                if (nx, ny) not in gscore or tentative_g < gscore[(nx, ny)]:
                    came_from[(nx, ny)] = (cx, cy)
                    gscore[(nx, ny)] = tentative_g
                    fscore[(nx, ny)] = tentative_g + heuristic((nx, ny), (gx, gy))
                    heappush(open_set, (fscore[(nx, ny)], (nx, ny)))

    # If goal not reached
    return []


def visualize_path_matplotlib(nav_map, path, title="A* Path"):
    
    plt.imshow(nav_map, cmap="gray_r", origin="upper")
    px = [p[0] for p in path]
    py = [p[1] for p in path]
    plt.plot(px, py, color="red", linewidth=2, marker="o", markersize=2)
    plt.title(title)
    plt.gca().invert_yaxis()  # optional: flip the y-axis to match typical image coords
    plt.show()


def reconstruct_path(came_from, current):
    """
    Reconstructs path from 'came_from' dict.
    """
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def run_nav(start, goal):
    """
    start: (x1, y1)
    goal: (x2, y2)"""

    # # 3) Run A* search
    path = astar(map, start, goal)
    # path = astar(nav_map, start, goal)
    if not path:
        print("No path found.")
    else:
        visualize_path_matplotlib(map, path, title="A* Path (Matplotlib)")
        
def get_end(location:str):
    if location =="Leacock 132":
        return (791,514)
    elif location =="Elevator":
        return (478,865)
    elif location =="Leacock 132 back entrance":
        return (1284,77)
    elif location =="Arts building":
        return (1336,470)
    elif location =="Emergency":
        return (1250,629)
    return (609,817)

def get_qr(location:int):
    if location==1:
        return (684,546)
    elif location ==2:
        return (685,624)
    elif location ==3:
        return (848,551)
    elif location ==4:
        return (848, 625)
    elif location ==5:
        return (1011, 553)
    elif location ==6:
        return (1011,624)
    elif location ==7:
        return (1175,552)
    elif location ==8:
        return (1175,625)

map = load_occupancy_map(Paths.NAV_MAP)
