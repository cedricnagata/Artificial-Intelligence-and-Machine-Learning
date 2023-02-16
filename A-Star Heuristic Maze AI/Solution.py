"""
Cedric Nagata
nagatac@uw.edu
CSE 473 A
Shapiro
Assignment 2

LIBRARIES USED:
- SHAPELY GEOMETRY LIBRARY (https://shapely.readthedocs.io/en/stable/installation.html)
- HEAPQ (https://docs.python.org/3/library/heapq.html)
"""

import heapq
from shapely.geometry import Polygon, LineString, Point

_start = Point # start point
_goal = Point # goal point
_num_obstacles = 0 # number of obstacles
_obstacles = [] # list of polygons for obstacles
_points = [] # list of all points

# State class for any state of environment
# 
# Fields:  
#   - point as Point object
#   - x as x coordinate
#   - y as y coordinate
#   - g_val as path g value
#   - h_val as path h value
#   - f_val as path f value
#   - parent as parent State
class State():
    # initialization method
    # 
    # arguments:
    #   - self
    #   - point for coordinates
    #   - parent state
    # return:
    #   - sets x and y coordinate 
    #   - sets g_val, h_val, and f_val
    #   - sets parent state
    def __init__(self, point, parent):
        global _goal
        
        self.point = point # set point object
        self.x = point.x # point x coordinate
        self.y = point.y # point x coordinate

        # set g value as total cost to this point
        if parent == None:
            self.g_val = 0
        else:
            self.g_val = float(parent.g_val) + self.point.distance(parent.point)
        # set h value as heuristic function result of straight line cost to goal
        self.h_val = self.point.distance(_goal)
        # set f value as overall score from g val plus h val
        self.f_val = self.g_val + self.h_val

        self.parent = parent # parent state

    # equality method
    # 
    # arguments:
    #   - self
    #   - other
    # return:
    #   - true or false based on equals criteria
    def __eq__(self, other):
        if isinstance(other, State):
            # if point and f_val are equal then true
            if self.point == other.point and self.f_val == other.f_val:
                return True
        else:
            return NotImplemented
    
    # less than method
    # 
    # arguments:
    #   - self
    #   - other
    # return:
    #   - true or false based on less than criteria
    def __lt__(self, other):
        if isinstance(other, State):
            # if f_val is less than other then true
            if self.f_val <= other.f_val:
                return True
        else:
            return NotImplemented

    # method to get all valid destination points from this state
    # that are not stopped by obstacles
    # 
    # arguments:
    #   - self
    #   - closed list of points
    # return:
    #   - list of valid destination points from current state
    def get_valid_points(self, closed_list):
        global _points
        
        valid_points = [] # return list
        new_points = _points

        # iterate through possible points
        for point in new_points:
            if point not in closed_list and point != self.point: # exclude closed list and self
                line = LineString([self.point, point]) # create line
                valid = True # initialize valid variable

                # check all obstacles
                for obstacle in _obstacles:
                    # if line crosses obstacle interior
                    if line.crosses(obstacle) or line.within(obstacle):
                        valid = False # path is not valid
                        break
                if valid == True: # add point if path is valid
                    valid_points.append(point) 
        
        return valid_points # return valid points list
    
    # method to check if current state is goal state
    # 
    # arguments:
    #   - self
    #   - goal state
    # return:
    #   - True if state is goal, False otherwise
    def is_goal_state(self, goal):
        # if self x and y coordinates match goal return true
        if (self.x == goal.x and self.y == goal.y):
            return True
        else:
            return False

# method to set up environment from file
# 
# arguments:
#   - file name
# return:
#   - sets global start point
#   - sets global goal point
#   - sets global obstacles list
#   - sets global obstacles number
#   - sets global points list
def setup_from_file (file_name):
    # globals
    global _start
    global _goal
    global _obstacles
    global _num_obstacles
    global _points
    
    # open file
    print("searching for file: " + file_name)
    file = open(file_name, 'r')
    print("file found!")

    # get start point
    start_input = [int(x) for x in file.readline().split()]
    _start = Point(start_input[0], start_input[1])

    # get goal point
    goal_input = [int(x) for x in file.readline().split()]
    _goal = Point(int(goal_input[0]), int(goal_input[1]))
    
    # get number of obstacles
    _num_obstacles = int(file.readline())

    # iterate through obstacle lines
    for i in range(_num_obstacles):        
        points_input = [int(x) for x in file.readline().split()] # get obstacle input
        points_x = []
        points_y = []
        points = []

        # iterate obstacle line input
        for j in range(len(points_input)):
            if j % 2 == 0:
                points_x.append(points_input[j]) # append x coordinate
            else:
                points_y.append(points_input[j]) # append y coordinate

        for k in range(len(points_x)): # create point objects and append
            point = Point(points_x[k], points_y[k])
            points.append(point) 
            _points.append(point)

        obstacle = Polygon([[p.x, p.y] for p in points]) # create obstacle object and append
        _obstacles.append(obstacle)

# method to search environment using A* Search
# and return shortest cost path from start point
# to goal point
# 
# arguments: none
# return:
#   - goal state with shortest cost parent path to start state
def search():
    # globals
    global _start
    global _goal
    global _obstacles
    global _num_obstacles

    print("Searching for shortest path to goal...\n")

    # set start state
    start_state = State(_start, None)
    
    open_list = [] # open list
    closed_list = [] # closed list

    heapq.heapify(open_list) # initialize open list as a priority queue
    heapq.heappush(open_list, (0, start_state)) # push start state

    # while open list not empty
    while len(open_list) != 0:
        curr_state = heapq.heappop(open_list)[1] # pop top of open list

        valid_points = curr_state.get_valid_points(closed_list) # get valid points

        for point in valid_points: # iterate valid points
            valid_state = State(point, curr_state) # create state

            if valid_state.is_goal_state(_goal): # if goal state return
                print("Goal State Reached!")
                return valid_state
            elif valid_state.point not in closed_list: # check closed list
                element = (valid_state.f_val, valid_state)
                if element not in open_list: # check open list
                    # push element on open list with f_val for search priority
                    heapq.heappush(open_list, element) 
        
        # if not already on closed list add current point
        if curr_state.point not in closed_list:
            closed_list.append(curr_state.point)

# get file and setup environment
file = input("Enter layout file to search: ")
setup_from_file(file)
print("")

# print environment
print("******ENVIRONMENT RESULTS******")
print("Start Point: " + str(_start))
print("Goal Point: " + str(_goal))
print("Number of Obstacles: " + str(_num_obstacles))
for x in range(len(_obstacles)):
    print("Obstacle "  + str(x + 1) + ": " + str(_obstacles[x]))
print("")

result = search() # get result from search

# reverse insert into path
path = []
while result != None:
    path.insert(0, result)
    result = result.parent

# print path
print("PATH:")
for i in range(len(path) - 1):
    print("   " + str(path[i].point) + " ---> " + str(path[i + 1].point) + 
          " | CUMULATIVE COST: " + str(round(path[i + 1].g_val, 3)))