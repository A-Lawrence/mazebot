from pprint import PrettyPrinter
from queue import PriorityQueue
import math, json, requests
from mazebot import *

pp = PrettyPrinter(depth=3, width=120)

BASE_URL = "https://api.noopschallenge.com"

######## Race Login
loginResponse = requests.post("%s/mazebot/race/start" % BASE_URL, json = {"login":"A-Lawrence"})

loginResponseData = loginResponse.json()

nextMazeURL = loginResponseData['nextMaze']

######## Handle Mazes
count = 1
while nextMazeURL != None:
    print("****MAZE %d****" % count)
    mazeRequestUrl = "%s%s" % (BASE_URL, nextMazeURL)
    mazeResponse = requests.get(mazeRequestUrl)

    data = mazeResponse.json()

    maze = {
        "data":data['map'],
        "start": (data['startingPosition'][0], data['startingPosition'][1]),
        "end": (data['endingPosition'][0], data['endingPosition'][1]),
        "graph": {},
        "journey": [],
        "compass": []
    }

    submissionURL = data['mazePath']

    maze['graph'] = importMazeRawToMazeGraph(maze)

    maze['graph'] = removeSingleTraversals(maze)

    maze['journey'], maze['compass'] = routeFinder(maze)

    submissionResponse = requests.post("%s%s" % (BASE_URL, submissionURL), json = {"directions": ''.join(maze['compass'])})
    submissionResponseData = submissionResponse.json()

    if submissionResponseData['result'] == 'finished':
        break

    print("Result:\t\t%s" % (submissionResponseData['result']))
    print("Speed:\t\t%f" % (submissionResponseData['elapsed']/1000))
    print("Shortest:\t%r" % (submissionResponseData['shortestSolutionLength'] == submissionResponseData['yourSolutionLength']))
    print("Next Maze:\t%s" % submissionResponseData['nextMaze'])

    nextMazeURL = submissionResponseData['nextMaze']
    count = count + 1

pp.pprint(submissionResponseData)
