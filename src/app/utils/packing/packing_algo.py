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
    bit_diameter: float,
    min_edge_distance: float,
    preview_filename: str,
    conversion_factor: float = 1.0
) -> Dict[str, Union[None, Tuple[str, Tuple[float, float]]]]:
    """
    Packs pieces into bins and returns their placements.

    Parameters:
        input_bins: List of tuples containing (bin_id, dimensions, contours).
        input_pieces: List of tuples containing (piece_id, contours).
        preview_filename: File to save preview
        bit_diameter: max of drill and mill bit diameter (tolerance on side of each piece)
        edge_tolerance: minimum distance from edge of plate

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
                shift_to_origin=False,
                edge_margin=bit_diameter
            )
            bin_obj.add_immovable_part(part) 
        bins.append(bin_obj)
    
    for piece in input_pieces:
        piece_id, outer_contour = piece
        pieces.append(
            Area2D(
                id=piece_id, 
                points=outer_contour, 
                edge_margin=bit_diameter
            )
        )

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
                x, y = piece.get_position()
                res[piece.id] = (
                    bin.id, 
                    (x, y)
                )

    for piece in pieces:
        if piece.id not in res:
            res[piece.id] = None
    
    if len(used_bins) > 0:
       plot_part_placements(used_bins, preview_filename, conversion_factor=conversion_factor)

    return res

def plot_part_placements(bins: list, filename: str, scale_factor: float = 1, width: float = 18, dpi: int = 120, conversion_factor: float = 1.0, bin_height: float = 3.75):
    """
    Plot contours of placed pieces inside multiple bins arranged vertically.

    Parameters:
    - bins: A list of Bin instances.
    - filename: The file path where the plot will be saved.
    - scale_factor: Factor to scale the plot (not used in this version).
    - width: Fixed width of the plots (in inches or other units after conversion).
    - dpi: Dots per inch for the saved image.
    - conversion_factor: Factor to scale bin and piece dimensions (e.g., convert from millimeters to inches, or scale by other units).
    - bin_height: Fixed height of each bin plot (default 3.75 units).
    """

    fig_width = width
    fig_height_per_bin = bin_height
    total_fig_height = fig_height_per_bin * len(bins)

    fig, axs = plt.subplots(len(bins), 1, figsize=(fig_width, total_fig_height), dpi=dpi)

    if len(bins) == 1:
        axs = [axs]

    for i, bin in enumerate(bins):
        ax = axs[i]
        ax.set_facecolor('white')

        bin_width = bin.dimension.width * conversion_factor
        bin_height = bin.dimension.height * conversion_factor

        bin_patch = patches.Rectangle(
            (0, 0), 
            bin_width,
            bin_height,
            edgecolor='black',
            facecolor='none',
            linewidth=2,
            linestyle='-'
        )
        ax.add_patch(bin_patch)

        text_plot_offset = 4

        for piece in bin.get_placed_pieces():
            piece_shape = piece.shape
            shape_patch = patches.Polygon(
                [(x * conversion_factor, y * conversion_factor) for x, y in piece_shape.exterior.coords],
                edgecolor='black',
                facecolor='none',
                linewidth=2,
                linestyle='-'
            )
            ax.add_patch(shape_patch)

            piece_bb = piece.get_bb()
            bbox_patch = patches.Rectangle(
                (piece_bb.min_x * conversion_factor, piece_bb.min_y * conversion_factor),
                piece_bb.width * conversion_factor,
                piece_bb.height * conversion_factor,
                edgecolor='blue',
                facecolor='none',
                linewidth=1,
                linestyle='--'
            )
            ax.add_patch(bbox_patch)

            label_x = (piece_bb.min_x + text_plot_offset) * conversion_factor
            label_y = (piece_bb.min_y + text_plot_offset) * conversion_factor

            display_text = 'ctr'+piece.id.split('ctr')[1] if 'ctr' in piece.id else piece.id[:4] + '...' + piece.id[-4:]

            ax.text(
                label_x, label_y,
                display_text, 
                verticalalignment='top', horizontalalignment='left',
                fontsize=8, color='white', bbox=dict(facecolor='blue', edgecolor='none', alpha=1)
            )

        for idx, free_rect in enumerate(bin.free_rectangles):
            rect_patch = patches.Rectangle(
                (free_rect.min_x * conversion_factor, free_rect.min_y * conversion_factor),
                free_rect.width * conversion_factor,
                free_rect.height * conversion_factor,
                edgecolor='green',  
                facecolor='none',
                linewidth=1,
                linestyle=':'
            )
            ax.add_patch(rect_patch)

            label_x = (free_rect.min_x + text_plot_offset) * conversion_factor 
            label_y = (free_rect.min_y + text_plot_offset) * conversion_factor 

            ax.text(
                label_x, label_y,
                f'{idx}', 
                verticalalignment='top', horizontalalignment='left',
                fontsize=8, color='white', bbox=dict(facecolor='green', edgecolor='none', alpha=1)
            )

        ax.set_xlim(0, bin_width)
        ax.set_ylim(0, bin_height)
        ax.set_aspect('equal')

        ax.invert_yaxis()

        ax.grid(False)
        ax.tick_params(axis='x', colors='black')
        ax.tick_params(axis='y', colors='black')
        for spine in ax.spines.values():
            spine.set_color('black')

        ax.set_title(f"Bin {bin.id}", fontsize=10)

    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight', facecolor='white', dpi=dpi)
    plt.close()

