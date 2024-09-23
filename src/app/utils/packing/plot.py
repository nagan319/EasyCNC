"""
Author: nagan319
Date: 2024/09/07
"""

import matplotlib
matplotlib.use('Agg')  # non-interactive method: does not display plots, simply saves them

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os
from typing import List

from .utils.rectangle2d import Rectangle2D
from .utils.area2d import Area2D
from .bin import Bin

os.makedirs('plots', exist_ok=True)

def plot_area(area: Area2D, show_bbox: bool = True, filename: str = 'plots/area_plot.png'):
    """
    Plot the given Area2D object, including its shape and optional bounding box, and save to file.

    Parameters:
    - area: An instance of the Area2D class.
    - show_bbox: Boolean flag indicating whether to show the bounding box of the shape.
    - filename: The file path where the plot will be saved.
    """
    fig, ax = plt.subplots()

    shape_patch = patches.Polygon(
        list(area.shape.exterior.coords),  
        edgecolor='red',
        facecolor='lightcoral',
        linewidth=2,
        label='Shape'
    )
    ax.add_patch(shape_patch)

    if show_bbox:
        bbox = area.get_bb()
        bbox_patch = patches.Rectangle(
            (bbox.min_x, bbox.min_y),
            bbox.width,
            bbox.height,
            edgecolor='blue',
            facecolor='none',
            linewidth=1,
            linestyle='--',
            label='Bounding Box'
        )
        ax.add_patch(bbox_patch)

    ax.set_xlim(0, area.get_bb().max_x + 10) 
    ax.set_ylim(0, area.get_bb().max_y + 10)  
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()
    plt.xlabel('Width')
    plt.ylabel('Height')
    plt.title('Area2D Shape')
    plt.legend()
    plt.grid(True)

    plt.savefig(filename)  
    plt.close()  

def plot_bin(bin: Bin, filename: str = 'plots/bin_plot.png'):
    """
    Plot the contents of the bin including placed pieces and free rectangles, and save to file.

    Parameters:
    - bin: An instance of the Bin class.
    - filename: The file path where the plot will be saved.
    """
    fig, ax = plt.subplots()

    bin_rect = Rectangle2D(0, 0, bin.dimension.width, bin.dimension.height)
    bin_patch = patches.Rectangle(
        (bin_rect.min_x, bin_rect.min_y),
        bin_rect.width,
        bin_rect.height,
        edgecolor='black',
        facecolor='none',
        linewidth=2,
        linestyle='--'
    )
    ax.add_patch(bin_patch)
    
    for piece in bin.get_placed_pieces():
        piece_bb = piece.get_bb()
        piece_patch = patches.Rectangle(
            (piece_bb.min_x, piece_bb.min_y),
            piece_bb.width,
            piece_bb.height,
            edgecolor='blue',
            facecolor='lightblue',
            linewidth=1,
            label='Placed Piece'
        )
        ax.add_patch(piece_patch)

    for rect in bin.free_rectangles:
        rect_patch = patches.Rectangle(
            (rect.min_x, rect.min_y),
            rect.width,
            rect.height,
            edgecolor='green',
            facecolor='lightgreen',
            linewidth=1,
            linestyle='--',
            label='Free Rectangle'
        )
        ax.add_patch(rect_patch)

    ax.set_xlim(0, bin.dimension.width)
    ax.set_ylim(0, bin.dimension.height)
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()
    plt.xlabel('Width')
    plt.ylabel('Height')
    plt.title('Bin Contents')
    plt.grid(True)

    plt.savefig(filename)  
    plt.close() 

def plot_bin_final(bin: Bin, filename: str = 'plots/bin_plot_final.png', scale_factor: float = 1, figsize: tuple = (3.9, 3.75), dpi: int = 80):
    """
    Plot only the contours of the placed pieces inside the bin with a white background, 
    showing only the bin dimensions and the pieces. Called in app to match aesthetic. 

    Parameters:
    - bin: An instance of the Bin class.
    - filename: The file path where the plot will be saved.
    - scale_factor: Factor to scale the plot.
    - figsize: Size of the figure (width, height).
    - dpi: Dots per inch for the saved image.
    """
    fig, ax = plt.subplots(figsize=figsize)

    ax.set_facecolor('white')

    bin_rect = Rectangle2D(0, 0, bin.dimension.width, bin.dimension.height)
    bin_patch = patches.Rectangle(
        (bin_rect.min_x, bin_rect.min_y),
        bin_rect.width,
        bin_rect.height,
        edgecolor='black',
        facecolor='none',
        linewidth=2,
        linestyle='-'
    )
    ax.add_patch(bin_patch)

    for piece in bin.get_placed_pieces():
        piece_shape = piece.shape  
        
        shape_patch = patches.Polygon(
            list(piece_shape.exterior.coords), 
            edgecolor='black',
            facecolor='none',
            linewidth=2,
            linestyle='-'
        )
        ax.add_patch(shape_patch)

        piece_bb = piece.get_bb()  
        bbox_patch = patches.Rectangle(
            (piece_bb.min_x, piece_bb.min_y),
            piece_bb.width,
            piece_bb.height,
            edgecolor='blue',
            facecolor='none',
            linewidth=1,
            linestyle='--'
        )
        ax.add_patch(bbox_patch)

    ax.set_xlim(0, bin.dimension.width)
    ax.set_ylim(0, bin.dimension.height)
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()

    plt.grid(False)
    ax.tick_params(axis='x', colors='black')  
    ax.tick_params(axis='y', colors='black')  

    for spine in ax.spines.values():
        spine.set_color('black')

    plt.savefig(filename, bbox_inches='tight', facecolor='white', dpi=dpi)
    plt.close()
