from .bin import Bin
from .utils.dimension2d import Dimension2D
from .utils.rectangle2d import Rectangle2D
from .utils.area2d import Area2D

from typing import List, Tuple, Dict, Union

import os

import matplotlib
matplotlib.use('Agg')  

import matplotlib.pyplot as plt
import matplotlib.patches as patches

def execute_packing_algorithm(
    input_bins: List[Tuple[str, Tuple[float, float], List[Tuple[float, float]]]], 
    input_pieces: List[Tuple[str, List[Tuple[float, float]]]],
    preview_filename: str
) -> Dict[str, Union[None, Tuple[str, Tuple[float, float]]]]:
    """
    Packs pieces into bins and returns their placements.

    Parameters:
        input_bins: List of tuples containing (bin_id, dimensions, contours).
        input_pieces: List of tuples containing (piece_id, contours).
        preview_filename: File to save preview

    Returns:
        A dictionary where:
        - key: piece_id
        - value: None if not placed, or (bin_id, coordinates) if placed.
    """
    
    if not os.path.exists(os.path.dirname(preview_filename)):
        raise FileNotFoundError(f"Directory for indicated preview filepath {preview_filename} does not exist.")
    if not preview_filename.lower().endswith('.png'):
        raise ValueError(f"Preview file must be a png, not {preview_filename}.")

    for bin in input_bins:
        id, dimensions, contours = bin
        if not isinstance(id, str):
            raise ValueError(f"Bin ID {id} is not a string.")
        if not isinstance(dimensions, tuple) or len(dimensions) != 2:
            raise ValueError(f"Bin dimensions {dimensions} must be a tuple of length 2")
        if not isinstance(dimensions[0], float) or not isinstance(dimensions[1], float):
            raise ValueError("Bin dimensions must be floats.")
        if dimensions[0] <= 0 or dimensions[1] <= 0:
            raise ValueError("Bin dimensions must be positive.")

    for piece in input_pieces:
        id, contour = piece
        if not isinstance(id, str):
            raise ValueError(f"Piece ID {id} is not a string.")
        for point in contour: 
            if not isinstance(point, tuple) or len(point) != 2:
                raise ValueError(f"Point {point} in piece {piece.id} is not a tuple of length 2, not {point}")
            for coordinate in point:
                if not isinstance(coordinate, float):
                    raise ValueError(f"All coordinates in piece {piece.id} must be floats, not {coordinate}")        

    bins: List[Bin] = []
    pieces: List[Area2D] = []
    res: Dict[str, Union[None, Tuple[str, Tuple[float, float]]]] = {}

    for bin in input_bins:
        bin_id, dimensions, contours = bin
        width, height = dimensions
        bin_obj = Bin(bin_id, Dimension2D(width, height))
        for i, contour in enumerate(contours):
            part = Area2D(
                bin_id+f'ctr{i}', 
                points=contour, 
                shift_to_origin=False
            )
            bin_obj.add_immovable_part(part)
        bins.append(bin_obj)
    
    for piece in input_pieces:
        piece_id, outer_contour = piece
        pieces.append(Area2D(id=piece_id, points=outer_contour))

    bins = sorted(bins, key=lambda b: b.get_empty_area())
    pieces = sorted(pieces, key=lambda p: p.get_bb().area, reverse=True)

    used_bins = []

    for bin in bins:
        if not pieces:  
            break
        
        pieces = bin.pack(pieces)

        if bin.n_placed > 0:
            used_bins.append(bin)
            for piece in bin.placed_pieces:
                res[piece.id] = (bin.id, piece.get_position())

    for piece in pieces:
        if piece.id not in res:
            res[piece.id] = None
    
    if len(used_bins) > 0:
       plot_part_placements(used_bins, preview_filename)

    return res

def plot_part_placements(bins: list, filename: str, scale_factor: float = 1, width: float = 18, dpi: int = 120):
    """
    Plot contours of placed pieces inside multiple bins arranged vertically.

    Parameters:
    - bins: A list of Bin instances.
    - filename: The file path where the plot will be saved.
    - scale_factor: Factor to scale the plot (not used in this version).
    - width: Fixed width of the plots.
    - dpi: Dots per inch for the saved image.
    """
    num_bins = len(bins)
    height = 3.75 * num_bins  
    fig, axs = plt.subplots(num_bins, 1, figsize=(width, height))

    if num_bins == 1:
        axs = [axs]

    for i, bin in enumerate(bins):
        ax = axs[i]
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

        ax.invert_yaxis()

        ax.grid(False)
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')

        for spine in ax.spines.values():
            spine.set_color('black')

        ax.set_title(f"{bin.id}", fontsize=10)

    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', facecolor='white', dpi=dpi)
    plt.close()
