import pygame
import time
import json
import os
from game.maze import generate_maze, solve_maze, CELL
from game.player import Player

FPS = 60
BG = (240, 235, 220)
WALL_COLOR = (40, 40, 60)
EXIT_COLOR = (80, 200, 80)
PATH_COLOR = (255, 200, 80)
COLS, ROWS = 15, 13

WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + 60

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 22)
        self.big_font = pygame.font.SysFont("monospace", 36, bold=True)
        self.leaderboard_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "leaderboard.json")
        self.leaderboard = self.load_leaderboard()
        self.reset()

    def load_leaderboard(self):
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, "r") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        return sorted([float(x) for x in data if isinstance(x, (int, float))])[:5]
            except Exception:
                pass
        return []

    def save_leaderboard(self):
        try:
            with open(self.leaderboard_file, "w") as f:
                json.dump(self.leaderboard, f, indent=2)
        except Exception:
            pass

    def reset(self):
        self.walls = generate_maze(COLS, ROWS)
        self.player = Player(0, 0)
        self.exit_rect = pygame.Rect((COLS-1)*CELL+5, (ROWS-1)*CELL+5, CELL-10, CELL-10)
        self.start_time = time.time()
        self.elapsed = 0
        self.won = False
        self.show_path = False
        self.fog_enabled = True
        self.solution_path = solve_maze(self.walls, (0,0), (ROWS-1, COLS-1))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_h:
                    self.show_path = not self.show_path
                elif event.key == pygame.K_f:
                    self.fog_enabled = not self.fog_enabled
        return True

    def update(self):
        if self.won:
            return
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.walls, ROWS, COLS)
        self.elapsed = time.time() - self.start_time
        if self.player.rect.colliderect(self.exit_rect):
            self.won = True
            final_time = round(self.elapsed, 2)
            self.leaderboard.append(final_time)
            self.leaderboard.sort()
            self.leaderboard = self.leaderboard[:5]
            self.save_leaderboard()

    def draw_path(self):
        pad = 8
        for r, c in self.solution_path:
            x, y = c * CELL, r * CELL
            path_rect = pygame.Rect(x + pad, y + pad, CELL - 2 * pad, CELL - 2 * pad)
            pygame.draw.rect(self.screen, PATH_COLOR, path_rect, border_radius=4)

    def draw_fog(self):
        fog_surf = pygame.Surface((WIDTH, ROWS * CELL), pygame.SRCALPHA)
        fog_surf.fill((10, 10, 20, 255))
        radius = 3 * CELL
        pygame.draw.circle(fog_surf, (0, 0, 0, 0), self.player.rect.center, radius)
        self.screen.blit(fog_surf, (0, 0))

    def draw_maze(self):
        wall_w = 3
        for r in range(ROWS):
            for c in range(COLS):
                x, y = c*CELL, r*CELL
                w = self.walls[r][c]
                if w[0]: pygame.draw.line(self.screen, WALL_COLOR, (x,y), (x+CELL,y), wall_w)
                if w[1]: pygame.draw.line(self.screen, WALL_COLOR, (x,y+CELL), (x+CELL,y+CELL), wall_w)
                if w[2]: pygame.draw.line(self.screen, WALL_COLOR, (x+CELL,y), (x+CELL,y+CELL), wall_w)
                if w[3]: pygame.draw.line(self.screen, WALL_COLOR, (x,y), (x,y+CELL), wall_w)

    def draw(self):
        self.screen.fill(BG)
        if self.show_path:
            self.draw_path()
        self.draw_maze()
        pygame.draw.rect(self.screen, EXIT_COLOR, self.exit_rect, border_radius=4)
        ex_label = self.font.render("EXIT", True, (20,80,20))
        self.screen.blit(ex_label, (self.exit_rect.x+2, self.exit_rect.y+4))
        self.player.draw(self.screen)

        if self.fog_enabled:
            self.draw_fog()

        hud = pygame.Rect(0, ROWS*CELL, WIDTH, 60)
        pygame.draw.rect(self.screen, (30,30,50), hud)
        time_surf = self.font.render(f"Time: {self.elapsed:.1f}s   R = New  H = Hint  F = Fog", True, (200,200,200))
        self.screen.blit(time_surf, (10, ROWS*CELL+18))

        if self.won:
            overlay = pygame.Surface((WIDTH, ROWS*CELL), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            msg = self.big_font.render(f"Solved in {self.elapsed:.2f}s!", True, (80, 240, 80))
            self.screen.blit(msg, (WIDTH//2 - msg.get_width()//2, 45))

            lb_title = self.font.render("--- TOP 5 LEADERBOARD ---", True, (255, 215, 0))
            self.screen.blit(lb_title, (WIDTH//2 - lb_title.get_width()//2, 105))

            y_offset = 145
            for rank, score in enumerate(self.leaderboard, 1):
                entry_str = f"#{rank}: {score:.2f}s"
                color = (100, 255, 100) if score == round(self.elapsed, 2) else (220, 220, 220)
                entry_surf = self.font.render(entry_str, True, color)
                self.screen.blit(entry_surf, (WIDTH//2 - entry_surf.get_width()//2, y_offset))
                y_offset += 30

            sub = self.font.render("Press R for a new maze", True, (200, 200, 200))
            self.screen.blit(sub, (WIDTH//2 - sub.get_width()//2, ROWS*CELL - 45))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
