"""
Interpolate given function.
"""

import numpy as np
import time
import random

from sampleFunctions import *


class InterpolateFunction:
    def __init__(self):

        pass

    def interpolate(self, f: callable, a: float, b: float, n: int) -> callable:
        """
        Interpolate the function f in the closed range [a,b] using at most n 
        points.
        
        Parameters
        ----------
        f : callable. it is the given function
        a : float
            beginning of the interpolation range.
        b : float
            end of the interpolation range.
        n : int
            maximal number of points to use.

        Returns
        -------
        The interpolating function.
        """

        if n == 1:
            def g(num):
                return f((a + b) / 2)

            return g
        n = n // 2

        # derivative calculator
        def d_f(x, i):
            h = 1e-9
            return (f(x + h) - yVal[i]) / h
        # Lists on X-Values, Y-Values and Derivative-Values.
        xVal = np.linspace(a, b, n, endpoint=True)
        yVal = np.array([f(i) for i in xVal])
        nigzeretVal = np.array([d_f(xVal[i], i) for i in range(len(xVal))])
        count = 0
        bezierLst = []
        delta = abs(xVal[1] - xVal[0])
        # Interpolating the function using Bezier curve.
        while count < len(xVal) - 1:
            p0 = (xVal[count], yVal[count])
            p3 = (xVal[count + 1], yVal[count + 1])
            p1 = (xVal[count] + delta / 3, yVal[count] + nigzeretVal[count] * (delta / 3))
            p2 = ((xVal[count + 1] - (delta / 3)), yVal[count + 1] - nigzeretVal[count + 1] * (delta / 3))
            bezierLst.append(bezier3(p0, p1, p2, p3))
            count += 1

        def f(num):
            pos = int(((num - a) / (b - a)) * (n - 1))
            T = ((num - a - pos * delta) / delta)
            if pos == len(bezierLst):
                return bezierLst[pos - 1](1)[1]
            return bezierLst[pos](T)[1]

        return f
