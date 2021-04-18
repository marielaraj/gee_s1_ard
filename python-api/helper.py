#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Version: v1.0
Date: 2021-03-12
Authors: Mullissa A., Vollrath A.,  Reiche J., Slagter B., Balling J. , Gou Y., Braun, C.
"""

import ee

# ---------------------------------------------------------------------------//
# Linear to db scale
# ---------------------------------------------------------------------------//

def lin_to_db(image):
    """
    Convert backscatter from linear to dB.

    Parameters
    ----------
    image : ee.Image
        Image to convert 

    Returns
    -------
    ee.Image
        output image

    """
    bandNames = image.bandNames().remove('angle')
    db = ee.Image.constant(10).multiply(image.select(bandNames).log10())
    return image.addBands(db, None, True)

def lin_to_db2(image):
    """
    Convert backscatter from linear to dB by removing the ratio band.

    Parameters
    ----------
    image : ee.Image
        Image to convert

    Returns
    -------
    ee.Image
        Converted image

    """
    db = ee.Algorithms.If(image.bandNames().contains('VH'),\
                            ee.Image.constant(10).multiply(image.select(['VV', 'VH']).log10()).rename(['VV', 'VH']) ,\
                                ee.Image.constant(10).multiply(image.select(['HH', 'HV']).log10()).rename(['HH', 'HV']))
    return image.addBands(db, None, True)

# ---------------------------------------------------------------------------//
# Add ratio bands
# ---------------------------------------------------------------------------//

def add_ratio_lin(image):
    """
    Adding ratio band for visualization 

    Parameters
    ----------
    image : ee.Image
        Image to use for creating band ratio

    Returns
    -------
    ee.Image
        Image containing the ratio band

    """
    ratio = ee.Algorithms.If(image.bandNames().contains('VH'),\
                                image.addBands(image.select('VV').divide(image.select('VH')).rename('VVVH_ratio')),\
                                    image.addBands(image.select('HH').divide(image.select('HV')).rename('HHHV_ratio')))
    
    return ratio.set('system:time_start', image.get('system:time_start'))
