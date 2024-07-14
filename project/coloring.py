import plotly.graph_objects as go

def coloringTriangles(triangles, polygon, additionalEdgesX, additionalEdgesY):
    verticesx = [vertex[0] for vertex in polygon]
    verticesy = [vertex[1] for vertex in polygon]
    colorMap = {}
    
    neighbors = {}
    
    for triangle in triangles:
        for i in range(3):
            point = triangle[i]
            if point not in neighbors:
                neighbors[point] = set()
            neighbors[point].add(triangle[(i+1)%3])
            neighbors[point].add(triangle[(i+2)%3])
    
    for point in neighbors:
        available_colors = {0, 1, 2} - {colorMap.get(neigh) for neigh in neighbors[point]}
        colorMap[point] = min(available_colors)

    coloringFrames = []
    data = []
    data.append(go.Scatter(x=verticesx, y=verticesy, mode='lines+markers+text', line=dict(color='black'), 
            text=[str(i) for i in range(len(polygon))] + [str(0)], textposition='top right', name='Polígono'))
    data.append(go.Scatter(x=additionalEdgesX, y=additionalEdgesY, mode='lines', line=dict(color='black')))

    for point, colored in colorMap.items():
        print(f"Vértice {point}: {colored}")
        if colored == 0:
            #print("ENTREI NO 0")
            data.append(go.Scatter(x=[point[0]], y=[point[1]], mode='markers', marker=dict(size=10, color='red')))

        elif colored == 1:
            #print("ENTREI NO 1")
            data.append(go.Scatter(x=[point[0]], y=[point[1]], mode='markers', marker=dict(size=10, color='green')))

        else: 
            #print("ENTREI NO 2")
            data.append(
                go.Scatter(x=[point[0]], y=[point[1]], mode='markers', marker=dict(size=10, color='blue')))

        coloringFrames.append(go.Frame(
            data=data,
            name=f'frame{len(coloringFrames)}'
        ))
        

    # colors = {0: 'red', 1: 'green', 2: 'blue'}
    # print("Cores dos vértices:")
    # for point, color in color_map.items():
    #     print(f"Vértice {point}: {colors[color]}")

    
    return coloringFrames, colorMap