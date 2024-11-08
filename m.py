import pygame
import random
from bf import bellmanford
import time
from collections import defaultdict

pygame.init()

w = 1000
h = 600
cell_size = 20

cols = w // cell_size
rows = h // cell_size

screen = pygame.display.set_mode((w, h))

WHITE = (255, 255, 255)
BLACK = (100, 100, 100)

maze = [[1 for i in range(cols)] for j in range(rows)]

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

graph = defaultdict(list)

Q = []
E = set()
p = True

#dfs to randomly assign the point to be either wall or path
def dfs(x, y):
    maze[y][x] = 0
    E.add((x, y))
    Q.append((x, y))

    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx * 2, y + dy * 2

        if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in E and maze[ny][nx] == 1:
            maze[y + dy][x + dx] = 0
            graph[(x, y)].append(((nx, ny),1))
            graph[(nx, ny)].append(((x, y),1))

            dfs(nx, ny)


dfs(1, 1)

wc = []
for y in range(rows):
    for x in range(cols):
        if maze[y][x] == 0 and x % 2 == 1 and y % 2 == 1:
            wc.append((x, y))

#number of negative weight edge
random_points = random.sample(wc, 10)
'''
print(maze, random_points)
for point in random_points:
    if point in graph.keys():
        print(True)
    else:
        print(False)
'''
#assigning random points negative weight
for point in random_points:
    if point in graph.keys():
        #graph[point] = [(graph[point][i][0], -3) for i in range(len(graph[point]))]
        for i in range(len(graph[point])):
            graph[point][i] = (graph[point][i][0], -1)
            #for k in graph[graph[point][i][0]]:
                #if k[0] == point:
                    #graph[graph[point][i][0]][i] = (point, -1)

    else:
        random_points.remove(point)

print("negative points", random_points)

print('graph:', graph)
result = bellmanford(graph, (1,1), ((cols-1), (rows-1)))

#print the shortest path and its length
if result == "Error":
    print(result)
    path = []
else:
    print(result[0],result[1])
    path = result[2]
    print('path:', path)

#main loop: draw black walls and white path and red points with negative whites, draw purple points to show the shortest path
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for y in range(rows):
        for x in range(cols):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * cell_size, y * cell_size, cell_size, cell_size))
            elif maze[y][x] == 0:
                pygame.draw.rect(screen, WHITE, (x * cell_size, y * cell_size, cell_size, cell_size))

    for point in random_points:
        pygame.draw.circle(screen, (200,0,0), (point[0]*cell_size+cell_size//2, point[1]*cell_size+cell_size-10),7)

    pygame.draw.circle(screen, (0, 0, 200),(cell_size + cell_size // 2, cell_size + cell_size - 10), 7)
    pygame.draw.circle(screen, (0, 200, 0),((cols-1) * cell_size + cell_size // 2, (rows-1) * cell_size + cell_size - 10), 7)

    if p:
        for point in path:
            pygame.draw.circle(screen, (200, 200, 255),(point[0] * cell_size + cell_size // 2, point[1] * cell_size + cell_size - 10), 4)
            time.sleep(0.1)
            pygame.display.flip()
        p = False
    for point in path:
        pygame.draw.circle(screen, (200, 200, 255),(point[0] * cell_size + cell_size // 2, point[1] * cell_size + cell_size - 10), 4)

    pygame.display.flip()

pygame.quit()