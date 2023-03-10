# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):  # sourcery skip: remove-unreachable-code
        # Write value iteration code here
        "*** BEGIN YOUR CODE HERE ***"
        states = self.mdp.getStates()

        for _ in range(self.iterations):
            next_vals = util.Counter()
            for s in states:
                bestA = self.getAction(s)
                next_vals[s] = 0 if bestA is None else self.getQValue(s, bestA)

            self.values = next_vals
        "*** END YOUR CODE HERE ***"

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        # sourcery skip: remove-unreachable-code
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** BEGIN YOUR CODE HERE ***"

        q = 0
        if action is not None:
            T = self.mdp.getTransitionStatesAndProbs(state, action)
            for newS, prob in T:
                R = self.mdp.getReward(state, action, newS)
                dV = self.discount*self.values[newS]
                q+= prob*(R + dV)

        return q
        "*** END YOUR CODE HERE ***"

    def computeActionFromValues(self, state):
        # sourcery skip: for-index-underscore, remove-unreachable-code
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** BEGIN YOUR CODE HERE ***"

        if self.mdp.isTerminal(state): return None
    
        actions = self.mdp.getPossibleActions(state)
        Q = util.Counter()

        for a in actions:
            Q[a] = self.getQValue(state, a)

        return Q.argMax()
        "*** END YOUR CODE HERE ***"

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        # Write value iteration code here
        "*** BEGIN YOUR CODE HERE ***"
        states = self.mdp.getStates()
        num_states = len(states)
        iter_states = [states[i%num_states] for i in range(self.iterations)]

        for s in iter_states:
            bestA = self.getAction(s)
            self.values[s] = 0 if bestA is None else self.getQValue(s, bestA)

        "*** END YOUR CODE HERE ***"

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** BEGIN YOUR CODE HERE ***"

        def updateQueue(q, lst, isPred=False):
            for s in lst:
                bestA = self.getAction(s)
                diff = abs(self.values[s] - self.getQValue(s, bestA))
                
                if (
                    (isPred and (diff > self.theta))
                    or (not isPred)
                ):
                    q.update(s,-diff)

        all_states = self.mdp.getStates()
        preds = {s: set() for s in all_states} #filter out terminal states

        for p, _ in preds.items():
            actions = self.mdp.getPossibleActions(p)
            for a in actions: 
                nextStates = self.mdp.getTransitionStatesAndProbs(p, a)

                for nextS, prob in nextStates: 
                    if prob > 0 and not self.mdp.isTerminal(nextS): 
                        preds[nextS].add(p) 

        P = util.PriorityQueue()

        updateQueue(P, preds)

        for _ in range(self.iterations):
            if P.isEmpty(): break
            s = P.pop()

            if not self.mdp.isTerminal(s):
                bestA = self.getAction(s)
                self.values[s] = self.getQValue(s, bestA)

            updateQueue(P, list(preds[s]), True)

        "*** END YOUR CODE HERE ***"
        

