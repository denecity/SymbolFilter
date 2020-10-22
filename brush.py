import numpy as np
import cv2
from numba import jit

windowTitle = "yeetyeet"




class brush():

    def __init__(windowTitle, maxValVal, cutoffVal):

        self.windowTitle = windowTitle
        self.maxValVal = 200
    cutoffVal = 40

    @jit(nopython=True, parallel=True)
    def createBrush(m, t, l, size, brush):
        for i in range(size[0]):
            for j in range(size[1]):
                x = ((m - i - 1)**2 + (m - j - 1)**2)**0.5
                brush[i][j] = int(t * (t / l) ** ((-1 * (x - m)**2)/(m**2)))
        return brush
    


@jit(nopython=True, parallel=True)
def createBrush(m, t, l, size, brush):
    for i in range(size[0]):
        for j in range(size[1]):
            x = ((m - i - 1)**2 + (m - j - 1)**2)**0.5
            brush[i][j] = int(t * (t / l) ** ((-1 * (x - m)**2)/(m**2)))
    return brush

def maxVal(val):
    global maxValVal
    maxValVal = val
    restFilters()

def cutoff(val):
    global cutoffVal
    cutoffVal = val
    restFilters()


def restFilters():
    cv2.namedWindow(windowTitle)

    size = (507, 507)
    m = (size[0] + 1) / 2

    brush = np.zeros(size)

    t = cutoffVal / 100
    l = maxValVal

    brush = createBrush(m, t, l, size, brush) / 255

    cv2.imshow(windowTitle, brush)

if __name__ == "__main__":
    cv2.namedWindow(windowTitle)
    cv2.createTrackbar("maxVal", windowTitle, 0, 255, maxVal)
    cv2.createTrackbar("cutoff", windowTitle, 0, 100, cutoff)

    restFilters()
    cv2.waitKey()