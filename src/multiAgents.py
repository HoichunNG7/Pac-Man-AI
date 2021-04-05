from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        we assume ghosts act in turn after the pacman takes an action
        so your minimax tree will have multiple min layers (one for each ghost)
        for every max layer

        gameState.generateChild(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state

        self.evaluationFunction(state)
        Returns pacman SCORE in current state (useful to evaluate leaf nodes)

        self.depth
        limits your minimax tree depth (note that depth increases one means
        the pacman and all ghosts has already decide their actions)
        """
        action, _ = self.maxValue(0, gameState)
        return action

    def maxValue(self, current_depth, state):
        if current_depth == self.depth or state.isWin() or state.isLose():
            return None, self.evaluationFunction(state)

        max_value = -10000000
        legal_actions = state.getLegalActions(0)
        max_action = None

        for action in legal_actions:
            value = self.minValue(current_depth, state.generateChild(0, action), 1)
            if value > max_value:
                max_value = value
                max_action = action

        return max_action, max_value

    def minValue(self, current_depth, state, agent_idx):
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        min_value = 10000000
        legal_actions = state.getLegalActions(agent_idx)
        last_monster = True if agent_idx == state.getNumAgents() - 1 else False

        for action in legal_actions:
            if last_monster:
                _, value = self.maxValue(current_depth+1, state.generateChild(agent_idx, action))
            else:
                value = self.minValue(current_depth, state.generateChild(agent_idx, action), agent_idx+1)
            if value < min_value:
                min_value = value

        return min_value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        action, _ = self.maxValue(0, gameState, -10000000, 10000000)
        return action

    def maxValue(self, current_depth, state, alpha, beta):
        if current_depth == self.depth or state.isWin() or state.isLose():
            return None, self.evaluationFunction(state)

        max_value = -10000000
        legal_actions = state.getLegalActions(0)
        max_action = None

        for action in legal_actions:
            value = self.minValue(current_depth, state.generateChild(0, action), 1, alpha, beta)
            if value > max_value:
                max_value = value
                max_action = action
            if max_value > beta:
                return max_action, max_value

            alpha = max_value if max_value > alpha else alpha

        return max_action, max_value

    def minValue(self, current_depth, state, agent_idx, alpha, beta):
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        min_value = 10000000
        legal_actions = state.getLegalActions(agent_idx)
        last_monster = True if agent_idx == state.getNumAgents() - 1 else False

        for action in legal_actions:
            if last_monster:
                _, value = self.maxValue(current_depth+1, state.generateChild(agent_idx, action), alpha, beta)
            else:
                value = self.minValue(current_depth, state.generateChild(agent_idx, action), agent_idx+1, alpha, beta)
            if value < min_value:
                min_value = value
            if min_value < alpha:
                return min_value

            beta = min_value if min_value < beta else beta

        return min_value
