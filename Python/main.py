import scipy as sp

from scipy.optimize import minimize
def f(x) : 
    return (x-3)**2
    
res = minimize(f,2)
res