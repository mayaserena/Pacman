# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    discovered = set()
    fringe = util.Stack() 
    fringe.push(problem.getStartState()) 
    directions = {}
    goal_node = None
    
    while not fringe.isEmpty():
        current_node = fringe.pop()
        discovered.add(current_node)
        if (problem.isGoalState(current_node)):
            goal_node = current_node
            break
        successors = problem.getSuccessors(current_node)
        for neighbor, action, cost in successors:
            if neighbor not in discovered:
                fringe.push(neighbor)
                directions[neighbor] = current_node, action
    
    if goal_node is None:
        return []
    path = []
    current_node = goal_node
    while current_node is not problem.getStartState():
        parent, direction = directions[current_node]
        path.append(direction)
        current_node = parent
    path.reverse()

    return path
                
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    discovered = set()
    fringe = util.Queue() 
    discovered.add(problem.getStartState())
    fringe.push(problem.getStartState()) 
    directions = {}
    goal_node = None
    
    while not fringe.isEmpty():
        current_node = fringe.pop()
        if (problem.isGoalState(current_node)):
            goal_node = current_node
            break
        successors = problem.getSuccessors(current_node)
        for neighbor, action, cost in successors:
            if neighbor not in discovered:
                discovered.add(neighbor)
                fringe.push(neighbor)
                directions[neighbor] = current_node, action
    
    if goal_node is None:
        return []
    path = []
    current_node = goal_node
    while current_node is not problem.getStartState():
        parent, direction = directions[current_node]
        path.append(direction)
        current_node = parent
    path.reverse()

    return path

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    discovered = set()
    fringe = util.PriorityQueue() 
    heap = set() #keeping track of what's in the heap
    discovered.add(problem.getStartState())
    fringe.push(problem.getStartState(), 0)
    heap.add(problem.getStartState())
    directions = {}
    cost_from_start = {problem.getStartState(): 0}
    goal_node = None
    
    while not fringe.isEmpty():
        current_node = fringe.pop()
        heap.remove(current_node)
        if (problem.isGoalState(current_node)):
            goal_node = current_node
            break
        discovered.add(current_node)
        successors = problem.getSuccessors(current_node)
        for neighbor, action, cost in successors:
            total_cost = cost_from_start[current_node] + cost
            print(current_node, total_cost, neighbor)
            if neighbor not in discovered and neighbor not in heap:
                fringe.update(neighbor, total_cost)
                heap.add(neighbor)
                cost_from_start[neighbor] = total_cost
                directions[neighbor] = current_node, action
            elif neighbor in heap and cost_from_start[neighbor] > total_cost:
                fringe.update(neighbor, total_cost)
                heap.add(neighbor) 
                cost_from_start[neighbor] = total_cost
                directions[neighbor] = current_node, action
    
    if goal_node is None:
        return []
    path = []
    current_node = goal_node
    while current_node is not problem.getStartState():
        parent, direction = directions[current_node]
        path.append(direction)
        current_node = parent
    path.reverse()

    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    discovered = set()
    fringe = util.PriorityQueue() 
    heap = set() #keeping track of what's in the heap
    discovered.add(problem.getStartState())
    fringe.push(problem.getStartState(), 0)
    heap.add(problem.getStartState())
    directions = {}
    cost_from_start = {problem.getStartState(): 0}
    cost_from_nodes = {problem.getStartState(): 0}
    goal_node = None
    
    while not fringe.isEmpty():
        current_node = fringe.pop()
        heap.remove(current_node)
        if (problem.isGoalState(current_node)):
            goal_node = current_node
            break
        discovered.add(current_node)
        successors = problem.getSuccessors(current_node)
        for neighbor, action, cost in successors:
            cost_between_nodes = cost_from_nodes[current_node] + cost
            total_cost = cost_between_nodes + heuristic(neighbor, problem)
            print(current_node, cost_between_nodes, total_cost, neighbor)
            if neighbor not in discovered and neighbor not in heap:
                fringe.update(neighbor, total_cost)
                heap.add(neighbor)
                cost_from_nodes[neighbor] = cost_between_nodes
                cost_from_start[neighbor] = total_cost
                directions[neighbor] = current_node, action
            elif neighbor in heap and cost_from_start[neighbor] > total_cost:
                fringe.update(neighbor, total_cost)
                heap.add(neighbor) 
                cost_from_nodes[neighbor] = cost_between_nodes
                cost_from_start[neighbor] = total_cost
                directions[neighbor] = current_node, action
    
    if goal_node is None:
        return []
    path = []
    current_node = goal_node
    while current_node is not problem.getStartState():
        parent, direction = directions[current_node]
        path.append(direction)
        current_node = parent
    path.reverse()

    return path

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
