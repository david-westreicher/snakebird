import bfs
import game
import sys

level = ''
fil = open(sys.argv[1],'r')
for l in fil:
    level+=l
fil.close()
level = level[:-1]

game.setLevel(level)
bfs.start(game,200)
