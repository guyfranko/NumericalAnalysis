"""
Fit a model function to data  that you sample from a contour of given shape.
Calculate the area of that shape.

The sampled data is very noisy so  minimize the mean least squares
between the model you fit and the data points you sample.  


"""

import numpy as np
import time
import random
from sklearn.cluster import KMeans
from sampleFunctions import *


class MyShape(AbstractShape):
    def __init__(self, area,bezierlst):
        self.area1 = area
        self.bezierlst = bezierlst

    def area(self):
        return np.float32(self.area1)
    def contour(self, n: int):
        linspace = np.linspace(0, 1, 100, endpoint=True)
        ekef = 0
        for i in self.bezierlst:
            for j in range(len(linspace)-1):
                ekef+=((i(linspace[j])[0]-i(linspace[j+1])[0])**2 + (i(linspace[j])[1]-i(linspace[j+1])[1])**2)**0.5
        linspace1 = np.linspace(0, ekef, n, endpoint=True)
        x = 0
        contr = 0
        conturlst = []
        for i in self.bezierlst:
            for j in range(len(linspace)-1):
                if contr == len(linspace1):
                    break
                x+=((i(linspace[j])[0]-i(linspace[j+1])[0])**2 + (i(linspace[j])[1]-i(linspace[j+1])[1])**2)**0.5
                if x>= linspace1[contr]-0.01 and x<= linspace1[contr]+0.01:
                    conturlst.append(((i((linspace[j+1]+linspace[j])/2)[0]),(i((linspace[j+1]+linspace[j])/2)[1])))
                    contr+= 1
        return np.array(conturlst)

class Assignment4:
    def __init__(self):


        pass

    def area(self, contour: callable, maxerr=0.001) -> np.float32:
        """
        Compute the area of the shape with the given contour. 

        Parameters
        ----------
        contour : callable
            Same as AbstractShape.contour 
        maxerr : TYPE, optional
            The target error of the area computation. The default is 0.001.

        Returns
        -------
        The area of the shape.

        """
        num = (str(maxerr))
        if num[len(num)-1] != str(1):
            num = int(num[len(num)-1]) -1
        else:
            num = len(num) -3
        dgimot = 20*(3**num)
        result = np.float32(0)
        arr = [(i[0],i[1]) for i in contour(dgimot)]
        for p in range(len(arr)-1):
            result += (arr[p][0]-arr[p+1][0]) * (((arr[p][1]+arr[p+1][1]) / 2))
        return np.float32(abs(result))

    def fit_shape(self, sample: callable, maxtime: float) -> AbstractShape:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape.

        Parameters
        ----------
        sample : callable.
            An iterable which returns a data point that is near the shape contour.
        maxtime : float
            This function returns after at most maxtime seconds.

        Returns
        -------
        An object extending AbstractShape.
        """

        SampleArr = []
        for i in range(40000):
            x, y = sample()
            SampleArr.append((x, y))
        def sortArr(arr, n, p):
            vp = []
            for i in range(n):
                dist = pow((p[0] - arr[i][0]), 2) + pow((p[1] - arr[i][1]), 2)
                vp.append((dist, (arr[i][0], arr[i][1])))
            return sorted(vp, key=lambda tup: tup[0])
        kmeans = KMeans(n_clusters=20, random_state=0).fit(SampleArr)
        centroids = [(i[0], i[1]) for i in kmeans.cluster_centers_]
        p = centroids[0]
        s = (centroids[0][0], centroids[0][1])
        BezierPoints = []
        while len(centroids) != 1:
            tmp = [i[1] for i in sortArr(centroids, len(centroids), p)]
            p = tmp[1]
            BezierPoints.append(tmp[0])
            centroids.remove((tmp[0][0], tmp[0][1]))
        BezierPoints.append(tmp[1])
        BezierPoints.append(centroids[0])
        BezierPoints.append(s)
        bezierlst = []
        while len(BezierPoints) != 0:
            if len(BezierPoints) == 3:
                p1 = BezierPoints[0]
                p3 = BezierPoints[2]
                p2 = ((2 * BezierPoints[1][0] - 0.5 * BezierPoints[0][0] - 0.5 * BezierPoints[2][0]),
                      (2 * BezierPoints[1][1] - 0.5 * BezierPoints[0][1] - 0.5 * BezierPoints[2][1]))
                bezierlst.append(bezier2(p1, p2, p3))
                break
            if len(BezierPoints) == 4:
                p1 = BezierPoints[0]
                p3 = BezierPoints[2]
                p2 = ((2 * BezierPoints[1][0] - 0.5 * BezierPoints[0][0] - 0.5 * BezierPoints[2][0]),
                      (2 * BezierPoints[1][1] - 0.5 * BezierPoints[0][1] - 0.5 * BezierPoints[2][1]))
                bezierlst.append(bezier2(p1, p2, p3))
                p11 = BezierPoints[1]
                p33 = BezierPoints[3]
                p22 = ((2 * BezierPoints[2][0] - 0.5 * BezierPoints[1][0] - 0.5 * BezierPoints[3][0]),
                      (2 * BezierPoints[2][1] - 0.5 * BezierPoints[1][1] - 0.5 * BezierPoints[3][1]))
                tmpbzar = bezier2(p11, p22, p33)
                p1 = BezierPoints[2]
                p3 = BezierPoints[3]
                p2 = tmpbzar(0.75)
                p2 = ((2 * p2[0] - 0.5 * BezierPoints[3][0] - 0.5 * BezierPoints[2][0]),
                      (2 * p2[1] - 0.5 * BezierPoints[3][1] - 0.5 * BezierPoints[2][1]))
                bezierlst.append(bezier2(p1, p2, p3))
                break
            p1 = BezierPoints[0]
            p3 = BezierPoints[2]
            p2 = ((2 * BezierPoints[1][0] - 0.5 * BezierPoints[0][0] - 0.5 * BezierPoints[2][0]), (2 * BezierPoints[1][1] - 0.5 * BezierPoints[0][1] - 0.5 * BezierPoints[2][1]))
            bezierlst.append(bezier2(p1, p2, p3))
            BezierPoints.remove(BezierPoints[0])
            BezierPoints.remove(BezierPoints[0])
        result = 0
        for i in bezierlst:
            linspace = np.linspace(1, 0, 100)
            x = []
            y = []
            for num in linspace:
                x.append(i(num)[0])
                y.append(i(num)[1])
            for i in range(len(x) - 1):
                result += (x[i] - x[i + 1]) * (((y[i] + y[i + 1]) / 2))
        result = MyShape(abs(result),bezierlst)
        return result

