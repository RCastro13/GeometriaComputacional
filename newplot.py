import plotly.graph_objects as go
import numpy as np

import math

def is_convex(polygon):
    """Verifica se um polígono é convexo."""
    n = len(polygon)
    if n < 3:
        return False
    
    sign = False
    for i in range(n):
        dx1 = polygon[(i + 2) % n][0] - polygon[(i + 1) % n][0]
        dy1 = polygon[(i + 2) % n][1] - polygon[(i + 1) % n][1]
        dx2 = polygon[i][0] - polygon[(i + 1) % n][0]
        dy2 = polygon[i][1] - polygon[(i + 1) % n][1]
        zcrossproduct = dx1 * dy2 - dy1 * dx2

        if i == 0:
            sign = zcrossproduct > 0
        elif sign != (zcrossproduct > 0):
            return False
    
    return True

def is_ear(polygon, i):
    """Verifica se o vértice i de um polígono é uma orelha."""
    n = len(polygon)
    prev = polygon[(i - 1) % n]
    curr = polygon[i]
    next = polygon[(i + 1) % n]

    # Verifica se o ângulo interno é convexo
    crossproduct = (curr[0] - prev[0]) * (next[1] - curr[1]) - (curr[1] - prev[1]) * (next[0] - curr[0])
    if crossproduct >= 0:
        return False

    # Verifica se não há outros vértices dentro do triângulo formado
    for j in range(n):
        if j != (i - 1) % n and j != i and j != (i + 1) % n:
            if is_point_in_triangle(polygon[j], prev, curr, next):
                return False

    return True

def is_point_in_triangle(pt, v1, v2, v3):
    """Verifica se um ponto pt está dentro do triângulo formado por v1, v2, v3."""
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v2, v3) < 0.0
    b3 = sign(pt, v3, v1) < 0.0

    return ((b1 == b2) and (b2 == b3))

def area_triangle(p1, p2, p3):
    """Calcula a área de um triângulo dado por seus vértices."""
    return abs((p1[0]*(p2[1] - p3[1]) + p2[0]*(p3[1] - p1[1]) + p3[0]*(p1[1] - p2[1])) / 2.0)


def triangulate_polygon(polygon):
    """Realiza a triangulação de um polígono usando o método de corte de orelhas."""
    triangles = []
    remaining_vertices = list(range(len(polygon)))

    while len(remaining_vertices) > 3:
        n = len(remaining_vertices)
        ear_found = False
        
        for i in range(n):
            if is_ear(polygon, remaining_vertices[i]):
                ear_vertex = remaining_vertices[i]
                ear_found = True
                break
        
        if not ear_found:
            raise ValueError("Não foi possível encontrar uma orelha válida.")

        prev_index = (ear_vertex - 1) % n
        next_index = (ear_vertex + 1) % n
        triangles.append((polygon[prev_index], polygon[ear_vertex], polygon[next_index]))
        remaining_vertices.remove(ear_vertex)

    # Último triângulo
    triangles.append((polygon[remaining_vertices[0]], polygon[remaining_vertices[1]], polygon[remaining_vertices[2]]))

    return triangles


def plot_polygon(polygon):
    """Plota um polígono utilizando Plotly."""
    fig = go.Figure()
    
    # Adiciona os vértices do polígono
    x, y = zip(*polygon)
    fig.add_trace(go.Scatter(x=x + (x[0],), y=y + (y[0],), mode='lines', name='Polygon'))

    # Configura layout sem autorange nos eixos
    fig.update_layout(
        title='Triangulação de Polígono com Corte de Orelhas',
        xaxis=dict(range=[min(x) - 1, max(x) + 1]),
        yaxis=dict(range=[min(y) - 1, max(y) + 1]),
    )

    return fig

def animate_triangulation(polygon):
    """Realiza a triangulação de um polígono e anima o processo com Plotly."""
    fig = plot_polygon(polygon)
    fig_frames = []

    remaining_vertices = list(range(len(polygon)))
    triangles = []

    while len(remaining_vertices) > 3:
        n = len(remaining_vertices)
        ear_found = False
        
        for i in range(n):
            if is_ear(polygon, remaining_vertices[i]):
                ear_vertex = remaining_vertices[i]
                ear_found = True
                break
        
        if not ear_found:
            raise ValueError("Não foi possível encontrar uma orelha válida.")

        prev_index = (ear_vertex - 1) % n
        next_index = (ear_vertex + 1) % n
        triangles.append((polygon[prev_index], polygon[ear_vertex], polygon[next_index]))

        # Animação: destaca a orelha encontrada
        x, y = zip(*polygon)
        fig.add_trace(go.Scatter(x=[polygon[prev_index][0], polygon[ear_vertex][0], polygon[next_index][0], polygon[prev_index][0]],
                                 y=[polygon[prev_index][1], polygon[ear_vertex][1], polygon[next_index][1], polygon[prev_index][1]],
                                 mode='lines',
                                 line=dict(color='red'),
                                 name='Ear Highlight',
                                 showlegend=False))

        fig_frames.append(go.Frame(data=[go.Scatter(x=x + (x[0],), y=y + (y[0],), mode='lines', name='Polygon'),
                                         go.Scatter(x=[polygon[prev_index][0], polygon[ear_vertex][0], polygon[next_index][0], polygon[prev_index][0]],
                                                    y=[polygon[prev_index][1], polygon[ear_vertex][1], polygon[next_index][1], polygon[prev_index][1]],
                                                    mode='lines',
                                                    line=dict(color='red'),
                                                    name='Ear Highlight',
                                                    showlegend=False)],
                                   name=f'Step {len(fig_frames)}'))

        remaining_vertices.remove(ear_vertex)

    # Último triângulo
    triangles.append((polygon[remaining_vertices[0]], polygon[remaining_vertices[1]], polygon[remaining_vertices[2]]))

    # Adiciona os triângulos finais
    for triangle in triangles:
        x, y = zip(*triangle)
        fig.add_trace(go.Scatter(x=x + (x[0],), y=y + (y[0],), mode='lines', name='Triangle', line=dict(color='blue')))

    fig.update_layout(
        updatemenus=[{
            "buttons": [
                {"args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": True}],
                 "label": "Play",
                 "method": "animate"},
                {"args": [[None], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate", "transition": {"duration": 0}}],
                 "label": "Pause",
                 "method": "animate"}
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }],
        sliders=[{
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Step:",
                "visible": True,
                "xanchor": "right"
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [{"args": [[f'Step {i}']], "label": f'Step {i}', "method": "animate"} for i in range(len(fig_frames))]
        }],
        title='Triangulação de Polígono com Corte de Orelhas',
    )

    fig.frames = fig_frames
    fig.show()

# Exemplo de uso
polygon = [
    (3.84375, 6.1728515625), (-0.568359375, 5.9921875), (0.7353515625, 9.197265625),
    (5.87109375, 8.4716796875), (5.98046875, 9.8125), (9.7734375, 4.330078125),
    (10.416015625, 7.8349609375), (8.4638671875, 9.9375), (-1.0302734375, 10.91796875),
    (-2.28515625, 7.859375), (-2.802734375, 7.701171875), (-2.05078125, 5.3076171875),
    (-1.138671875, 5.00390625), (-1.27734375, 4.4296875), (-1.052734375, 3.671875),
    (1.283203125, 1.3623046875), (7.44140625, 2.384765625), (10.6484375, 2.19921875),
    (11.85546875, 1.689453125), (6.701171875, 7.7724609375)
]

animate_triangulation(polygon)