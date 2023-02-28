# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** BEGIN YOUR CODE HERE ***"

        minFD = float('inf')
        
        for food in newFood.asList():
            newD = manhattanDistance(newPos, food)
            minFD = min(minFD,newD)

        minGD = float('inf')
        minG = ()
        
        for ghost in newGhostStates:
            pos = ghost.getPosition()
            newD = manhattanDistance(newPos, pos)
            minGD = min(minGD,newD)
            if minGD == newD:
                minG = ghost

        fWeight = 2**(-minFD) #decreases slower than g
        gWeight = 5**(-minGD)
        
        if minG.scaredTimer == 0: # penalty for unafraid ghosts
            gWeight *= -1
        
        score = fWeight + gWeight

        "*** END YOUR CODE HERE ***"
        # ^^^ you should return something in the above block
        
        # but by default, this is the evaluation function before you put your code in
        return successorGameState.getScore() + score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
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
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        # sourcery skip: remove-unreachable-code
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** BEGIN YOUR CODE HERE ***"

        PAC_MAN = 0
        LAST_DEPTH = self.depth-1
        NUM_AGENTS = gameState.getNumAgents()

        def minimax(state, agent, depth):
            if (depth == -1 and agent == PAC_MAN) or state.isWin() or state.isLose():
                return self.evaluationFunction(state), Directions.STOP

            nextDepth = depth-1 if agent == PAC_MAN else depth
            nextAgent = (agent+1)%NUM_AGENTS

            actions = state.getLegalActions(agent)
            successors = [state.generateSuccessor(agent, a) for a in actions]
            scores= [ minimax(s,nextAgent,nextDepth)[0] for s in successors ]

            bestS = max(scores) if agent == PAC_MAN else min(scores)
            bestSind = scores.index(bestS)
            bestA = actions[bestSind]

            return bestS, bestA

        return minimax(gameState, PAC_MAN, LAST_DEPTH)[1]

        "*** END YOUR CODE HERE ***"

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        # sourcery skip: remove-unreachable-code
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** BEGIN YOUR CODE HERE ***"
        
        PAC_MAN = 0
        LAST_DEPTH = self.depth-1
        NUM_AGENTS = gameState.getNumAgents()

        def ab_minimax(state, agent, depth, beta, alpha):
            if (depth == -1 and agent == PAC_MAN) or state.isWin() or state.isLose():
                return self.evaluationFunction(state), Directions.STOP

            nextDepth = depth-1 if agent == PAC_MAN else depth
            nextAgent = (agent+1)%NUM_AGENTS

            actions = state.getLegalActions(agent)

            v = -float("inf") if agent == PAC_MAN else float("inf")

            bestA = Directions.STOP

            def succ_generator():
                for a in actions:
                    yield (state.generateSuccessor(agent, a), a)
    
            for s, a in succ_generator():
                nextV = ab_minimax(s, nextAgent, nextDepth, beta, alpha)[0]
                
                v = max(v, nextV) if agent == PAC_MAN else min(v, nextV)

                if v == nextV: bestA = a

                prune = v>beta if agent == PAC_MAN else v<alpha

                if prune:
                    break

                if agent == PAC_MAN:
                    alpha = max(alpha, v)
                else:
                    beta = min(beta, v)

            return v, bestA

        alpha = -float("inf")
        beta = float("inf")

        return ab_minimax(gameState, PAC_MAN, LAST_DEPTH, beta, alpha)[1]
        "*** END YOUR CODE HERE ***"

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        # sourcery skip: remove-unreachable-code
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** BEGIN YOUR CODE HERE ***"
        
        PAC_MAN = 0
        LAST_DEPTH = self.depth-1
        NUM_AGENTS = gameState.getNumAgents()

        def exp_minimax(state, agent, depth):
            if (depth == -1 and agent == PAC_MAN) or state.isWin() or state.isLose():
                return self.evaluationFunction(state), Directions.STOP

            nextDepth = depth-1 if agent == PAC_MAN else depth
            nextAgent = (agent+1)%NUM_AGENTS

            actions = state.getLegalActions(agent)
            successors = [state.generateSuccessor(agent, a) for a in actions]

            scores= [ exp_minimax(s,nextAgent,nextDepth)[0] for s in successors ]

            v = 0
            bestA = Directions.STOP
            
            if agent == PAC_MAN:
                v = max(scores) 
                vInd = scores.index(v)
                bestA = actions[vInd]
            else:
                bestA = random.choice(actions)
                p = 1/len(successors)
                for score in scores:
                    # numS = successors.count(s)
                    v += p*score

            return v, bestA

        return exp_minimax(gameState, PAC_MAN, LAST_DEPTH)[1]
        "*** END YOUR CODE HERE ***"

def betterEvaluationFunction(currentGameState: GameState):
    # sourcery skip: remove-unreachable-code
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: Everything is the same as my evaluation function from question 1, except I used currentGameState instead of successorGameState and didn't involve actions.
    """
    "*** BEGIN YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    minFD = float('inf')
    
    for food in newFood.asList():
        newD = manhattanDistance(newPos, food)
        minFD = min(minFD,newD)

    minGD = float('inf')
    minG = ()
    
    for ghost in newGhostStates:
        pos = ghost.getPosition()
        newD = manhattanDistance(newPos, pos)
        minGD = min(minGD,newD)
        if minGD == newD:
            minG = ghost

    fWeight = 2**(-minFD) #decreases slower than g
    gWeight = 5**(-minGD)
    
    if minG.scaredTimer == 0: # penalty for unafraid ghosts
        gWeight *= -1
    
    score = fWeight + gWeight
    
    return currentGameState.getScore() + score
    "*** END YOUR CODE HERE ***"

# Abbreviation
better = betterEvaluationFunction
