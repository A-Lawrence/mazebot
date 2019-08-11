from pprint import PrettyPrinter
from queue import PriorityQueue
import math

DEBUG = False

def debug(output):
    if DEBUG:
        print(output)
        
    return

def importMazeRawToMazeGraph(maze):
    mazeGraph = {}
    
    for y, row in enumerate(maze['data']):
        for x, cell in enumerate(row):
            if cell == 'X':
                continue

            # Empty array for this node.
            mazeGraph[(x, y)] = []
            
            # Can we traverse north?
            if y > 0 and maze['data'][y-1][x] != 'X':
                mazeGraph[(x, y)].append((x, y-1))

            # Can we traverse east?
            if x < len(row)-1 and maze['data'][y][x+1] != 'X':
                mazeGraph[(x, y)].append((x+1, y))

            # Can we traverse south?
            if y < len(maze['data'])-1 and maze['data'][y+1][x] != 'X':
                mazeGraph[(x, y)].append((x, y+1))

            # Can we traverse west?
            if x > 0 and maze['data'][y][x-1] != 'X':
                mazeGraph[(x, y)].append((x-1, y))

    return mazeGraph

def removeSingleTraversals(maze):
    changesMade = False
    graphWithRemovals = dict(maze['graph'])
    removedNodes = []
    
    for (x, y), traversals in maze['graph'].items():
        # We don't want to remove the start/end position if a dead end.
        if (x, y) in [maze['start'], maze['end']]:
            continue;
        
        if len(traversals) <=1 :
            changesMade = True
            del graphWithRemovals[(x,y)]
            removedNodes.append((x, y))

    for (x, y), traversals in maze['graph'].items():
        for (xt, yt) in traversals:
            if (xt, yt) in removedNodes:
                traversals.remove((xt, yt))

    if changesMade:
        maze['graph'] = graphWithRemovals
        graphWithRemovals = removeSingleTraversals(maze)
    
    return graphWithRemovals

def getCompassDirection(start, end):
    (startX, startY) = start
    (endX, endY) = end
    
    if endY < startY:
        return "N"
    
    if startX < endX:
        return "E"

    if startY < endY:
        return "S"

    if endX < startX:
        return "W"

    return "X"

def calculateDistance(start, end):
    (startX, startY) = start
    (endX, endY) = end

    return math.sqrt((endX - startX)**2 + (endY + startY)**2)

def isQueued(q, position):
   return position in (item[1] for item in q.queue)

def routeFinder(maze):
    q = PriorityQueue()
    distances = {}
    previous = {}
    heuristic = {}
    visited = [maze['start']]

    q.put((0, maze['start']))

    for index, position in enumerate(maze['graph'].keys()):
        distances[position] = math.inf
        previous[position] = None

    while not q.empty():
        priority, current = q.get()
        debug("Fetched %s, with priority %f" % (current, priority))

        if current == maze['end']:
            break

        if not current in maze['graph']:
            continue

        visited.append(current)

        for neighbour in maze['graph'][current]:
            debug("\tConsider neighbour node (%d, %d)" % (neighbour))
            
            if neighbour in visited:
                debug("\t\tWas found in recently visited.")
                continue

            debug("\t\tInitial Distance %f." % (distances[current]))
            
            if distances[current] == math.inf:
                altDist = 1
            else:
                altDist = distances[current] + 1

            debug("\t\tAlternative Distance %f." % (altDist))
            
            if not neighbour in distances or altDist < distances[neighbour]:
                debug("\t\t%f < %f." % (altDist, distances[current]))
                
                distances[neighbour] = altDist
                previous[neighbour] = current

                est = altDist + calculateDistance(neighbour, maze['end'])

                if not isQueued(q, neighbour):
                    q.put((est, neighbour))

                debug("\t\tDistance: %s = %f" % (neighbour, altDist))
                debug("\t\tPrevious: %s = %s" % (neighbour, current))
                debug("\t\tWeight: %s = %f" % (neighbour, est))
    
    journey = []
    compass = []
    cur = maze['end']
    prev = previous[maze['end']]

    while prev != None:
        journey.append(prev)
        compass.append(getCompassDirection(prev, cur))
        cur = prev
        prev = previous[prev]

    journey.reverse()
    compass.reverse()

    return journey, compass

def mazeDisplay(maze):
    mazeDisplay = []
    for y, row in enumerate(maze['data']):
        mazeDisplay.append([])
        for x, cell in enumerate(row):
            if (x, y) == maze['start']:
                mazeDisplay[y].append('A')
            elif (x, y) == maze['end']:
                mazeDisplay[y].append('B')
            elif (len(maze['journey']) > 0 and (x, y) in maze['journey']) or (len(maze['journey']) == 0 and (x, y) in maze['graph']):
                mazeDisplay[y].append(' ')
            else:
                mazeDisplay[y].append('X')
    
    return mazeDisplay
