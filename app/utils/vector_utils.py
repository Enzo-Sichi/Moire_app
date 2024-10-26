import streamlit as st
import plotly.graph_objects as go
import numpy as np
from typing import List, Tuple, Dict
from itertools import product

def create_frequency_vectors(pattern_type: str, frequencies: List[float], angles: List[float]) -> List[Dict]:
    vectors = []
    for i, (f, theta) in enumerate(zip(frequencies, angles)):
        x = f * np.cos(np.radians(theta))
        y = f * np.sin(np.radians(theta))
        base_vector = np.array([x, y])
        
        if 'Dot' in pattern_type:
            # For dot patterns, create two perpendicular vectors
            perp_vector = np.array([-y, x])  # Perpendicular vector
            vectors.append({'vector': base_vector, 'index': i, 'intensity': 1.0, 'direction': 'horizontal'})
            vectors.append({'vector': perp_vector, 'index': i, 'intensity': 1.0, 'direction': 'vertical'})
        else:
            vectors.append({'vector': base_vector, 'index': i, 'intensity': 1.0, 'direction': None})
    return vectors

def create_all_vectors(base_vectors, nHarmonics):
    all_vectors = []

    # Generate all possible combinations of harmonics for the number of base vectors
    harmonic_range = range(-nHarmonics, nHarmonics + 1)
    harmonic_combinations = product(harmonic_range, repeat=len(base_vectors))

    # Iterate over each combination of harmonic coefficients
    for combination in harmonic_combinations:
        # Create a new vector object with initial values
        vector = {'vector': np.array([0.0, 0.0]), 'coordinates': [], 'intensity': 1.0}

        # Loop over each base vector and corresponding harmonic coefficient
        for harmonic, base_vector in zip(combination, base_vectors):
            vector['vector'] += harmonic * base_vector['vector']
            vector['coordinates'].append(harmonic)
            vector['intensity'] *= base_vector['intensity']

        # Add the generated vector to the list of all vectors
        all_vectors.append(vector)

    return all_vectors

def is_within_visibility_disk(vector: np.ndarray, disk_radius: float) -> bool:
    return np.linalg.norm(vector) <= disk_radius
