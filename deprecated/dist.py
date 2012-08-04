import numpy
import math

class DistPair:
    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2
        self.getDist()

    def getDist(self):
        x = []
        y = []
        i = self.c1
        j = self.c2
        rawx = i.high()
        indx = i.date()
        rawy = j.high()
        indy = j.date()
        maxind = min(len(indx), len(indy))
        for ind in xrange(maxind):
            if indx[ind] in indy:
                x.append(rawx[ind])
                y.append(rawy[ind])
        deltaX = delta(diff(x))
        deltaY = delta(diff(y))

        self.dist = sqrtDist(x, y)
        self.deltaDist = sqrtDist(deltaX, deltaY)



def sqrtDist(x, y):
    a = numpy.array(x)
    b = numpy.array(y)
    dist = sum(a*b) / (math.sqrt(sum(a*a))*math.sqrt(sum(b*b)))
    return dist

def diff(x):
    d = []
    for ind in xrange(len(x)-1):
        d.append(x[ind+1] - x[ind])
    return d

def delta(x):
    d = []
    for i in x:
        if i>0: d.append(1)
        elif i==0: d.append(0)
        else: d.append(-1)
    return d

def distCompanys(companys):
    dists = []
    for j in companys.values():
        for i in companys.values():
            d = DistPair(i, j)
            dists.append(d)
            print 'A:',d.c1.ticker,'B:',d.c2.ticker,'dist:',d.dist,\
                'deltaDist:',d.deltaDist
    return dists
        
def test(companys):
    dists = distCompanys(companys)
    return dists
