"""
Fit a model function of to data that you sample from a given function.

The sampled data is very noisy so should minimize the mean least squares
between the model you fit and the data points you sample.  

 """
import unittest
import numpy as np
import time
import random
from sampleFunctions import *
from tqdm import tqdm
class FitData:
    def __init__(self):

        pass

    def fit(self, f: callable, a: float, b: float, d:int, maxtime: float) -> callable:
        """
        Build a function that accurately fits the noisy data points sampled from
        some closed shape. 
        
        Parameters
        ----------
        f : callable. 
            A function which returns an approximate (noisy) Y value given X. 
        a: float
            Start of the fitting range
        b: float
            End of the fitting range
        d: int 
            The expected degree of a polynomial matching f
        maxtime : float
            This function returns after at most maxtime seconds. 

        Returns
        -------
        a function:float->float that fits f between a and b
        """


        arr = [0 for i in range(d*d)]
        linspace = np.linspace(a, b, d*d,endpoint=True)
        T = time.time()
        counter = 0
        bezierlst = []
        while (time.time()-T)<(maxtime-1):
            counter += 1
            for j in range(len(linspace)):
                arr[j] += f(linspace[j]).item()
        for i in range(len(arr)):
            arr[i] = (linspace[i],arr[i]/counter)
        while len(arr) != 0:
            if len(arr) == 3:
                p1 = arr[0]
                p3 = arr[2]
                p2 = ((2 * arr[1][0] - 0.5 * arr[0][0] - 0.5 * arr[2][0]),
                      (2 * arr[1][1] - 0.5 * arr[0][1] - 0.5 * arr[2][1]))
                bezierlst.append(bezier2(p1, p2, p3))
                break
            if len(arr) == 4:
                p1 = arr[0]
                p3 = arr[2]
                p2 = ((2 * arr[1][0] - 0.5 * arr[0][0] - 0.5 * arr[2][0]),
                      (2 * arr[1][1] - 0.5 * arr[0][1] - 0.5 * arr[2][1]))
                bezierlst.append(bezier2(p1, p2, p3))
                p11 = arr[1]
                p33 = arr[3]
                p22 = ((2 * arr[2][0] - 0.5 * arr[1][0] - 0.5 * arr[3][0]),
                      (2 * arr[2][1] - 0.5 * arr[1][1] - 0.5 * arr[3][1]))
                tmpbzar = bezier2(p11, p22, p33)
                p1 = arr[2]
                p3 = arr[3]
                p2 = tmpbzar(0.75)
                p2 = ((2 * p2[0] - 0.5 * arr[3][0] - 0.5 * arr[2][0]),
                      (2 * p2[1] - 0.5 * arr[3][1] - 0.5 * arr[2][1]))
                bezierlst.append(bezier2(p1, p2, p3))
                break
            p1 = arr[0]
            p3 = arr[2]
            p2 = ((2 * arr[1][0] - 0.5 * arr[0][0] - 0.5 * arr[2][0]), (2 * arr[1][1] - 0.5 * arr[0][1] - 0.5 * arr[2][1]))
            bezierlst.append(bezier2(p1, p2, p3))
            arr.remove(arr[0])
            arr.remove(arr[0])
        def f(num):
            for node in bezierlst:
                if num >= node(0)[0] and num <= node(1)[0]:
                    T = abs((num - node(0)[0]) / (node(1)[0] - node(0)[0]))
                    return node(T)[1]
            return bezierlst[0](0)[1]
        return f

