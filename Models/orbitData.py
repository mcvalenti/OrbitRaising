'''
Created on 7 mar. 2022

@author: ceci
'''
import numpy as np


def Period(semimajorAxis):
    """ Computes orbital period in seconds  """
    mu = 398600.448
    return 2*np.pi*np.sqrt(semimajorAxis*semimajorAxis*semimajorAxis/mu)

