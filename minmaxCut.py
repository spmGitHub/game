from stack import Stack
from board import Board
from copy import deepcopy
from time import localtime


def minmax(player,state, score1, score2):

    d = 6  # definition of depth of search
    s = 12 # enter here the number of holes per player. Finally set to: 12


    current_time = localtime()  # set timer for calculation
    start = current_time.tm_sec
    end=(start+8)%60


    nodeStack=Stack()
    orig=Board(state, score1, score2)
    nodeStack.push(orig)


    if (player==1):
        maxMoves=s
        minMoves=s*2
    else:
        maxMoves=2*s
        minMoves=s

    ## evalFunctions
    def evalFunction(state):
        if (player==1):
            delta = state.score1 - state.score2
        else:
            delta = state.score2 - state.score1
        return delta

    
    # when to stop going down in tree, returns true or false
    def cutOff(state):
        current_time2=localtime()
        if (nodeStack.size() == d or state.endGame or current_time2.tm_sec > end):  # stop when depth-level reached, or game over, or taking too much time
            return True
        else:
            return False

    # update state and create new child
    def updateState(board,move, player):
        tempBoard = Board(board.bins, board.score1, board.score2)
        tempBoard.updateBoard(player, move)
        return tempBoard


    def maxNode(state):
        if(cutOff(state)):
            st=nodeStack.pop()
            return evalFunction(st)
        v= -1000
        o = maxMoves-s
        while(o < maxMoves):
            child=updateState(nodeStack.peek(),o,player)
            if (child.bins != nodeStack.peek().bins):
                nodeStack.push(child)
                v=max(v,minNode(nodeStack.peek()))
            o=o+1

        nodeStack.pop()
        return v

    def minNode(state):
        if(cutOff(state)):
            st=nodeStack.pop()
            res = evalFunction(st)
            return res
        v= 1000
        n = minMoves-s
        while(n < minMoves):
            child=updateState(nodeStack.peek(),n,((player%2)+1))
            if (child.bins != nodeStack.peek().bins):
                nodeStack.push(child)
                v=min(v,maxNode(nodeStack.peek()))
            n=n+1
        nodeStack.pop()  ### in order to get rid of the node that already generated all its children and needs to return its value on level up
        return v              


                          
    #start
    #results={}
    v= -1000
    #nodeStack=Stack()
    #orig=Board(state, score1, score2)
    #nodeStack.push(orig)
    m=maxMoves-s
    while(m < maxMoves):
        child = updateState(nodeStack.peek(),m, player)
        if(child.bins != nodeStack.peek().bins):
            nodeStack.push(child)
            temp=v
            v=max(v,minNode(nodeStack.peek()))
            if (v != temp):
                
                bestMove=m
        m = m+1
    return bestMove
                      
                
