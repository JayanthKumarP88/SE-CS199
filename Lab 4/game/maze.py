import random

CELL = 40  # cell size in pixels

def generate_maze(cols, rows):
    """Recursive backtracker maze generation. Returns 2D grid of walls."""
    visited = [[False]*cols for _ in range(rows)]
    # walls: each cell has [N, S, E, W]
    walls = [[[True,True,True,True] for _ in range(cols)] for _ in range(rows)]
    
    def neighbors(r, c):
        dirs = [(-1,0,0,1),(1,0,1,0),(0,1,2,3),(0,-1,3,2)]  # dr,dc,wall_dir,opp_dir
        result = []
        for dr,dc,wd,od in dirs:
            nr,nc = r+dr,c+dc
            if 0<=nr<rows and 0<=nc<cols and not visited[nr][nc]:
                result.append((nr,nc,wd,od))
        return result

    stack = [(0,0)]
    visited[0][0] = True
    while stack:
        r,c = stack[-1]
        nbrs = neighbors(r,c)
        if nbrs:
            nr,nc,wd,od = random.choice(nbrs)
            walls[r][c][wd] = False
            walls[nr][nc][od] = False
            visited[nr][nc] = True
            stack.append((nr,nc))
        else:
            stack.pop()
    return walls

from collections import deque

def solve_maze(walls, start=(0,0), end=None):
    """BFS solver to find shortest path from start cell to end cell."""
    rows = len(walls)
    cols = len(walls[0])
    if end is None:
        end = (rows - 1, cols - 1)

    queue = deque([start])
    visited = {start}
    parent = {}
    dirs = [(-1, 0, 0), (1, 0, 1), (0, 1, 2), (0, -1, 3)]  # dr, dc, wall_idx

    found = False
    while queue:
        curr = queue.popleft()
        if curr == end:
            found = True
            break
        r, c = curr
        for dr, dc, w_idx in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if not walls[r][c][w_idx] and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    parent[(nr, nc)] = curr
                    queue.append((nr, nc))

    if not found:
        return []

    path = []
    curr = end
    while curr in parent:
        path.append(curr)
        curr = parent[curr]
    path.append(start)
    path.reverse()
    return path

def cell_rect(r, c, import_pygame=None):
    import pygame
    return pygame.Rect(c*CELL, r*CELL, CELL, CELL)

