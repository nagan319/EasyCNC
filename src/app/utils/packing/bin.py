"""
Author: nagan319
Date: 2024/09/04
"""

from typing import List, Tuple, Union, Dict
import copy

from .utils.area2d import Area2D
from .utils.dimension2d import Dimension2D
from .utils.rectangle2d import Rectangle2D
from .utils.vector2d import Vector2D 

'''
implementation for bin edges:   
    create bin with edge distance parameter == min_dist_from_edge - drill/mill bit diameter
    reduce bin dimension by 2 * edge distance on each axis
    adjust part placements by necessary delta, output
        how is position returned? 
'''

class Bin:
    """ Bin class to handle packing algorithm. """
    def __init__(self, id: str, dimension: Dimension2D, edge_distance: float = 0):
        self.id = id
        self.dimension = Dimension2D(dimension.width, dimension.height)
        self.n_placed: int = 0
        self.placed_pieces: List[Area2D] = []
        self.free_rectangles: List[Rectangle2D] = [
            Rectangle2D(0, 0, self.dimension.width, self.dimension.height)
        ]
        self.edge_distance = edge_distance
        if self.edge_distance > 0:
            self.add_edge_margins()
    
    """ Accessor methods """

    def get_placed_pieces(self) -> List[Area2D]:
        """ Get list of all placed pieces. """
        return self.placed_pieces

    def get_n_placed(self) -> int:
        """ Get number of placed pieces. """
        return self.n_placed    
    
    def get_occupied_area(self) -> float:
        """ Get area occupied by pieces. """
        area = 0
        for piece in self.placed_pieces:
            area += piece.get_area()
        return area

    def get_empty_area(self) -> float:
        """ Get area not occupied by pieces. """
        area = self.dimension.width * self.dimension.height
        for piece in self.placed_pieces:
            area -= piece.get_area()
        return area

    """ Pre-packing placement (existing parts) """

    def add_edge_margins(self):
        """ Add edge margins in the case of a required 'safe edge distance' """
        rectangles = [
            Rectangle2D(
                0,
                0,
                self.dimension.width, 
                self.edge_distance,
            ),
            Rectangle2D(
                0,
                self.dimension.height - self.edge_distance, 
                self.dimension.width,
                self.edge_distance
            ),
            Rectangle2D(
                0, 
                self.edge_distance,
                self.edge_distance,
                self.dimension.height - (2 * self.edge_distance)
            ),
            Rectangle2D(
                self.dimension.width - self.edge_distance,
                self.edge_distance,
                self.edge_distance,
                self.dimension.height - (2 * self.edge_distance)               
            )
        ]
        for i, rect in enumerate(rectangles):
            self.add_immovable_part(Area2D(id=f'edge{i}', shape=rect, shift_to_origin=False))

    def add_immovable_part(self, piece: Area2D):
        """ Adds pre-placed part at indicated coordinate. """
        if piece.get_bb().width > self.dimension.width or piece.get_bb().height > self.dimension.height:
            raise ValueError(f"Attempted to place part of size ({piece.get_bb().width}, {piece.get_bb().height}) given a bin size of ({self.dimension.width}, {self.dimension.height})")
        Bin.update_rectangles(piece, self.free_rectangles)
        self.placed_pieces.append(piece)
        self.n_placed += 1

    """ Packing algorithm """

    def pack(self, to_place: List[Area2D]) -> List[Area2D]:
        """ Main packing strategy. Returns list of unplaced pieces. """
        sorted_pieces = sorted(to_place, key=lambda p: p.get_area(), reverse=True)
        remaining_pieces = []

        occupied_area = Area2D()
        for piece in self.placed_pieces:
            occupied_area.add(Area2D(shape=piece.get_bb()))     

        for piece in sorted_pieces:
            best_placement_idx = Bin.get_best_placement(piece, self.free_rectangles, occupied_area, self.dimension)

            if best_placement_idx != -1:
                best_placement_rectangle = self.free_rectangles[best_placement_idx]
                piece.move(Vector2D(best_placement_rectangle.min_x, best_placement_rectangle.min_y))
                
                Bin.update_rectangles(piece, self.free_rectangles)
                
                self.placed_pieces.append(piece)
                self.n_placed += 1
            else:
                remaining_pieces.append(piece)

        return remaining_pieces

    @staticmethod
    def get_best_placement(piece: Area2D, free_rectangles: List[Rectangle2D], occupied_area: Area2D, bin_dimensions: Dimension2D) -> int:
        """ Iterates through top-left corners of free rectangles, progressing across x and y coordinates.
            Returns the index of the first available position for placement in the original list or -1 if no valid placement is found.
        """
        piece_bb = piece.get_bb()
        indexed_rectangles = [(i, r) for i, r in enumerate(free_rectangles)]
        sorted_indexed_rectangles = sorted(indexed_rectangles, key=lambda item: (item[1].min_x, item[1].min_y))

        for original_idx, rectangle in sorted_indexed_rectangles:
            placed_piece = Area2D(shape=Rectangle2D(rectangle.min_x, rectangle.min_y, piece_bb.width, piece_bb.height))
            if placed_piece.get_bb().fits_inside(rectangle) and not placed_piece.intersection(occupied_area):
                return original_idx 

        return -1 
    
    @staticmethod
    def update_rectangles(piece: Area2D, free_rectangles: List[Rectangle2D]):
        """ Updates free rectangle array to reflect addition of newly-placed piece.
            All affected rectangles are split into up to 4 pieces around the newly-placed piece.
        """
        piece_bb = piece.get_bb()
        to_add = []
        
        for rectangle in free_rectangles[:]:  
            if rectangle.intersects(piece_bb):
                free_rectangles.remove(rectangle)

                margin_values: Dict[str, float] = {
                    'top': max(0, piece_bb.min_y - rectangle.min_y),
                    'right': max(0, rectangle.max_x - piece_bb.max_x),
                    'bottom': max(0, rectangle.max_y - piece_bb.max_y),
                    'left': max(0, piece_bb.min_x - rectangle.min_x)
                }

                '''
                splitting scheme:
                T T T
                L X R
                B B R
                '''
                margin_rectangles: List[Tuple[str, Tuple[float, float, float, float]]] = [
                    ('top', (rectangle.min_x, rectangle.min_y, rectangle.width, margin_values['top'])),
                    ('right', (piece_bb.max_x, piece_bb.min_y, margin_values['right'], rectangle.height - margin_values['top'])),
                    ('bottom', (rectangle.min_x, piece_bb.max_y, rectangle.width - margin_values['right'], margin_values['bottom'])),
                    ('left', (rectangle.min_x, piece_bb.min_y, margin_values['left'], rectangle.height - margin_values['top'] - margin_values['bottom']))
                ]
                
                for margin, rect_params in margin_rectangles:
                    if margin_values[margin] > 0:
                        to_add.append(Rectangle2D(*rect_params))
        
        free_rectangles.extend(to_add)

    def __repr__(self) -> str:
        """Return a string representation of the Bin object."""
        placed_piece_ids = [piece.id for piece in self.placed_pieces]
        return (f"\nBin ID: {self.id}, "
                f"Dimensions: {self.dimension.width}x{self.dimension.height}, "
                f"Placed Pieces: {placed_piece_ids}")
    