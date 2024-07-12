import plotly.graph_objects as go
import networkx as nx
import numpy as np

# Função para criar o grafo a partir dos triângulos fornecidos
def create_graph_from_triangles(triangles):
    G = nx.Graph()
    for triangle in triangles:
        for i in range(3):
            G.add_edge(triangle[i], triangle[(i + 1) % 3])
    return G

# Função para colorir o grafo usando 3-coloração
def three_color_graph(G):
    color_map = {}
    for node in G.nodes():
        available_colors = {0, 1, 2} - {color_map.get(neigh) for neigh in G.neighbors(node)}
        color_map[node] = min(available_colors)
    return color_map

# Função para criar a animação
def create_animation(triangles, color_map):
    fig = go.Figure()
    
    # Configuração inicial do layout
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
    )

    # Adiciona o primeiro frame com todos os triângulos desenhados sem coloração
    for triangle in triangles:
        x_coords = [point[0] for point in triangle] + [triangle[0][0]]
        y_coords = [point[1] for point in triangle] + [triangle[0][1]]
        fig.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='lines', line=dict(color='black')))

    frames = []
    for step, triangle in enumerate(triangles):
        frame_data = []
        
        for i, tri in enumerate(triangles):
            x_coords = [point[0] for point in tri] + [tri[0][0]]
            y_coords = [point[1] for point in tri] + [tri[0][1]]
            
            if i <= step:
                vertex_colors = [color_map[tri[0]], color_map[tri[1]], color_map[tri[2]]]
                for j, vertex in enumerate(tri):
                    frame_data.append(go.Scatter(
                        x=[vertex[0]],
                        y=[vertex[1]],
                        mode='markers',
                        marker=dict(size=10, color=['red', 'green', 'blue'][vertex_colors[j]]),
                    ))
            
            frame_data.append(go.Scatter(x=x_coords, y=y_coords, mode='lines', line=dict(color='blue')))

        frames.append(go.Frame(data=frame_data))
    
    fig.frames = frames
    
    fig.update_layout(
        updatemenus=[{
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 1500, 'redraw': True}, 'fromcurrent': True}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'showactive': False,
            'type': 'buttons'
        }]
    )

    fig.show()

# Exemplo de entrada de triângulos
triangles = [
    ((0.7353515625, 9.197265625), (5.87109375, 8.4716796875), (5.98046875, 9.8125)),
    ((5.98046875, 9.8125), (9.7734375, 4.330078125), (10.416015625, 7.8349609375)),
    ((5.98046875, 9.8125), (10.416015625, 7.8349609375), (8.4638671875, 9.9375)),
    ((5.98046875, 9.8125), (8.4638671875, 9.9375), (-1.0302734375, 10.91796875)),
    ((0.7353515625, 9.197265625), (5.98046875, 9.8125), (-1.0302734375, 10.91796875)),
    ((-0.568359375, 5.9921875), (0.7353515625, 9.197265625), (-1.0302734375, 10.91796875)),
    ((-0.568359375, 5.9921875), (-1.0302734375, 10.91796875), (-2.28515625, 7.859375)),
    ((-0.568359375, 5.9921875), (-2.28515625, 7.859375), (-2.802734375, 7.701171875)),
    ((-0.568359375, 5.9921875), (-2.802734375, 7.701171875), (-2.05078125, 5.3076171875)),
    ((3.84375, 6.1728515625), (-0.568359375, 5.9921875), (-2.05078125, 5.3076171875)),
    ((3.84375, 6.1728515625), (-2.05078125, 5.3076171875), (-1.138671875, 5.00390625)),
    ((3.84375, 6.1728515625), (-1.138671875, 5.00390625), (-1.27734375, 4.4296875)),
    ((3.84375, 6.1728515625), (-1.27734375, 4.4296875), (-1.052734375, 3.671875)),
    ((3.84375, 6.1728515625), (-1.052734375, 3.671875), (1.283203125, 1.3623046875)),
    ((6.701171875, 7.7724609375), (3.84375, 6.1728515625), (1.283203125, 1.3623046875)),
    ((6.701171875, 7.7724609375), (1.283203125, 1.3623046875), (7.44140625, 2.384765625)),
    ((6.701171875, 7.7724609375), (7.44140625, 2.384765625), (10.6484375, 2.19921875)),
    ((10.6484375, 2.19921875), (11.85546875, 1.689453125), (6.701171875, 7.7724609375))
]

# Criação do grafo e aplicação da 3-coloração
G = create_graph_from_triangles(triangles)
color_map = three_color_graph(G)

# Criação da animação
create_animation(triangles, color_map)
