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

polygon = [
    (3.84375, 6.1728515625), (-0.568359375, 5.9921875), (0.7353515625, 9.197265625),
    (5.87109375, 8.4716796875), (5.98046875, 9.8125), (9.7734375, 4.330078125),
    (10.416015625, 7.8349609375), (8.4638671875, 9.9375), (-1.0302734375, 10.91796875),
    (-2.28515625, 7.859375), (-2.802734375, 7.701171875), (-2.05078125, 5.3076171875),
    (-1.138671875, 5.00390625), (-1.27734375, 4.4296875), (-1.052734375, 3.671875),
    (1.283203125, 1.3623046875), (7.44140625, 2.384765625), (10.6484375, 2.19921875),
    (11.85546875, 1.689453125), (6.701171875, 7.7724609375), (3.84375, 6.1728515625)
]

verticesx = [vertex[0] for vertex in polygon]
verticesy = [vertex[1] for vertex in polygon]

additionalEdgesX = []
additionalEdgesY = []

frames = []
for i in range(len(verticesx)):
    if is_ear(polygon, i):
        additionalEdgesX.append(verticesx[(i-1) % len(polygon)])
        additionalEdgesX.append(verticesx[(i+1) % len(polygon)])
        additionalEdgesY.append(verticesy[(i-1) % len(polygon)])
        additionalEdgesY.append(verticesy[(i+1) % len(polygon)])

    frames.append(go.Frame(
        data=[
            go.Scatter(x=verticesx, y=verticesy, mode='lines+markers', line=dict(color='black')),
            go.Scatter(x=additionalEdgesX, y=additionalEdgesY, mode='lines', line=dict(color='green')),
            go.Scatter(x=[verticesx[i], verticesx[(i + 1) % len(verticesx)], verticesx[(i + 2) % len(verticesx)]],
                       y=[verticesy[i], verticesy[(i + 1) % len(verticesy)], verticesy[(i + 2) % len(verticesy)]],
                       mode='lines', line=dict(color='blue'))
        ],
        name=f'frame{i}'
    ))

fig = go.Figure(
    data=[
        go.Scatter(x=verticesx, y=verticesy, mode='lines+markers', line=dict(color='black')),
        go.Scatter(x=additionalEdgesX, y=additionalEdgesY, mode='lines', line=dict(color='green')),
        go.Scatter(x=verticesx + [verticesx[0]], y=verticesy + [verticesy[0]], mode='lines', line=dict(color='red'))
    ],
    layout=go.Layout(
        xaxis=dict(range=[min(verticesx) - 1, max(verticesx) + 1], autorange=False),
        yaxis=dict(range=[min(verticesy) - 1, max(verticesy) + 1], autorange=False),
        title="Animating Polygon Edges",
        updatemenus=[{
            "buttons": [
                {"label": "Ear-clipping", "method": "animate", "args": [None, {"frame": {"duration": 2500, "redraw": True}, "fromcurrent": True, "mode": "immediate"}]}
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
                "prefix": "Frame:",
                "visible": True,
                "xanchor": "right"
            },
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [{"label": f"{i}", "method": "animate", "args": [["frame{i}"], {"frame": {"duration": 500, "redraw": True}, "mode": "immediate", "transition": {"duration": 500}}]} for i in range(len(verticesx))]
        }]
    ),
    frames=frames
)

fig.show()