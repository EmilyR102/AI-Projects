# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9
    answerNoise = 0.001
    return answerDiscount, answerNoise


#look at lecture 8 and 7 examples
#high discount => higher preference for closer rewards or rewards that have higher value after discount 
#low noise -> less exploration so sticking with a policy
#high living reward -> very low chance of moving into a terminal state or dead end

#Prefer the close exit (+1), risking the cliff (-10)
def question3a():
    answerDiscount = .1
    answerNoise = .001
    answerLivingReward = .01
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

#Prefer the close exit (+1), but avoiding the cliff (-10)
def question3b():
    answerDiscount = .1
    answerNoise = .001
    answerLivingReward = .6
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

#Prefer the distant exit (+10), risking the cliff (-10)
def question3c():
    answerDiscount = .9
    answerNoise = .001
    answerLivingReward = .001
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

#Prefer the distant exit (+10), avoiding the cliff (-10)
def question3d():
    answerDiscount = .9
    answerNoise = .02
    answerLivingReward = .7
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

#Avoid both exits and the cliff (so an episode should never terminate)
def question3e():
    answerDiscount = 1
    answerNoise = 1
    answerLivingReward = 1
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question8():
    answerEpsilon = 0
    answerLearningRate = 1
    return "NOT POSSIBLE"
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))
