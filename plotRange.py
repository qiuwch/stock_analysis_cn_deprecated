from pylab import *
import dj
import dist
import pdb
from DowJonesDataLoader import DowJonesDataLoader

def testPlot():
    plot(1,1)
    show()

def plotRange(x, y, markerType=None):
    if markerType == None:
        plot(x, y)
    else:
        plot(x, y, markerType)
    show()

def plotCompany(c, y=None, start = datetime.datetime(1988, 4, 1), end = datetime.datetime(1998, 5, 1), markerType=None):
    title(c.ticker)
    start = datetime.datetime(1988, 4, 1)
    end = datetime.datetime(1998, 5, 1)
    x = c.GetDate(start, end)
    px = range(len(x))
    # px = x

    if y == None:
        y = c.high(start, end)
    plotRange(px, y, markerType)

def plotCompanys(companys):
    for c in companys.values(): plotCompany(c)

def testPlot(companys):
    c = companys['msft']
    start = datetime.datetime(1988, 4, 1)
    end = datetime.datetime(1998, 5, 1)
    # y = dist.delta(dist.diff(c.GetHigh(start, end)))
    # y.append(0) # to make the dimension match
    y = c.GetHigh(start, end)
    # plotCompany(c, y, start, end, '*')
    plotCompany(c, y, start, end)

if __name__ == '__main__':
    companys = DowJonesDataLoader.load()
    testPlot(companys)
