import copy

snakenames = ['R','G','Y']
possmoves = [(1,0),(-1,0),(0,1),(0,-1)]
moveIndexName = ['right','left','down','up']

class DiedException(Exception):
    pass

class Level:
    def __init__(self,strlvl=None):
        if strlvl is not None:
            split = strlvl.split('\n')
            self.height = len(split)
            self.width = len(split[0])
            self.data = [[split[y][x] for x in range(self.width)] for y in range(self.height)]

    def init(self):
        fruits = []
        while True:
            fruit = self.finddel('f')
            if fruit is None:
                break
            fruits.append(fruit)
        snakes = []
        for name in snakenames:
            snake = []
            start = self.finddel(name)
            if start is None:
                continue
            snake.append(start)
            found = True
            while found:
                found = False
                for m in possmoves:
                    newx = start[0]+m[0]
                    newy = start[1]+m[1]
                    val = self.data[newy][newx]
                    if val==name.lower():
                        self.data[newy][newx] = ' '
                        start = [newx,newy]
                        snake.append(start)
                        found = True
                        break
            if len(snake)>0:
                snakes.append(snake)
        return snakes,fruits

    @staticmethod
    def lvlfromstate(state):
        globallevel = Level.globallevel
        newlevel = Level()
        newlevel.width = globallevel.width
        newlevel.height = globallevel.height
        newlevel.data = copy.deepcopy(globallevel.data)
        snakes,fruits,_ = state
        for snakeid,snake in enumerate(snakes):
            name = snakenames[snakeid]
            for i,pos in enumerate(snake):
                newlevel.data[pos[1]][pos[0]] = name if i==0 else name.lower()
        if fruits is not None:
            for i,pos in enumerate(fruits):
                newlevel.data[pos[1]][pos[0]] = 'f'
        return newlevel 

    def find(self,char):
        for x in range(self.width):
            for y in range(self.height):
                if self.data[y][x] == char:
                    return [x,y]
        return None

    def finddel(self,char):
        pos = self.find(char)
        if pos is not None:
            self.data[pos[1]][pos[0]] = ' '
        return pos

    def printLvl(self):
        for y in range(self.height):
            for x in range(self.width):
                val = self.data[y][x]
                if val.lower()=='r':
                    print(colors.RED+val+colors.END),
                elif val.lower()=='g':
                    print(colors.GREEN+val+colors.END),
                elif val.lower()=='f':
                    print(colors.YELLOW+val+colors.END),
                else:
                    print(val),
            print('\n'),

class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def printState(state):
    lvl = Level.lvlfromstate(state)
    _,_,player = state
    print('Turn: '+snakenames[player])
    lvl.printLvl()

def printMoves(moves):
    def add(count,last):
        if last is not None:
            cmds.append(str(count)+'x '+last)

    last = None
    count = 1
    cmds = []
    for m in moves:
        if m==last:
            count+=1
        else:
            add(count,last)
            count = 1
        last = m
    add(count,last)
    print(cmds)


def advanceSnake(snake,move):
    snake.pop()
    start = copy.deepcopy(snake[0])
    start[0]+=move[0]
    start[1]+=move[1]
    snake.insert(0,start)
    return snake 

def moveSnake(lvl,snake,snakesym,direction):
    # TODO could move snakes recursively
    hit = False
    spikes = 0
    for el in snake:
        x = el[0]+direction[0]
        y = el[1]+direction[1]
        if y>=lvl.height:
            raise DiedException()
        val = lvl.data[y][x].lower()
        if val=='s':
            spikes+=1
        elif val!=snakesym and val!=' ' and val!='e':
            hit = True
            break
    if not hit:
        if spikes>0:
            raise DiedException()
        for el in snake:
            lvl.data[el[1]][el[0]] = ' '
        for eli,el in enumerate(snake):
            el[0]+=direction[0]
            el[1]+=direction[1]
            lvl.data[el[1]][el[0]] = snakesym if eli==0 else snakesym.lower()
    return hit

def gravity(snakes,fruits):
    # TODO could fall into goal with the head
    lvl = Level.lvlfromstate((snakes,fruits,None))
    while True:
        allonground = True
        for snakei,snake in enumerate(snakes):
            if not moveSnake(lvl,snake,snakenames[snakei].lower(),[0,1]):
                allonground = False
                madechange = True
        if allonground:
            break

def getPoss(state,moves):
    snakes,fruits,player = state
    if player>=len(snakes):
        player=0
    poss = []
    def addposs(state,mvs):
        newmoves = copy.deepcopy(moves)
        newmoves.extend(mvs)
        poss.append((state,newmoves))
    # press tab
    if len(snakes)>1:
        addposs((snakes,fruits,(player+1)%len(snakes)),['tab'])
    # move player
    lvl = Level.lvlfromstate(state)
    playerpos = lvl.find(snakenames[player])
    if playerpos is None:
        return []
    for movei,move in enumerate(possmoves):
        newx = playerpos[0]+move[0]
        newy = playerpos[1]+move[1]
        blockval = lvl.data[newy][newx]
        newsnakes = copy.deepcopy(snakes)
        newfruits = copy.deepcopy(fruits)
        allvalid = True
        newmvs = [moveIndexName[movei]]
        if blockval == ' ':
            advanceSnake(newsnakes[player],move)
        elif blockval == 'f':
            newsnakes[player].insert(0,[newx,newy])
            for fruiti,fruit in enumerate(newfruits):
                if fruit[0]==newx and fruit[1]==newy:
                    break
            if fruiti>=0:
                del newfruits[fruiti]
        elif blockval == 'e':
            del newsnakes[player]
            newmvs.append('wait')
        elif blockval.upper() != snakenames[player] and blockval.upper() in snakenames:
            newlvl = Level.lvlfromstate(state)
            pushsnakei = snakenames.index(blockval.upper())
            allvalid = False
            try:
                if not moveSnake(newlvl,newsnakes[pushsnakei],snakenames[pushsnakei].lower(),move):
                    advanceSnake(newsnakes[player],move)
                    allvalid = True
            except DiedException as e:
                pass
        else:
            allvalid = False
        if allvalid:
            try:
                gravity(newsnakes,newfruits)
                addposs((newsnakes,newfruits,player),newmvs)
            except DiedException as e:
                pass
    return poss

def setLevel(lvl):
    global strlvl
    strlvl = lvl

def init():
    Level.globallevel = Level(strlvl)
    snakes,fruits = Level.globallevel.init()
    return (snakes,fruits,0)

def goal(state):
    snakes,fruits,_ = state
    if len(snakes)==0 and len(fruits)==0:
        return True
    return False

def printstate(state,moves=None):
    printState(state)
    if moves is not None:
        printMoves(moves)
