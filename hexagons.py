import math


def hex_distance(coord_a, coord_b) -> int:
    a_q = coord_a[0]
    a_r = coord_a[1]
    b_q = coord_b[0]
    b_r = coord_b[1]
    return (abs(a_q - b_q) + abs(a_q + a_r - b_q - b_r) + abs(a_r - b_r)) / 2
