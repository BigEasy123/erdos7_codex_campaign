#!/usr/bin/env python3
"""Safe compact consequences of a dual Benders inequality."""
import math
import numpy as np


def derive_compact(g, rhs, tol=1e-12):
    """Yield valid subset caps implied by ``sum(g_i e_i) <= rhs`` for binary e."""
    coefficients = np.asarray(g, dtype=float)
    negative_floor = float(np.minimum(coefficients, 0.0).sum())
    positive = sorted({float(value) for value in coefficients if value > tol})
    for threshold in positive:
        indices = tuple(int(index) for index, value in enumerate(coefficients)
                        if value + tol >= threshold)
        cap = math.floor((float(rhs) - negative_floor + tol) / threshold)
        if cap < len(indices):
            yield indices, cap