import networkx as nx
import plotly.graph_objects as go
import pandas as pd

# Passo 1: Definir o polígono (uma lista de vértices em ordem)
polygon = [
    (3.84375, 6.1728515625), (-0.568359375, 5.9921875), (0.7353515625, 9.197265625),
    (5.87109375, 8.4716796875), (5.98046875, 9.8125), (9.7734375, 4.330078125),
    (10.416015625, 7.8349609375), (8.4638671875, 9.9375), (-1.0302734375, 10.91796875),
    (-2.28515625, 7.859375), (-2.802734375, 7.701171875), (-2.05078125, 5.3076171875),
    (-1.138671875, 5.00390625), (-1.27734375, 4.4296875), (-1.052734375, 3.671875),
    (1.283203125, 1.3623046875), (7.44140625, 2.384765625), (10.6484375, 2.19921875),
    (11.85546875, 1.689453125), (6.701171875, 7.7724609375)
]

# Função para verificar se três pontos são convexos
def is_convex(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) > 0

def triangle_area(a, b, c):
    return abs((a[0]*b[1] + b[0]*c[1] + c[0]*a[1]) - (a[1]*b[0] + b[1]*c[0] + c[1]*a[0])) / 2

def is_point_in_triangle(p, a, b, c):
    # Usa o método da área para verificar
    area_orig = triangle_area(a, b, c)
    area1 = triangle_area(p, b, c)
    area2 = triangle_area(p, a, c)
    area3 = triangle_area(p, a, b)
    return abs(area_orig - (area1 + area2 + area3)) < 1e-10

# Função auxiliar para verificar se três pontos formam uma orelha
def is_ear(polygon, i):
    a, b, c = polygon[i-1], polygon[i], polygon[(i+1) % len(polygon)]
    # Verifica se b é um vértice convexo
    if not is_convex(a, b, c):
        return False
    # Verifica se nenhum outro vértice está dentro do triângulo abc
    for p in polygon:
        if p not in (a, b, c) and is_point_in_triangle(p, a, b, c):
            return False
    return True

# Passo 3: Implementar o algoritmo de corte de orelhas
def ear_clipping_triangulation(polygon, edgesDf, vertexDf):
    triangles = []
    poly = polygon[:]
    currentEdges = []
    while len(poly) > 3:
        for i in range(len(poly)):
            if is_ear(poly, i):
                p1, p2, p3 = poly[i-1], poly[i], poly[(i+1) % len(poly)]
                triangles.append((p1, p2, p3))
                edgesArray = [p1, p2, p3]
                
                for edge in edgesArray:
                    if edge != p2:
                        additionalEdgesX.append(edge[0])
                        additionalEdgesY.append(edge[1])

                frames.append(go.Frame(
                    data=[
                        go.Scatter(x=verticesx, y=verticesy, mode='lines+markers+text', line=dict(color='black'), text=[str(i) for i in range(len(polygon))] + [str(0)], textposition='top right'),
                        go.Scatter(x=additionalEdgesX, y=additionalEdgesY, mode='lines', line=dict(color='blue')),
                        go.Scatter(x=erasedEdgesX, y=erasedEdgesY, mode='lines', line=dict(color='lightgray')),
                        go.Scatter(x=[p1[0], p2[0], p3[0]], y=[p1[1], p2[1], p3[1]], mode='markers+lines', line=dict(color='red')),
                        
                                      
                    ],
                    name=f'frame{len(frames)}'
                ))
                for edge in edgesArray:
                    erasedEdgesX.append(edge[0])
                    erasedEdgesY.append(edge[1])
                
                del poly[i]
                G.add_edge(p1, p3)  # Adiciona a aresta do triângulo no grafo
                break

    triangles.append((poly[0], poly[1], poly[2]))
    return triangles

# Passo 2: Criar o grafo representando o polígono
G = nx.Graph()
for i in range(len(polygon)):
    G.add_edge(polygon[i], polygon[(i+1) % len(polygon)])

# Criando o DataFrame para os vértices
vertices = []
for i, (x, y) in enumerate(polygon):
    # Índices dos vizinhos (considerando vizinhos diretos)
    vizinhos = [(i - 1) % len(polygon), (i + 1) % len(polygon)]  # Circular
    vertices.append({
        'index': i,
        'x': x,
        'y': y,
        'index_vizinhos': vizinhos,
        'cor': 'black'  # Você pode definir a cor que desejar
    })

vertexDf = pd.DataFrame(vertices)

# Criando o DataFrame para as arestas
arestas = []
for i in range(len(polygon)):
    x1, y1 = polygon[i]
    x2, y2 = polygon[(i + 1) % len(polygon)]  # Aresta até o próximo vértice
    arestas.append({
        'index': i,
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2,
        'cor': 'black'  # Defina a cor desejada
    })

edgesDf = pd.DataFrame(arestas)

# Passo 4: Executar a triangulação e exibir os resultados
frames = []
verticesx = [coord[0] for coord in G.nodes]
verticesy = [coord[1] for coord in G.nodes]
verticesx.append(verticesx[0])
verticesy.append(verticesy[0])

additionalEdgesX = []
additionalEdgesY = []
erasedEdgesX = []
erasedEdgesY = []
triangles = ear_clipping_triangulation(polygon, edgesDf, vertexDf)

fig = go.Figure(
    data=[
        go.Scatter(x=verticesx, y=verticesy, mode='lines+markers+text', line=dict(color='black'), text=[str(i) for i in range(len(polygon))] + [str(0)], textposition='top right'),
        go.Scatter(x=erasedEdgesX, y=erasedEdgesY, mode='lines', line=dict(color='lightgray')),
        go.Scatter(x=additionalEdgesX, y=additionalEdgesY, mode='lines', line=dict(color='blue')),
        go.Scatter(x=verticesx + [verticesx[0]], y=verticesy + [verticesy[0]], mode='lines', line=dict(color='black'))
    ],
    layout=go.Layout(
        xaxis=dict(range=[min(verticesx) - 1, max(verticesx) + 1], autorange=False),
        yaxis=dict(range=[min(verticesy) - 1, max(verticesy) + 1], autorange=False),
        title="Animating Polygon Edges",
        updatemenus=[{
            "buttons": [
                {
                    "label": "Play", 
                    "method": "animate", 
                    "args": [None, {"frame": {"duration": 2000, "redraw": True}, "fromcurrent": True, "mode": "immediate"}]
                },
                {
                    'label': 'Pause',
                    'method': 'animate',
                    'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate', 'transition': {'duration': 0}}]
                }
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
            "steps": [{"label": f"{i}", "method": "animate", "args": [["frame{i}"], {"frame": {"duration": 500, "redraw": True}, "mode": "immediate", "transition": {"duration": 500}}]} for i in range(len(frames))]
        }]
    ),
    frames=frames
)

fig.show()