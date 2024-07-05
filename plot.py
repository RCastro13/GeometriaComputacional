import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import plotly

def is_convex(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) > 0

def is_point_in_triangle(pt, v1, v2, v3):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0

    return ((b1 == b2) and (b2 == b3))

def is_ear(polygon, i):
    p1 = polygon[i - 1]
    p2 = polygon[i]
    p3 = polygon[(i + 1) % len(polygon)]

    if not is_convex(p1, p2, p3):
        return False

    for j in range(len(polygon)):
        if j in [i - 1, i, (i + 1) % len(polygon)]:
            continue
        if is_point_in_triangle(polygon[j], p1, p2, p3):
            return False

    return True

def find_ears(polygon):
    ears = []
    for i in range(len(polygon)):
        if is_ear(polygon, i):
            ears.append(i)
    return ears

def triangulate_polygon(polygon):
    triangles = []
    polygon = polygon[:]

    while len(polygon) > 3:
        ears = find_ears(polygon)
        if not ears:
            raise ValueError("No ears found. Polygon might be malformed or not simple.")

        ear_index = ears[0]
        p1 = polygon[ear_index - 1]
        p2 = polygon[ear_index]
        p3 = polygon[(ear_index + 1) % len(polygon)]
        triangles.append([p1, p2, p3])

        del polygon[ear_index]

    triangles.append(polygon)
    return triangles

def plot_polygon_and_triangulation(polygon, triangles):
    fig, ax = plt.subplots()
    polygon_patch = Polygon(polygon, closed=True, fill=None, edgecolor='r')
    ax.add_patch(polygon_patch)

    for triangle in triangles:
        triangle_patch = Polygon(triangle, closed=True, fill=None, edgecolor='b')
        ax.add_patch(triangle_patch)

    ax.set_xlim(-10, 20)
    ax.set_ylim(0, 12)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig('grafico.png')

# Exemplo de uso
#polygon = [(1, 1), (2, 1), (4, 4), (5, 1), (7, 3),(6, 6), (3, 8), (1, 6), (0, 3)]

polygon = [(1, 1),( 2, 1), (2, 2), (4, 2) ,(4, 4), (6, 4) ,(6, 6), (7, 6) ,(7, 7), (5 ,7) ,(5, 5), (3 ,5), (3, 3), (1 ,3)]
#polygon = [(2, 2), (4, 4), (6, 2), (8, 5), (6, 8), (4, 6), (2, 8), (0, 5)]
polygon = [
    (3.84375, 6.1728515625), (-0.568359375, 5.9921875), (0.7353515625, 9.197265625),
    (5.87109375, 8.4716796875), (5.98046875, 9.8125), (9.7734375, 4.330078125),
    (10.416015625, 7.8349609375), (8.4638671875, 9.9375), (-1.0302734375, 10.91796875),
    (-2.28515625, 7.859375), (-2.802734375, 7.701171875), (-2.05078125, 5.3076171875),
    (-1.138671875, 5.00390625), (-1.27734375, 4.4296875), (-1.052734375, 3.671875),
    (1.283203125, 1.3623046875), (7.44140625, 2.384765625), (10.6484375, 2.19921875),
    (11.85546875, 1.689453125), (6.701171875, 7.7724609375)
]
triangles = triangulate_polygon(polygon)
#print(triangles)
plot_polygon_and_triangulation(polygon, triangles)
