import numpy as np

def build_distance():
    n = 28
    m = n*n
    d = np.empty((m,m))
    coor = []
    for i in range(n):
        for j in range(n):
            coor.append(np.array([i,j]))
    for i in range(m):
        for j in range(m):
            d[i][j] = np.linalg.norm(coor[i]-coor[j])**2
    return d