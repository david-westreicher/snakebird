import bfs
import game
import sys
import time
import uinput

level = ''
fil = open(sys.argv[1],'r')
for l in fil:
    level+=l
fil.close()
level = level[:-1]

game.setLevel(level)
moves = bfs.start(game,200 if len(sys.argv)<=2 else int(sys.argv[2]))
if moves is not None:
    keys = {'u':uinput.KEY_U,'l':uinput.KEY_L,'d':uinput.KEY_D,'r':uinput.KEY_R,'tab':uinput.KEY_T}
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
