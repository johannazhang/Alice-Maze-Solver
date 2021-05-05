import sys


# FUNCTIONS
def adj_list(maze, step) -> dict:
    """
    Return the adjacency list of the given maze according to the given step size
    """
    AL = {}  # initialize empty adjacency list
    for cell in maze:
        row = cell[0]            # row of cell
        col = cell[1]            # column of cell
        node = (step, row, col)  # node in the adjacency list
        AL[node] = []

        # iterate through the paths of each cell in the given maze,
        # and update AL
        for path in maze[cell]:
            if path == "north":
                AL[node].append((step, row - step, col))
            elif path == "east":
                AL[node].append((step, row, col + step))
            elif path == "south":
                AL[node].append((step, row + step, col))
            elif path == "west":
                AL[node].append((step, row, col - step))
            elif path == "northeast":
                AL[node].append((step, row - step, col + step))
            elif path == "southeast":
                AL[node].append((step, row + step, col + step))
            elif path == "southwest":
                AL[node].append((step, row + step, col - step))
            elif path == "northwest":
                AL[node].append((step, row - step, col - step))
    return AL


def get_distance(maze, step) -> dict:
    """
    Return the distance values of the nodes representing the given maze
    with the given step size
    """
    distance = {}
    for cell in maze:
        node = (step, cell[0], cell[1])
        distance[node] = "inf"
    return distance


def get_parent(maze, step) -> dict:
    """
    Return the parent values of the nodes representing the given maze
    with the given step size
    """
    parent = {}
    for cell in maze:
        node = (step, cell[0], cell[1])
        parent[node] = "nil"
    return parent


def get_colour(maze, step) -> dict:
    """
    Return the arrow colour values of the nodes representing the given maze
    with the given step size
    """
    colour = {}
    for cell in maze:
        node = (step, cell[0], cell[1])
        colour[node] = cell[2]
    return colour


def alice_path(maze, start, goal) -> tuple:
    """
    Return the solution path and its length of the given Alice Maze.
    If no solution exists, return "no solution".
    """
    visited = []  # keep track of visited nodes
    queue = []    # initialize queue

    steps = [1]                         # keep track of step sizes encountered
    maze_graph = adj_list(maze, 1)      # adjacency list of maze with step = 1
    distance = get_distance(maze, 1)    # distance of nodes with step = 1
    parent = get_parent(maze, 1)        # parent of nodes with step = 1
    colour = get_colour(maze, 1)        # colour of nodes with step = 1

    s = (1, start[0], start[1])         # start cell
    distance[s] = 0                     # set distance of start cell to 0
    visited.append(s)                   # append s to visited
    queue.append(s)                     # add s to queue

    success = 0                         # initialize success status

    while queue and success == 0:
        s = queue.pop(0)                # pop s off queue
        step = s[0]                     # step size is s[0]
        if colour[s] == "red":          # increment step if colour is red
            step += 1
        elif colour[s] == "yellow":     # decrement step if colour is yellow
            step -= 1

        if step != 0:
            if step not in steps:       # check if step has been encountered
                steps.append(step)
                maze_graph.update(adj_list(maze, step))     # update maze AL
                distance.update(get_distance(maze, step))   # update distance
                parent.update(get_parent(maze, step))       # update parent
                colour.update(get_colour(maze, step))       # update colour

            for neighbour in maze_graph[(step, s[1], s[2])]:
                # check that node is valid and has not been visited
                if neighbour in maze_graph and neighbour not in visited:
                    visited.append(neighbour)
                    distance[neighbour] = distance[s] + 1   # update distance
                    parent[neighbour] = s                   # update parent
                    queue.append(neighbour)
                    # check if we've reached our goal
                    if (neighbour[1], neighbour[2]) == goal:
                        success = neighbour

    # trace solution path if it exists, and return the path and its length
    if success == 0:
        return "no solution"
    path = []
    curr = success
    while distance[curr] != 0:
        path.insert(0, curr[1:])
        curr = parent[curr]
    path.insert(0, curr[1:])
    length = len(path) - 1
    return length, path


# SET UP MAZE
# reminder to put file name
if len(sys.argv) != 2:
    print("Usage: python3 Alice.py <inputfilename>")
    sys.exit()

# open file whose name is given as the first argument
f = open(sys.argv[1])

# parse file and set up alice_maze
lines = f.readlines()

# alice_path parameters
alice_maze = {}
start = tuple(map(int, lines[0].split(', ')))
goal = tuple(map(int, lines[1].split(', ')))

for line in lines[2:]:
    cell = line.strip().split(', ')
    row = int(cell[0])
    col = int(cell[1])
    colour = cell[2]
    paths = cell[3:]
    alice_maze[(row, col, colour)] = paths


# EXECUTE ALGORITHM
print(alice_path(alice_maze, start, goal))
