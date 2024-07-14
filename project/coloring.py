import plotly.graph_objects as go

def three_color_triangles(triangles):
    # Cria um dicionário para armazenar a cor de cada ponto
    color_map = {}
    
    # Cria um dicionário para armazenar os vizinhos de cada ponto
    neighbors = {}
    
    # Adiciona os vizinhos de cada ponto com base nos triângulos
    for triangle in triangles:
        for i in range(3):
            point = triangle[i]
            if point not in neighbors:
                neighbors[point] = set()
            neighbors[point].add(triangle[(i+1)%3])
            neighbors[point].add(triangle[(i+2)%3])
    
    # Aplica a coloração de 3 cores
    
    for point in neighbors:
        available_colors = {0, 1, 2} - {color_map.get(neigh) for neigh in neighbors[point]}
        color_map[point] = min(available_colors)
        

    # colors = {0: 'red', 1: 'green', 2: 'blue'}
    # print("Cores dos vértices:")
    # for point, color in color_map.items():
    #     print(f"Vértice {point}: {colors[color]}")
    
    return color_map