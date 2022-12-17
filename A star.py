from warnings import warn
import heapq
import pygame


class Node:
    # Opretter node class til A* algoritme pathfinding

    def __init__(self, parent=None, position=None):
        # Parent node er den forrige node, altså den tættere på start node
        self.parent = parent
        self.position = position

        # Tre værdier for node:
        # g = afstand fra node til start
        # h = estimeret afstand til slut. Der skal bruges pythagoras til dette
        # f = g + h
        # Skal beregnes hver gang en ny node oprettes!!!

        self.g = 0
        self.h = 0
        self.f = 0


# Her bliver der kaldt to objekter der bliver sammenlignet hvor der bliver returned true hvis de er og falls hvis ikke de er equal.
    def __eq__(self, other):
        return self.position == other.position


# Her bliver der brugt __repr__ til at returne objektet i string format hvor:
    # self.position er selve objektet
    # self.g, self.h, self.f er forskellige variabler der hører til self.position.
    def __repr__(self):
        return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # Her defineres mindre end formålet for Heap queue
    def __lt__(self, other):
        return self.f < other.f

    # Her defineres større end formålet for Heap queue
    def __gt__(self, other):
        return self.f > other.f

# Her bliver der lavet en tom liste hvor current bliver sat til current_node og går ind i et loop
# Hvor der så bliver returned den reversed path til sidst.
def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end, allow_diagonal_movement=True):
    # A* search algorithm
    """
    Dette er astar funktionen som der finder den hurtigste vej til den node man vil hen til ved brug af:
    :param maze:
    :param start:
    :param end:
    :return:
    """

    # Her bliver der initialized start og end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize både open og closed list
    open_list = []
    closed_list = []

    # Her bliver der heapify open_list og added start_node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # Tilføjet en stop variabel
    outer_iterations = 0
    max_iterations = 100000

    # Her bliver der defineret to variabler der svarer til tuples hvor koordinaterne svarer til:
    # Højre, venstre, top og bund
    # hvor der er koordinater for både adjacent_squares og diagonal_squares.
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Her bliver der kørt et loop indtil man finder slutpunkt.
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
            # Hvis vi rammer dette punkt returner stien, som den er.
            # Den vil ikke indeholde destinationen.
            warn("giving up on pathfinding too many iterations")
            return return_path(current_node)

            # Hent den aktuelle node.
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # Fundet målet og returner node.
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []

        for new_position in adjacent_squares:  # Adjacent squares

            # Få den aktuelle position.
            # Koden beregner den absolute position af den nye node.
            # Hvor den adder de tilsvarende koordinater af den nuværende node.
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Her bliver der sikret at det er inde for rækkevidde.
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            # Her bliver der sikret at et er et terræn der kan tilgås, altså uden forhindringer.
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Dannelse af ny node.
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            # Child er på closed_list så vil den fortsætte.
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Dannelse af f, g, og h variabler.
            child.g = current_node.g + (((child.position[0] - child.parent.position[0]) ** 2) + (
                        (child.position[1] - child.parent.position[1]) ** 2)) ** 0.5
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + (
                        (child.position[1] - end_node.position[1]) ** 2)) ** 0.5
            child.f = child.g + child.h

            # Hvis child allerede er på open_list
            if child in open_list:
                idx = open_list.index(child)
                if child.g < open_list[idx].g:
                    # Opdater noden i open_list.
                    open_list[idx].g = child.g
                    open_list[idx].f = child.f
                    open_list[idx].h = child.h
            else:
                # Add child til open_list.
                heapq.heappush(open_list, child)

            # Add child til open_list.
            heapq.heappush(open_list, child)

    warn("Couldn't get a path to destination")
    return None


def example(print_maze=True):
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ],
            [0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, ],
            [0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, ],
            [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, ],
            [0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, ],
            [0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, ],
            [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, ],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, ],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, ]]

    start = (0, 0)
    end = (12,4)

    path = astar(maze, start, end)

# Her bliver der lavet en visuel 2D tegning af matricen hvor den illustrerer via en linje.
    # Hvor der bliver defineret farvekode og printet ruten til sidst af labyrinten.
    if print_maze:
        for step in path:
            maze[step[0]][step[1]] = 2

        for row in maze:
            line = []
            for col in row:
                if col == 1:
                    line.append("\u2588")
                elif col == 0:
                    line.append(" ")
                elif col == 2:
                    line.append(".")
            print("".join(line))

    print(path)

    # I denne sektion er det koden til illustrationen af algoritmen der finder vej gennem labyrinten.
    # Hvor der bliver brugt Pygame til at illustrerer det.
    # Definerer størrelsen på vinduet.
    WINDOW_SIZE = (1000, 1000)

    # Skaber vinduet.
    window = pygame.display.set_mode(WINDOW_SIZE)

    # Sæt baggrundsfarven til hvid.
    window.fill((255, 255, 255))
    # Definere størrelsen af hver celle i labyrinten.
    CELL_SIZE = 25

    # Tegne labyrinten.
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 1:
                # Tegne et sort rektangel til en væg.
                pygame.draw.rect(window, (0, 0, 0), (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                # Tegne et hvidt rektangel for et acceptabelt rum.
                pygame.draw.rect(window, (255, 255, 255), (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                if (i, j) in path:
                    # Beregn x- og y-positionerne af cellen til brug i tegning af kurveceller. ?`?????????????????????????????????????????????????????????????????
                    x = j * CELL_SIZE
                    y = i * CELL_SIZE
                    pygame.draw.rect(window, (255,0,0), (x, y, CELL_SIZE, CELL_SIZE))




    # Opdatere displayet.
    pygame.display.update()

    # run the Pygame loop.
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == '__main__':
    example()