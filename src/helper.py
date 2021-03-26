import numpy as np


def kth_diag_indices(a, k):
	"""Get diagonal indices using an offset.
	
	:param a: given array
	:type a: array
	:param k: offset
	:type k: int
	:return: tuple of rows and cols indices for diagonals
	:rtype: tuple
	"""
    rows, cols = np.diag_indices_from(a)
    if k < 0:
        return rows[-k:], cols[:k]
    elif k > 0:
        return rows[:-k], cols[k:]
    else:
        return rows, cols
