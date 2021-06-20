"""
Area enclosed between the two given functions.
The rightmost and the leftmost x values for the integration are the rightmost and 
the leftmost intersection points of the two functions. 

"""

import numpy as np
import time
import random

from assignment1 import Assignment1
from assignment2 import Assignment2


class Assignment3:
    def __init__(self):

        pass

    def integrate(self, f: callable, a: float, b: float, n: int) -> np.float32:
        """
        Integrate the function f in the closed range [a,b] using at most n 
        points. Your main objective is minimizing the integration error. 

        
        Parameters
        ----------
        f : callable. it is the given function
        a : float
            beginning of the integration range.
        b : float
            end of the integration range.
        n : int
            maximal number of points to use.

        Returns
        -------
        np.float32
            The definite integral of f between a and b
        """

        #Using function interpolation
        test = Function_Interpolation()
        g = test.interpolate(f, a, b, n)
        n = n*1000
        dist = (b - a) / (n - 1)
        lst = [g(a), g(b)]
        for i in range(1, n - 1):
            num = g(a + i * dist)
            if i % 2 == 1:
                lst.append(4 * num)
            else:
                lst.append(2 * num)
        return np.float32(sum(sorted(lst))*(dist / 3))


    def areabetween(self, f1: callable, f2: callable) -> np.float32:
        """
        Finds the area enclosed between two functions. This method finds 
        all intersection points between the two functions to work correctly. 


        Parameters
        ----------
        f1,f2 : callable. These are the given functions

        Returns
        -------
        np.float32
            The area between function and the X axis

        """
        #Using intersections finder
        intersec = Intersections_Finder()
        intersec_lst = intersec.intersections(f1, f2, 1, 100)
        intersections = []
        for i in intersec_lst:
            intersections.append(i)
        if len(intersections)<2:
            return None
        result = 0
        # Calculate area between
        for i in range(len(intersections) - 1):
            a1 = intersections[i]
            b1 = intersections[i + 1]
            tmp = np.linspace(a1, b1, 1000)
            x = np.array([i for i in tmp])
            y1 = np.array([f1(i) for i in tmp])
            y2 = np.array([f2(i) for i in tmp])
            for i in range(len(x) - 1):
                result += abs(x[i] - x[i + 1]) * (abs((y1[i] + y1[i + 1]) / 2 - (y2[i] + y2[i + 1]) / 2))
        return np.float32(result)

