'''
Created on 7 mar. 2022

@author: ceci
'''
import numpy as np


def Period(semimajorAxis):
    """ 
    -Computes orbital period in seconds- 
    semimajorAxis: float [km]   
     """
    mu = 398600.448
    if semimajorAxis>0:
        period=2*np.pi*np.sqrt(semimajorAxis*semimajorAxis*semimajorAxis/mu)
    else:
        print('SemimajorAxis must be a positive number')
    return period

def semimajorAxis(rp,ra):
    """
    Rt: Terrestrial radious [km]
    rp: perigee altitude [km]
    ra: apogee altitude [km]
    """
    Rt=6378.0
    if (rp>0) and (ra>0):
        semimajor_axis=((rp+Rt+ra+Rt)/2)
    else:
        print('Altitudes must be positives numbers')
    return semimajor_axis
