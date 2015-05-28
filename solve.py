import bfs
import game
import sys
import time
import uinput
import imutil
import pickle

def lvlfromscreen():
    PATCH_NAMES = {
        'spikes':'s',
        'wall':'w',
        'fruit':'f',
        'snake':'s',
        'bodygreen':'g',
        'headgreen':'G',
        'bodyblue':'b',
        'headblue':'B',
        'bodyred':'r',
        'headred':'R',
        'goal':'e'
    }
    level = ''
    im = imutil.screenshot()
    im = imutil.loadim('screens/0.png')
    clf = pickle.load(open('svm.conf','rb'))
    width = 0
    for x,y,patch in imutil.getPatches(im):
        if y==0 and x>0:
                level+='\n'
        if x==0:
            width+=1
        histo = imutil.histogram(patch)
        pname = str(clf.predict([histo])[0])
        level+= ' ' if pname not in PATCH_NAMES else PATCH_NAMES[pname]

    empty = ''.join([' ' for i in range(width)])
    for i in range(5):
        level=empty+'\n'+level+'\n'+empty
    return level

def lvlfromfile(f):
    level = ''
    fil = open(f,'r')
    for l in fil:
        level+=l
    fil.close()
    level = level[:-1]
    return level

def simulatemoves(moves):
    if moves is None:
        return
    keys = {'up':uinput.KEY_UP,'left':uinput.KEY_LEFT,'down':uinput.KEY_DOWN,'right':uinput.KEY_RIGHT,'tab':uinput.KEY_TAB}
    devkeys = []
    for k in keys:
        devkeys.append(keys[k])
    device = uinput.Device(devkeys)
    time.sleep(2)
    print('starting keypresses')
    for m in moves:
        time.sleep(0.4)
        print('simulate '+m)
        if m=='wait':
            time.sleep(1)
        else:
            device.emit_click(keys[m])
            device.syn()
    print('finished keypresses')

if __name__=="__main__":
    level = lvlfromscreen() if len(sys.argv)==1 else lvlfromfile(sys.argv[1])
    game.setLevel(level)
    moves = bfs.start(game,200 if len(sys.argv)<=2 else int(sys.argv[2]))
    simulatemoves(moves)
