import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict, Any

"""
Utils for plotting plates and routers.
"""

class PlottingConstants: 
    PLOT_BG_COLOR = '#ffffff' 
    PLOT_TEXT_COLOR = '#000000'
    PLOT_LINE_COLOR = '#000000'

def _generate_rectangle_coordinates(width: float, height: float, offset_x: float = 0, offset_y: float = 0) -> Tuple[List[float], List[float]]:
    """
    Gets rectangle coordinates given width, height, and offset.

    Arguments:
    - width
    - height
    - offset_x
    - offset_y
    All arguments are floating point values.

    Returns:
    - Tuple of x and y coordinates in plotting format.
    """
    x_coordinates = [offset_x, offset_x + width, offset_x + width, offset_x, offset_x]
    y_coordinates = [offset_y, offset_y, offset_y + height, offset_y + height, offset_y]
    return x_coordinates, y_coordinates
