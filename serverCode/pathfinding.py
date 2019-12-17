class Node:
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


class PathFinder:
    def __init__(self, spaces, roads):
        self.distanceBetweenTags = 100  # in centimeters
        self.grid = []
        self.generateGrid(spaces, roads)

    def generateGrid(self, spaces, roads):
        # find out max values for grid (making use of spaces + roads)
        biggestY = 0
        biggestX = 0
        for tag, (y, x) in spaces + roads:
            if y > biggestY:
                biggestY = y
            if x > biggestX:
                biggestX = x
        # generate fresh grid
        self.grid = []
        for y in range(biggestY + 1):
            self.grid.append([])
            for x in range(biggestX + 1):
                self.grid[y].append(1)
        # add roads to existing grid
        for _, (y, x) in roads:
            self.grid[y][x] = 0

    def setDestitinationInGrid(self, grid, *coordinates):
        for (y, x) in coordinates:
            grid[y][x] = 0
        return grid

    def generateAStarPath(self, grid, beginCoordinates, endCoordinates):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""

        # Create start and end node
        start_node = Node(None, beginCoordinates)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, endCoordinates)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]  # Return reversed path

            # Generate children
            children = []
            # Adjacent squares (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), ]:

                # Get node position
                node_position = (
                    current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(grid) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(grid[len(grid) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if grid[node_position[0]][node_position[1]] > 0:
                    continue
                """
                knal hier parking idtjes erin
                work voor later: 
                        1.vindt index (cordinaat) via de index methode eg= grid.index("d2")
                        gooi 1 in de bovenstaande if
                        geef die route 
                """

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) **
                           2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

    def assignDirectionsToPath(self, path, prevCor=None):
        if prevCor is None:
            prevCor = []
        direction = ''
        directions = []
        for index, (y, x) in enumerate(path):
            if prevCor and index + 1 < len(path):
                if x == path[index + 1][1]:
                    if x == prevCor[1]:
                        if path[index + 1] == prevCor:
                            direction = 'A'
                        else:
                            direction = 'V'
                    elif x < prevCor[1]:
                        direction = 'R'
                    else:
                        direction = 'L'
                elif y == path[index + 1][0]:
                    if y == prevCor[0]:
                        direction = 'V'
                    elif y < prevCor[0]:
                        direction = 'R'
                    else:
                        direction = 'L'
                directions.append(direction)
            prevCor = (y, x)
        return self.specifyDirections(directions)

    def specifyDirections(self, directions):
        specificDirections = []
        distanceTillTurn = self.distanceBetweenTags
        for direction in directions:
            if direction == 'V':
                distanceTillTurn += self.distanceBetweenTags
            else:
                specificDirections.append(str(distanceTillTurn) + direction)
                distanceTillTurn = self.distanceBetweenTags
        if not specificDirections:
            specificDirections.append(str(distanceTillTurn) + directions[-1])
        specificDirections.append('arrived')
        return specificDirections

    def getPath(self, beginCoordinates, endCoordinates, prevCoordinates, entryCoordinates):
        print(beginCoordinates, endCoordinates, prevCoordinates, entryCoordinates)
        if entryCoordinates:
            print('using entryCoordinates')
            grid = self.setDestitinationInGrid(self.grid, beginCoordinates, entryCoordinates)
            self.printGrid(grid)
            generatedPath = self.generateAStarPath(grid, beginCoordinates, entryCoordinates)
            generatedPath.append(endCoordinates)
        else:
            grid = self.setDestitinationInGrid(self.grid, beginCoordinates, endCoordinates)
            self.printGrid(grid)
            generatedPath = self.generateAStarPath(grid, beginCoordinates, endCoordinates)

        pathModifiedWithDirections = self.assignDirectionsToPath(generatedPath, prevCoordinates)
        return [generatedPath, pathModifiedWithDirections]

    def printGrid(self, grid):
        print('Currently used grid:')
        for i in grid:
            print(i)
        print()


def main():
    start = (0, 1)
    end = (0, 4)
    prevTag = (1, 1)

    parkingSpaces = [('tag15', (4, 0)), ('tag16', (3, 0)), ('tag17', (2, 0)), ('tag18', (1, 0)), ('tag19', (0, 1)),
                     ('tag20', (0, 2)), ('tag21', (0, 3)), ('tag22', (1, 5)), ('tag23', (2, 5)), ('tag24', (3, 5)),
                     ('tag25', (4, 5)), ('tag26', (5, 4)), ('tag27', (5, 3)), ('tag28', (5, 2)), ('tag29', (2, 2)),
                     ('tag30', (2, 3)), ('tag31', (3, 2)), ('tag32', (3, 3))]

    parkingRoads = [('tag01', (5, 1)), ('tag02', (4, 1)), ('tag03', (3, 1)), ('tag04', (2, 1)), ('tag05', (1, 1)),
                    ('tag06', (1, 2)),
                    ('tag07', (1, 3)), ('tag08', (1, 4)), ('tag09', (0, 4)), ('tag10', (2, 4)), ('tag11', (3, 4)),
                    ('tag12', (4, 4)),
                    ('tag13', (4, 3)), ('tag14', (4, 2))]

    pathFinder = PathFinder(parkingSpaces, parkingRoads)
    path = pathFinder.getPath(start, end, prevTag, '')
    print('Path:', path)


if __name__ == '__main__':
    main()