from src.app.utils.packing.bin import Bin
from src.app.utils.packing.utils.area2d import Area2D
from src.app.utils.packing.utils.rectangle2d import Rectangle2D
from src.app.utils.packing.utils.dimension2d import Dimension2D
from src.app.utils.packing.plot import plot_bin

import pytest

@pytest.fixture
def default_bin():
    return Bin(Dimension2D(100, 100))

@pytest.fixture
def placed_pieces():
    return [Area2D(shape=Rectangle2D(0, 0, 50, 50))]

def test_bin_init(default_bin):
    bin = default_bin
    assert bin.dimension.width == default_bin.dimension.width
    assert bin.dimension.height == default_bin.dimension.height
    assert bin.n_placed == 0
    assert bin.placed_pieces == []
    assert bin.free_rectangles[0].width == default_bin.dimension.width
    assert bin.free_rectangles[0].height == default_bin.dimension.height

def test_get_placed_pieces(default_bin, placed_pieces):
    bin = default_bin
    bin.placed_pieces = placed_pieces
    bin.n_placed = len(placed_pieces)
    assert bin.get_placed_pieces() == placed_pieces
    assert bin.get_n_placed() == len(placed_pieces)

def test_get_area(default_bin, placed_pieces):
    bin = default_bin
    assert bin.get_occupied_area() == 0
    assert bin.get_empty_area() == default_bin.dimension.width * default_bin.dimension.height
    bin.placed_pieces = placed_pieces
    assert bin.get_occupied_area() == placed_pieces[0].get_area()
    assert bin.get_empty_area() == default_bin.dimension.width * default_bin.dimension.height - placed_pieces[0].get_area()

""" Tests for update_rectangles """

def test_update_rectangles_all_four():
    bin_dimensions = Dimension2D(width=100, height=100)
    piece = Area2D(shape=Rectangle2D(10, 10, 80, 80))
    bin = Bin(bin_dimensions)
    Bin.update_rectangles(piece, bin.free_rectangles)
    # plot_bin(bin, 'plots/bin_update_rectangles_all_four_sides.png')

def test_update_rectangles_top_corner():
    bin_dimensions = Dimension2D(width=100, height=100)
    piece = Area2D(shape=Rectangle2D(0, 0, 50, 50))
    bin = Bin(bin_dimensions)
    Bin.update_rectangles(piece, bin.free_rectangles)
    # plot_bin(bin, 'plots/bin_update_rectangles_top_corner.png')

""" Tests for get_best_placement """

def test_get_best_placement_case_1():
    piece = Area2D(Rectangle2D(0, 0, 10, 10))
    free_rectangles = [
        Rectangle2D(5, 5, 15, 10),
        Rectangle2D(0, 0, 5, 5),
        Rectangle2D(5, 0, 10, 5),
        Rectangle2D(0, 5, 10, 10),
    ]
    res = Bin.get_best_placement(piece, free_rectangles, Area2D(), Dimension2D(15, 15))
    assert res == 3  # Based on the provided example

def test_get_best_placement_case_2():
    piece = Area2D(Rectangle2D(0, 0, 5, 5))
    free_rectangles = [
        Rectangle2D(5, 5, 15, 15),
        Rectangle2D(0, 0, 10, 10),
        Rectangle2D(10, 0, 10, 10),
    ]
    res = Bin.get_best_placement(piece, free_rectangles, Area2D(), Dimension2D(20, 20))
    assert res == 1  # The piece fits perfectly in the second rectangle (index 1)

def test_get_best_placement_case_3():
    piece = Area2D(Rectangle2D(0, 0, 12, 12))
    free_rectangles = [
        Rectangle2D(5, 5, 10, 10),
        Rectangle2D(0, 0, 15, 15),
        Rectangle2D(20, 20, 10, 10),
    ]
    res = Bin.get_best_placement(piece, free_rectangles, Area2D(), Dimension2D(25, 25))
    assert res == 1  # The piece fits perfectly in the second rectangle (index 1)

def test_get_best_placement_case_4():
    piece = Area2D(Rectangle2D(0, 0, 8, 8))
    free_rectangles = [
        Rectangle2D(0, 0, 8, 8),
        Rectangle2D(5, 5, 20, 20),
        Rectangle2D(15, 15, 10, 10),
    ]
    res = Bin.get_best_placement(piece, free_rectangles, Area2D(), Dimension2D(30, 30))
    assert res == 0  # The piece fits perfectly in the first rectangle (index 0)

def test_get_best_placement_case_5():
    piece = Area2D(Rectangle2D(0, 0, 10, 10))
    free_rectangles = [
        Rectangle2D(20, 20, 15, 15),
        Rectangle2D(0, 0, 15, 15),
        Rectangle2D(10, 10, 5, 5),
    ]
    res = Bin.get_best_placement(piece, free_rectangles, Area2D(), Dimension2D(30, 30))
    assert res == 1  # The piece fits perfectly in the second rectangle (index 1)

def test_get_best_placement_case_no_fit():
    piece = Area2D(Rectangle2D(0, 0, 20, 20))
    free_rectangles = [
        Rectangle2D(5, 5, 10, 10),
        Rectangle2D(0, 0, 15, 15),
        Rectangle2D(30, 30, 5, 5),
    ]
    res = Bin.get_best_placement(piece, free_rectangles, Area2D(), Dimension2D(40, 40))
    assert res == -1  # The piece cannot fit into any of the rectangles

def test_get_best_placement_case_edge():
    piece = Area2D(Rectangle2D(0, 0, 20, 20))
    free_rectangles = [
        Rectangle2D(0, 0, 20, 20),
        Rectangle2D(10, 10, 15, 15),
        Rectangle2D(5, 5, 25, 25),
    ]
    res = Bin.get_best_placement(piece, free_rectangles, Area2D(), Dimension2D(30, 30))
    assert res == 0  # The piece fits perfectly in the first rectangle (index 0)

""" Tests for pack """
def test_pack_basic():
    bin = Bin(Dimension2D(100, 100))
    pieces = [
        Area2D(Rectangle2D(0, 0, 10, 10)),
        Area2D(Rectangle2D(0, 0, 80, 80)),
        Area2D(Rectangle2D(0, 0, 20, 20))
    ]
    bin.pack(pieces)
    # plot_bin(bin, 'plots/packed_basic.png')

def test_pack_no_pieces():
    bin = Bin(Dimension2D(100, 100))
    pieces = []
    bin.pack(pieces)
    # plot_bin(bin, 'plots/packed_no_pieces.png')

def test_pack_one_large_piece():
    bin = Bin(Dimension2D(100, 100))
    pieces = [Area2D(Rectangle2D(0, 0, 100, 100))]
    bin.pack(pieces)
    # plot_bin(bin, 'plots/packed_one_large_piece.png')

def test_pack_large_piece():
    bin = Bin(Dimension2D(100, 100))
    pieces = [Area2D(Rectangle2D(0, 0, 120, 120))]
    bin.pack(pieces)
    # plot_bin(bin, 'plots/packed_large_piece.png')

def test_pack_identical_pieces():
    bin = Bin(Dimension2D(100, 100))
    pieces = [Area2D(Rectangle2D(0, 0, 10, 10)), Area2D(Rectangle2D(0, 0, 10, 10)), Area2D(Rectangle2D(0, 0, 10, 10)), Area2D(Rectangle2D(0, 0, 10, 10)), Area2D(Rectangle2D(0, 0, 10, 10)), Area2D(Rectangle2D(0, 0, 10, 10)), Area2D(Rectangle2D(0, 0, 10, 10)), Area2D(Rectangle2D(0, 0, 10, 10)), Area2D(Rectangle2D(0, 0, 10, 10)), Area2D(Rectangle2D(0, 0, 10, 10))] 
    bin.pack(pieces)
    # plot_bin(bin, 'plots/packed_identical_pieces.png')

def test_pack_irregular_pieces():
    bin = Bin(Dimension2D(150, 150))
    pieces = [
        Area2D(Rectangle2D(0, 0, 50, 50)),
        Area2D(Rectangle2D(0, 0, 70, 30)),
        Area2D(Rectangle2D(0, 0, 20, 60)),
        Area2D(Rectangle2D(0, 0, 40, 40))
    ]
    bin.pack(pieces)
    # plot_bin(bin, 'plots/packed_irregular_pieces.png')

def test_pack_perfect_fit():
    bin = Bin(Dimension2D(200, 200))
    pieces = [
        Area2D(Rectangle2D(0, 0, 100, 100)),
        Area2D(Rectangle2D(100, 0, 100, 100))
    ]
    bin.pack(pieces)
    # plot_bin(bin, 'plots/packed_perfect_fit.png')
