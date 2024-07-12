import matplotlib.pyplot as plt

# Dados fornecidos
data = {
    (0.7353515625, 9.197265625): 0,
    (5.87109375, 8.4716796875): 1,
    (5.98046875, 9.8125): 2,
    (9.7734375, 4.330078125): 0,
    (10.416015625, 7.8349609375): 1,
    (8.4638671875, 9.9375): 0,
    (-1.0302734375, 10.91796875): 1,
    (-0.568359375, 5.9921875): 2,
    (-2.28515625, 7.859375): 0,
    (-2.802734375, 7.701171875): 1,
    (-2.05078125, 5.3076171875): 0,
    (3.84375, 6.1728515625): 1,
    (-1.138671875, 5.00390625): 2,
    (-1.27734375, 4.4296875): 0,
    (-1.052734375, 3.671875): 2,
    (1.283203125, 1.3623046875): 0,
    (6.701171875, 7.7724609375): 2,
    (7.44140625, 2.384765625): 1,
    (10.6484375, 2.19921875): 0,
    (11.85546875, 1.689453125): 1
}

# Separar os pontos e as cores
x = [point[0] for point in data.keys()]
y = [point[1] for point in data.keys()]
colors = [data[point] for point in data.keys()]

# Definir o mapa de cores
cmap = {0: 'red', 1: 'green', 2: 'blue'}
color_values = [cmap[color] for color in colors]

# Criar o plot
plt.scatter(x, y, c=color_values)

# Adicionar arestas entre os pontos na ordem fornecida
plt.plot(x, y, 'k-', alpha=0.5)  # 'k-' para linha preta e alpha=0.5 para transparência

# Adicionar rótulos e título
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Plot de Pontos com Arestas e Cores Baseadas no Valor Associado')

# Mostrar o plot
plt.show()
