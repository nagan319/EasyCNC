import os
import matplotlib.pyplot as plt

import numpy as np
from scipy.stats import norm

import random

from src.app.utils.packing.bin import Bin
from src.app.utils.packing.utils.dimension2d import Dimension2D
from src.app.utils.packing.utils.area2d import Area2D
from src.app.utils.packing.utils.rectangle2d import Rectangle2D
from src.app.utils.packing.utils.plot_for_testing import plot_bin

import pytest

DIR_NAME = 'efficiency plots'

@pytest.fixture
def preview_directory():
    parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'packing algo preview')
    efficiency_dir = os.path.join(parent_dir, DIR_NAME)
    os.makedirs(efficiency_dir, exist_ok=True)
    return efficiency_dir


def generate_random_pieces(bin_width, bin_height, max_percent_size = 0.5):
    pieces = []
    area = 0
    while area < bin_width * bin_height:
        width = random.uniform(1, bin_width * max_percent_size)
        height = random.uniform(1, bin_height * max_percent_size)
        pieces.append(Area2D(id='piece', shape=Rectangle2D(0, 0, width, height)))
        area += width * height
    return pieces

def test_efficiency(preview_directory):
    bin_width = 100
    bin_height = 100
    num_iterations = 128
    efficiency_list = []

    print("\n\n")

    for i in range(num_iterations):
        bin = Bin('id', Dimension2D(bin_width, bin_height))
        pieces = generate_random_pieces(bin_width, bin_height, 0.25)
        bin.pack(pieces)
        total_area = bin_width * bin_height
        empty_area = bin.get_empty_area()
        efficiency = (1 - empty_area / total_area) * 100
        efficiency_list.append(efficiency)
        plot_bin(bin, os.path.join(preview_directory, f'bin_plot_{i}.png'))
        percentage = i / num_iterations * 100
        progress_bar = '*' * int(round(percentage))
        print(f"\r{percentage:.2f}% {progress_bar}", end="")

    print()
    
    # Compute statistics
    mean_efficiency = np.mean(efficiency_list)
    std_dev_efficiency = np.std(efficiency_list)
    min_efficiency = min(efficiency_list)
    max_efficiency = max(efficiency_list)
    min_index = efficiency_list.index(min_efficiency)
    max_index = efficiency_list.index(max_efficiency)

    print("\n\n")
    print(f"Mean efficiency: {mean_efficiency:.2f}%")
    print(f"Standard deviation: {std_dev_efficiency:.2f}%")
    print(f"Min efficiency: {min_efficiency:.2f}% @ Iteration {min_index}")
    print(f"Max efficiency: {max_efficiency:.2f}% @ Iteration {max_index}")
    
    # Plot histogram with normal curve
    plt.figure()
    
    # Define bins to represent 1% intervals
    bins = np.arange(0, 101, 1)
    
    # Plot histogram
    counts, bins, patches = plt.hist(efficiency_list, bins=bins, edgecolor='black', density=True, alpha=0.6)
    
    # Add normal distribution curve
    bin_centers = 0.5 * (bins[1:] + bins[:-1])
    normal_curve = norm.pdf(bin_centers, mean_efficiency, std_dev_efficiency)
    plt.plot(bin_centers, normal_curve, 'r--', label='Normal Distribution')
    
    # Set x-axis limits to show only a few percent from the edges
    plt.xlim(max(0, mean_efficiency - 3*std_dev_efficiency), min(100, mean_efficiency + 3*std_dev_efficiency))
    
    # Add mean and standard deviation lines
    plt.axvline(mean_efficiency, color='blue', linestyle='--', label=f'Mean: {mean_efficiency:.2f}%')
    plt.axvline(mean_efficiency - std_dev_efficiency, color='green', linestyle='--', label=f'-1 Std Dev: {mean_efficiency - std_dev_efficiency:.2f}%')
    plt.axvline(mean_efficiency + std_dev_efficiency, color='green', linestyle='--', label=f'+1 Std Dev: {mean_efficiency + std_dev_efficiency:.2f}%')
    
    plt.xlabel('Packing Efficiency (%)')
    plt.ylabel('Density')
    plt.title('Histogram of Packing Efficiencies with Normal Curve')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(preview_directory, 'packing_efficiency_histogram_with_curve.png'))
    plt.close()
