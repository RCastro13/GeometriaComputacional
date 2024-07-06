import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import plotly
import plotly.graph_objects as go

BRANCO = 0
AZUL = 1
VERMELHO = 2
AMARELO = 3

class Dot:
    def __init__(self, x, y):
        self.color = BRANCO
        self.x = x
        self.y = y
        self.visitedForCount = 0
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))

class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

def create_dots_and_triangles(triangle_list):
    triangles = []
    dots_set = set()
    
    # Create Dot objects
    for triangle in triangle_list:
        for point in triangle:
            dot = Dot(point[0], point[1])
            dots_set.add(dot)
    
    # Create Triangle objects
    for triangle in triangle_list:
        a = next(dot for dot in dots_set if dot.x == triangle[0][0] and dot.y == triangle[0][1])
        b = next(dot for dot in dots_set if dot.x == triangle[1][0] and dot.y == triangle[1][1])
        c = next(dot for dot in dots_set if dot.x == triangle[2][0] and dot.y == triangle[2][1])
        triangles.append(Triangle(a, b, c))
    
    return triangles

# def create_adjacency_list(triangle_list):
#     adjacency_list = {}
    
#     # Constrói a lista de adjacência
#     for triangle in triangle_list:
#         for point in triangle:
#             if point not in adjacency_list:
#                 adjacency_list[point] = []
    
#     # Preenche os vizinhos para cada ponto
#     for triangle in triangle_list:
#         p1, p2, p3 = triangle
#         adjacency_list[p1].extend([p2, p3])
#         adjacency_list[p2].extend([p1, p3])
#         adjacency_list[p3].extend([p1, p2])
    
#     # Remove duplicatas nos vizinhos
#     for point in adjacency_list:
#         adjacency_list[point] = list(set(adjacency_list[point]))
    
#     return adjacency_list

# def welsh_powell(graph):
#     # Ordena os vértices por grau decrescente
#     vertices = sorted(graph.keys(), key=lambda x: len(graph[x]), reverse=True)
    
#     # Dicionário para armazenar as cores dos vértices
#     colors = {}
    
#     # Itera sobre cada vértice ordenado
#     for vertex in vertices:
#         # Conjunto de cores usadas pelos vértices adjacentes
#         used_colors = set(colors.get(neighbour, None) for neighbour in graph[vertex])
        
#         # Encontra a menor cor disponível para o vértice
#         for color in range(len(graph)):
#             if color not in used_colors:
#                 colors[vertex] = color
#                 break
    
#     return colors

def three_coloring(triangles):
    for triangle in triangles:
        corVerticeA = triangle.a.color
        corVerticeB = triangle.b.color
        corVerticeC = triangle.c.color
        
        if corVerticeA == BRANCO and corVerticeB == BRANCO and corVerticeC == BRANCO:
            triangle.a.color = AZUL
            triangle.b.color = VERMELHO
            triangle.c.color = AMARELO
        
        if corVerticeA == BRANCO and corVerticeB == BRANCO and corVerticeC != BRANCO:
            if corVerticeC == AZUL:
                triangle.a.color = VERMELHO
                triangle.b.color = AMARELO
            elif corVerticeC == VERMELHO:
                triangle.a.color = AZUL
                triangle.b.color = AMARELO
            else:
                triangle.a.color = AZUL
                triangle.b.color = VERMELHO
        
        if corVerticeA == BRANCO and corVerticeB != BRANCO and corVerticeC == BRANCO:
            if corVerticeB == AZUL:
                triangle.a.color = VERMELHO
                triangle.c.color = AMARELO
            elif corVerticeB == VERMELHO:
                triangle.a.color = AZUL
                triangle.c.color = AMARELO
            else:
                triangle.a.color = AZUL
                triangle.c.color = VERMELHO
        
        if corVerticeA != BRANCO and corVerticeB == BRANCO and corVerticeC == BRANCO:
            if corVerticeA == AZUL:
                triangle.b.color = VERMELHO
                triangle.c.color = AMARELO
            elif corVerticeA == VERMELHO:
                triangle.b.color = AZUL
                triangle.c.color = AMARELO
            else:
                triangle.b.color = AZUL
                triangle.c.color = VERMELHO
        
        if corVerticeA == BRANCO and corVerticeB != BRANCO and corVerticeC != BRANCO:
            if corVerticeB == AZUL:
                if corVerticeC == VERMELHO:
                    triangle.a.color = AMARELO
                else:
                    triangle.a.color = VERMELHO
            elif corVerticeB == VERMELHO:
                if corVerticeC == AZUL:
                    triangle.a.color = AMARELO
                else:
                    triangle.a.color = AZUL
            else:
                if corVerticeC == AZUL:
                    triangle.a.color = VERMELHO
                else:
                    triangle.a.color = AZUL
        
        if corVerticeA != BRANCO and corVerticeB == BRANCO and corVerticeC != BRANCO:
            if corVerticeA == AZUL:
                if corVerticeC == VERMELHO:
                    triangle.b.color = AMARELO
                else:
                    triangle.b.color = VERMELHO
            elif corVerticeA == VERMELHO:
                if corVerticeC == AZUL:
                    triangle.b.color = AMARELO
                else:
                    triangle.b.color = AZUL
            else:
                if corVerticeC == AZUL:
                    triangle.b.color = VERMELHO
                else:
                    triangle.b.color = AZUL
        
        if corVerticeA != BRANCO and corVerticeB != BRANCO and corVerticeC == BRANCO:
            if corVerticeA == AZUL:
                if corVerticeB == VERMELHO:
                    triangle.c.color = AMARELO
                else:
                    triangle.c.color = VERMELHO
            elif corVerticeA == VERMELHO:
                if corVerticeB == AZUL:
                    triangle.c.color = AMARELO
                else:
                    triangle.c.color = AZUL
            else:
                if corVerticeB == AZUL:
                    triangle.c.color = VERMELHO
                else:
                    triangle.c.color = AZUL
                    
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

def plot_triangles(triangles):
    fig = go.Figure()
    
    # Define o mapa de cores
    color_map = {
        1: 'blue',    # Azul
        2: 'yellow',  # Amarelo
        3: 'red'      # Vermelho
    }
    
    for triangle in triangles:
        # Coordenadas dos vértices
        x_coords = [triangle.a.x, triangle.b.x, triangle.c.x, triangle.a.x]
        y_coords = [triangle.a.y, triangle.b.y, triangle.c.y, triangle.a.y]
        
        # Cores dos vértices
        colors = [color_map[triangle.a.color], color_map[triangle.b.color], color_map[triangle.c.color]]
        print("Triangulo de coordenadas: ", x_coords, y_coords, " e cores: ", colors)
        # Adiciona o triângulo ao gráfico
        fig.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='lines+markers',
                                 line=dict(color='black'),
                                 marker=dict(size=12, color=colors)))
    
    fig.update_layout(title='Triângulos Coloridos',
                      xaxis=dict(range=[0, 8], autorange=False),
                      yaxis=dict(range=[0, 8], autorange=False),
                      showlegend=False)
    
    fig.show()


def plot_colored_triangles(triangle_list, vertex_colors):
    fig = go.Figure()
    
    for triangle in triangle_list:
        x_coords = [point[0] for point in triangle] + [triangle[0][0]]
        y_coords = [point[1] for point in triangle] + [triangle[0][1]]
        colors = [vertex_colors[point] for point in triangle]
        
        fig.add_trace(go.Scatter(x=x_coords, y=y_coords, mode='lines+markers',
                                 line=dict(color='blue'),
                                 marker=dict(size=12, color=colors, colorscale='Viridis', showscale=True)))
    
    fig.update_layout(title='Triângulos Coloridos',
                      xaxis=dict(range=[0, 8], autorange=False),
                      yaxis=dict(range=[0, 8], autorange=False),
                      showlegend=False)
    
    fig.show()

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

#polygon = [(1, 1),( 2, 1), (2, 2), (4, 2) ,(4, 4), (6, 4) ,(6, 6), (7, 6) ,(7, 7), (5 ,7) ,(5, 5), (3 ,5), (3, 3), (1 ,3)]
polygon = [(2, 6), (5, 1), (7, 1), (8, 4), (6.3, 7), (6, 8)]

# polygon = [
#     (3.84375, 6.1728515625), (-0.568359375, 5.9921875), (0.7353515625, 9.197265625),
#     (5.87109375, 8.4716796875), (5.98046875, 9.8125), (9.7734375, 4.330078125),
#     (10.416015625, 7.8349609375), (8.4638671875, 9.9375), (-1.0302734375, 10.91796875),
#     (-2.28515625, 7.859375), (-2.802734375, 7.701171875), (-2.05078125, 5.3076171875),
#     (-1.138671875, 5.00390625), (-1.27734375, 4.4296875), (-1.052734375, 3.671875),
#     (1.283203125, 1.3623046875), (7.44140625, 2.384765625), (10.6484375, 2.19921875),
#     (11.85546875, 1.689453125), (6.701171875, 7.7724609375)
# ]
trianglesList = triangulate_polygon(polygon)
triangles = create_dots_and_triangles(trianglesList)
three_coloring(triangles)
plot_triangles(triangles)
    # Exemplo de acesso às cores após a coloração
# for triangle in triangles:
#     print(f"Cor do vértice A: {triangle.a.color}")
#     print(f"Cor do vértice B: {triangle.b.color}")
#     print(f"Cor do vértice C: {triangle.c.color}")
#     print()

# graph = create_adjacency_list(trianglesList)
    
#     # Aplica o algoritmo de Welsh-Powell para coloração
# vertex_colors = welsh_powell(graph)

# Plota os triângulos coloridos
# plot_colored_triangles(trianglesList, vertex_colors)

# print(trianglesList)
# plot_polygon_and_triangulation(polygon, trianglesList)
