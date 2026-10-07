import pygame
from game.maze import CELL

SPEED = 3

class Player:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        x = c*CELL + CELL//2
        y = r*CELL + CELL//2
        self.rect = pygame.Rect(x-10, y-10, 20, 20)
        self.color = (60,120,220)

    def move(self, keys, walls, rows, cols):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = SPEED

        # Wall-aware movement (check cell boundaries)
        new_rect = self.rect.move(dx, 0)
        if not self._hits_wall(new_rect, walls, rows, cols):
            self.rect = new_rect
        new_rect = self.rect.move(0, dy)
        if not self._hits_wall(new_rect, walls, rows, cols):
            self.rect = new_rect

    def _hits_wall(self, rect, walls, rows, cols):
        # 1. Outer boundary check
        if rect.left < 0 or rect.top < 0 or rect.right > cols * CELL or rect.bottom > rows * CELL:
            return True

        # 2. Check grid walls for all cells intersecting rect
        min_r = max(0, rect.top // CELL)
        max_r = min(rows - 1, (rect.bottom - 1) // CELL)
        min_c = max(0, rect.left // CELL)
        max_c = min(cols - 1, (rect.right - 1) // CELL)

        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                w = walls[r][c]  # [N, S, E, W]
                # North wall (y = r * CELL)
                if w[0] and rect.top < r * CELL < rect.bottom:
                    return True
                # South wall (y = (r + 1) * CELL)
                if w[1] and rect.top < (r + 1) * CELL < rect.bottom:
                    return True
                # East wall (x = (c + 1) * CELL)
                if w[2] and rect.left < (c + 1) * CELL < rect.right:
                    return True
                # West wall (x = c * CELL)
                if w[3] and rect.left < c * CELL < rect.right:
                    return True

        return False

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)
