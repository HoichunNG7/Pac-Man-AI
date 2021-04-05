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

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    explored_set = set()
    frontier = Stack()
    frontier.push((problem.getStartState(), list()))
    explored_set.add(problem.getStartState())

    while True:
        if frontier.isEmpty():
            return []
        current_node, current_solution = frontier.pop()
        if problem.isGoalState(current_node):
            return current_solution

        # print('current node: ', current_node)
        for triple in problem.expand(current_node):
            if triple[0] not in explored_set:
                explored_set.add(triple[0])
                solution = current_solution.copy()
                solution.append(triple[1])
                frontier.push((triple[0], solution))


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    explored_set = set()
    frontier = Queue()
    frontier.push((problem.getStartState(), list()))
    explored_set.add(problem.getStartState())

    while True:
        if frontier.isEmpty():
            return []
        current_node, current_solution = frontier.pop()
        if problem.isGoalState(current_node):
            return current_solution

        for triple in problem.expand(current_node):
            if triple[0] not in explored_set:
                explored_set.add(triple[0])
                solution = current_solution.copy()
                solution.append(triple[1])
                frontier.push((triple[0], solution))


def nullHeuristic(state, problem=None):
    """
    A example of heuristic function which estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial. You don't need to edit this function
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    explored_set = set()
    frontier_set = set()  # Track every node that is currently in frontier
    node_info = dict()  # Store tuples consisting of the action sequence of a node and its backward cost
    frontier = PriorityQueue()

    start_state = problem.getStartState()
    frontier.push(start_state, 0 + heuristic(start_state, problem))
    frontier_set.add(start_state)
    node_info[start_state] = (list(), 0)

    while True:
        if frontier.isEmpty():
            return []
        current_node = frontier.pop()
        frontier_set.remove(current_node)
        current_solution, current_path_cost = node_info[current_node]
        if problem.isGoalState(current_node):
            return current_solution
        explored_set.add(current_node)
        # print(current_node)
        # print('Explored:', explored_set)

        for triple in problem.expand(current_node):
            solution = current_solution.copy()
            solution.append(triple[1])
            path_cost = current_path_cost + triple[2]
            priority = path_cost + heuristic(triple[0], problem)

            new_child = triple[0]
            if new_child not in explored_set and new_child not in frontier_set:
                frontier.push(new_child, priority)
                frontier_set.add(new_child)
                node_info[new_child] = (solution, path_cost)
            elif new_child in frontier_set:
                frontier.update(new_child, priority)
                _, old_path_cost = node_info[new_child]
                if path_cost < old_path_cost:
                    node_info[new_child] = (solution, path_cost)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch