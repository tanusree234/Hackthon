import numpy as np
import matplotlib.pyplot as plt
import heapq


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(grid, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    while open_list:
        _, current = heapq.heappop(open_list)
        if current == goal:
            break
        for i, j in neighbors:
            next = (current[0] + i, current[1] + j)
            if next[0] < 0 or next[0] >= len(grid) or next[1] < 0 or next[1] >= len(grid[0]) or grid[next[0]][
                next[1]] == 1:
                continue
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                heapq.heappush(open_list, (priority, next))
                came_from[next] = current
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


# Assume we have some sensor data in a 2D numpy array
sensor_data = np.random.rand(10, 10)

# Create a 2D map from the sensor data
map_data = np.where(sensor_data > 0.5, 1, 0)

# Define the start and end points
start = (0, 0)
end = (9, 9)

# Implement a simple steering algorithm (e.g., A* pathfinding)
path = a_star(map_data, start, end)

# Display the map and the path
plt.imshow(map_data, cmap='gray')
plt.plot(*zip(*path), color='red')
plt.show()
