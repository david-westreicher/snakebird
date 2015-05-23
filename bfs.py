def start(problem,maxdepth):
    states = 1
    queue = [(problem.init(),[])]
    allposs = {str(queue[0][0]):True}
    for i in range(maxdepth):
        nextqueue = []
        print('#####DEPTH'+str(i)+'#####')
        for state,moves in queue:
            posss = problem.getPoss(state,moves)
            for poss,newmoves in posss:
                if problem.goal(poss):
                    print('Reached GOAL at depth: '+str(i)+' with visiting '+str(states)+' states')
                    problem.printstate(poss,newmoves)
                    return
                hashr = str(poss)
                if(hashr not in allposs):
                    #problem.printstate(poss,newmoves)
                    allposs[hashr] = True
                    states+=1
                    nextqueue.append((poss,newmoves))
        queue = nextqueue
        if len(nextqueue) == 0:
            break
