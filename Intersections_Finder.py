"""
Intersection points for two functions.
"""

import numpy as np
import time
import random
from collections.abc import Iterable


class Intersection:
    def __init__(self):

        pass

    def intersections(self, f1: callable, f2: callable, a: float, b: float, maxerr=0.001) -> Iterable:
        """
        Find as many intersection points as you can.

        Parameters
        ----------
        f1 : callable
            the first given function
        f2 : callable
            the second given function
        a : float
            beginning of the interpolation range.
        b : float
            end of the interpolation range.
        maxerr : float
            An upper bound on the difference between the
            function values at the approximate intersection points.

        Returns
        -------
        X : iterable of approximate intersection Xs such that for each x in X:
            |f1(x)-f2(x)|<=maxerr.

        """
        # Using Bisection method
        def bis(g, c, d):
            z = (c + d) / 2
            while abs(g(z)) > maxerr:
                if g(c) * g(z) < 0:
                    d = z
                else:
                    c = z
                z = (c + d) / 2
            return z
        # Using Secant method
        def secant(g, c, d):
            x = [c, d, d]
            i = 0
            while abs(g(x[2])) > maxerr and i < 100:
                i += 1
                x[2] = x[1] - g(x[1]) * ((x[1] - x[0]) / (g(x[1]) - g(x[0])))
                x[0] = x[1]
                x[1] = x[2]
                try:
                    g(x[2])
                except:
                    break
            if c <= x[2] <= d and abs(g(x[2])) < maxerr:
                return x[2]
        f = f1 - f2
        intersections = []
        while a < b:
            if f(a + 0.05)*f(a)< 0:
                P = bis(f, a, a + 0.05)
                intersections.append(P)
            else:
                P = secant(f, a, a + 0.05)
                if P is not None:
                    intersections.append(P)
            if P is not None:
                pow = 0
                while abs(f(P + 0.05 * 2 ** pow)) <= maxerr:
                    pow += 1
                a = P + 0.05 * 2 ** pow
            else:
                a += 0.05
        return iter(intersections)

