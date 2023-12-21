# %% [markdown]
# # A* Search Algorithm
#
# A* search is a pathfinding algorithm that is commonly used in computer science
# to find the shortest path between two points. It combines the strengths of two
# other algorithms, Dijkstra's algorithm and Greedy Best-First Search, to
# efficiently find a path that is guaranteed to be the shortest possible. The
# algorithm works by keeping track of two values for each node in the search
# space: the actual distance from the starting point to that node, and an
# estimate of the distance from that node to the goal. By using these two
# values, the algorithm can prioritize which paths to explore first and can
# quickly rule out paths that are clearly not the shortest. This allows the
# algorithm to be very efficient, especially when used on large search spaces.

# %%
import heapq

# define the graph
graph = {
    "A": {"B": 10, "C": 3},
    "B": {"D": 2},
    "C": {"D": 8, "E": 2},
    "D": {"E": 7},
    "E": {"F": 5},
    "F": {},
}


def a_star(graph, start, goal):
    # create a priority queue to store the nodes to explore
    queue = []
    heapq.heappush(queue, (0, start))

    # keep track of which nodes have been visited
    visited = set()

    # store the cost of the cheapest path to each node
    cost_so_far = {start: 0}

    # store the parent of each node in the shortest path
    parent = {start: None}

    # keep exploring nodes until we reach the goal
    while queue:
        # get the node with the lowest cost
        current = heapq.heappop(queue)[1]

        # check if we have reached the goal
        if current == goal:
            break

        # mark the current node as visited
        visited.add(current)

        # explore the neighbors of the current node
        for neighbor, cost in graph[current].items():
            # check if we have already visited this node
            if neighbor in visited:
                continue

            # calculate the cost of the path to the neighbor
            new_cost = cost_so_far[current] + cost

            # check if this is a cheaper path to the neighbor than any previous path
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                # update the cost and parent of the neighbor
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = current

                # calculate the estimated total cost of the path to the goal
                priority = new_cost + heuristic(graph[goal], graph[neighbor])

                # add the neighbor to the queue
                heapq.heappush(queue, (priority, neighbor))

    # construct the shortest path from the parent information
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()

    return path


def heuristic(goal, neighbor):
    # calculate the estimated distance to the goal using the Manhattan distance
    return abs(goal[0] - neighbor[0]) + abs(goal[1] - neighbor[1])


# %%
# find the shortest path from start to goal
start = "A"
goal = "F"
path = a_star(graph, start, goal)

print(f"The shortest path from {start} to {goal} is: {path}")

# %%
