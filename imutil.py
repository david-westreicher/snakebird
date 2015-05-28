import numpy as np
from matplotlib import pyplot as plt
from pyscreenshot import grab
from scipy import signal
from scipy import misc

BINS_PER_COLOR=8

def histogram(img):
    histo = np.zeros(BINS_PER_COLOR**3,dtype=np.int)
    img = img[:,:]/(256/BINS_PER_COLOR)
    for row in img:
        for pix in row:
            index = 0
            for i,c in enumerate(pix):
                index+=c*BINS_PER_COLOR**i
            histo[index]+=1
    #plt.plot(histo)
    #plt.show()
    return histo*1000.0/float(img.shape[0]*img.shape[1])
    #return histo

def loadim(f):
    return misc.imread(f)

def show(im):
    plt.imshow(im)
    plt.show()

def screenshot():
    im = grab(bbox=(50,80,860,470),backend=None)
    pix = np.array(im.getdata(),dtype=np.uint8).reshape(im.size[1],im.size[0],3)
    return pix

def edgefilter(horizontal=True):
    z = np.zeros((3,3))
    if horizontal:
        z[:,0] = -1
        z[:,2] = 1
    else:
        z[0,:] = -1
        z[2,:] = 1
    return z

def colToGray(pix):
    return np.dot(pix,[0.299, 0.587, 0.144]) 

def getLines(screen):
    # get horizontal line responses with convolution
    hor = signal.convolve2d(screen,edgefilter(True),mode='same',boundary='symm')
    ver = signal.convolve2d(screen,edgefilter(False),mode='same',boundary='symm')
    hor = np.absolute(hor)-np.absolute(ver)

    # binarize possible horizontal lines
    thresh = 5
    hor[hor[:,:]<thresh] = 0
    hor[hor[:,:]>thresh] = 1
    #plt.imshow(hor)
    #plt.show()

    # blur the image to make 2 lines -> 1 line
    box = np.ones((3,3))
    box = box*((1.0/3.0)**2)
    hor = signal.convolve2d(hor,box,mode='same',boundary='symm')
    #plt.imshow(hor)
    #plt.show()

    # sum up in the vertical
    horsum = hor.sum(axis = 0)

    validlinethresh = 0.2

    # find lines by taking the average region above a threshold as a line
    lines = []
    start = 0
    for i in range(horsum.shape[0]):
        if horsum[i]/screen.shape[0]>validlinethresh:
            if start == 0:
                start = i
        elif start>0:
            lines.append(float(start+i)/2)
            start = 0

    #plt.plot(horsum/screen.shape[0])
    #plt.plot(lines,horsum[lines]/screen.shape[0],'ro')
    #plt.show()

    def isinlier(index):
        for i in [-1,0,1]:
            if horsum[int(i+index)]/screen.shape[0]>validlinethresh:
                return True
        return False

    def getgrid(start,end,cellnum):
        width = end-start
        cells = []
        for l in range(0,cellnum+1):
            cells.append(start+float(l)*width/cellnum)
        return cells

    def fillgrid(start,end,cellnum):
        width = (end-start)/cellnum
        curr = start
        cells = []
        while curr>=0:
            cells.append(curr)
            curr -= width
        curr = start+width
        cells = list(reversed(cells))
        while curr<screen.shape[1]-1:
            cells.append(curr)
            curr += width
        return cells 


    model = (None,[])
    for i in range(len(lines)-1):
        for j in range(i,len(lines)):
            for k in range(1,j-i+1):
                start = float(lines[i])
                end = float(lines[j])
                cells = getgrid(start,end,k)
                inliers = []
                for c in cells:
                    if isinlier(c):
                        inliers.append(c)
                if len(inliers)>len(model[1]):
                    model = ((start,end,k),inliers)

    plt.plot(horsum/screen.shape[0])
    plt.plot(lines,horsum[lines]/screen.shape[0],'ro')
    lines = fillgrid(*model[0])
    plt.plot(lines,np.ones(len(lines))*0.2,'bo')
    plt.show()
    return lines

def getPatches(image):
    imagegray = colToGray(image)
    verlines = getLines(imagegray)
    horlines = getLines(imagegray.T)

    for h in range(len(horlines)-1):
        for v in range(len(verlines)-1):
            #print(horlines[h],horlines[h+1],verlines[v],verlines[v+1])
            fromx = int(horlines[h])+2
            tox = int(horlines[h+1])-2
            fromy = int(verlines[v])+2
            toy = int(verlines[v+1])-2
            sliced = image[fromx:tox,fromy:toy]
            yield h,v,sliced
