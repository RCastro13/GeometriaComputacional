import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import plotly as plt
import plotly.graph_objects as go

# Verifica se os pontos formam uma curva para a esquerda
def is_convex(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) > 0

# Verifica se o ponto está dentro do triângulo
def is_point_in_triangle(pt, v1, v2, v3):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0

    return ((b1 == b2) and (b2 == b3))

# Verifica se uma dada sequência de 3 pontos forma uma orelha
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
    steps = []
    triangles = []
    polygon_copy = polygon[:]

    while len(polygon_copy) > 3:
        ears = find_ears(polygon_copy)
        if not ears:
            raise ValueError("No ears found. Polygon might be malformed or not simple.")

        ear_index = ears[0]
        p1 = polygon_copy[ear_index - 1]
        p2 = polygon_copy[ear_index]
        p3 = polygon_copy[(ear_index + 1) % len(polygon_copy)]
        triangles.append([p1, p2, p3])

        steps.append({
            'polygon': polygon[:],
            'ear': [p1, p2, p3]
        })

        del polygon_copy[ear_index]

    triangles.append(polygon_copy)
    return triangles, steps

#plota a triangulação do poligono
def plot_triangulation(polygon, triangles):

    return True


# Exemplo de uso
#polygon = [(1, 1), (2, 1), (4, 4), (5, 1), (7, 3),(6, 6), (3, 8), (1, 6), (0, 3)]

#polygon = [(1, 1),( 2, 1), (2, 2), (4, 2) ,(4, 4), (6, 4) ,(6, 6), (7, 6) ,(7, 7), (5 ,7) ,(5, 5), (3 ,5), (3, 3), (1 ,3)]
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

verticesx = [vertex[0] for vertex in polygon]
verticesy = [vertex[1] for vertex in polygon]

#triangles = triangulate_polygon(polygon)
triangles, steps = triangulate_polygon(polygon)
#print(triangles)
#plot_triangulation(polygon, triangles)
frames = []
for step in steps:
    polygon_trace = go.Scatter(
        x=[p[0] for p in step['polygon']] + [step['polygon'][0][0]],
        y=[p[1] for p in step['polygon']] + [step['polygon'][0][1]],
        mode='lines+markers',
        name='Polygon',
        marker=dict(color='blue')
    )
    ear_trace = go.Scatter(
        x=[p[0] for p in step['ear']] + [step['ear'][0][0]],
        y=[p[1] for p in step['ear']] + [step['ear'][0][1]],
        mode='lines+markers',
        name='Ear',
        marker=dict(color='red', size=10)
    )
    frames.append(go.Frame(data=[polygon_trace, ear_trace]))

# Configura a animação
fig = go.Figure(
    data=[go.Scatter(x=[], y=[])],
    frames=frames,
    layout=go.Layout(
        title="Triangulação de Polígono",
        updatemenus=[{
            'type': 'buttons',
            'buttons': [{
                'label': 'Play',
                'method': 'animate',
                'args': [None, {'frame': {'duration': 1000, 'redraw': True}, 'fromcurrent': True}]
            }]
        }]
    )
)

# Adiciona a configuração inicial do polígono
fig.add_trace(go.Scatter(
    x=[p[0] for p in polygon] + [polygon[0][0]],
    y=[p[1] for p in polygon] + [polygon[0][1]],
    mode='lines+markers',
    name='Polygon',
    marker=dict(color='blue')
))

fig.show()