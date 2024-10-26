import streamlit as st
import plotly.graph_objects as go
import numpy as np
from typing import List, Tuple, Dict
from itertools import product

def create_pattern(size: int, frequency: float, angle: float, pattern_type: str) -> np.ndarray:
    x = np.linspace(-size/2, size/2, size)
    y = np.linspace(-size/2, size/2, size)
    X, Y = np.meshgrid(x, y)
    
    theta = np.radians(angle)
    X_rot = X * np.cos(theta) + Y * np.sin(theta)
    Y_rot = -X * np.sin(theta) + Y * np.cos(theta)
    
    if 'Dot' in pattern_type:
        return ((X_rot % (size/frequency) < size/(2*frequency)) & 
                (Y_rot % (size/frequency) < size/(2*frequency)))
    else:
        return X_rot % (size/frequency) < size/(2*frequency)