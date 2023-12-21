# %% [markdown]
#
# # Dijkstra's algorithm
#
# Dijkstra's algorithm is a pathfinding algorithm that is used to find the
# shortest path between two points in a graph. It works by starting at the
# starting point and exploring all of the neighboring nodes, keeping track of
# the total cost of the path from the starting point to each node. As the
# algorithm explores each node, it updates the cost of the path to that node if
# it finds a cheaper path than any previous path. This process is repeated until
# the algorithm reaches the goal node.
#
# The key feature of Dijkstra's algorithm is that it is guaranteed to find the
# shortest path, as long as the graph does not contain any negative-cost edges.
# This makes it very useful for many applications, such as routing in networking
# and navigation in video games.
#
# Here is a simple implementation of Dijkstra's algorithm in Python:

# %%
import heapq

# define the graph
graph = {
    "A": {"B": 5, "C": 1},
    "B": {"A": 5, "C": 2, "D": 1},
    "C": {"A": 1, "B": 2, "D": 4, "E": 8},
    "D": {"B": 1, "C": 4, "E": 3, "F": 6},
    "E": {"C": 8, "D": 3},
    "F": {"D": 6},
}


def dijkstra(graph, start, goal):
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

                # add the neighbor to the queue
                heapq.heappush(queue, (new_cost, neighbor))

    # construct the shortest path from the parent information
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()

    return path


# find the shortest path from start to goal
start = "A"
goal = "F"
path = dijkstra(graph, start, goal)
print(path)
