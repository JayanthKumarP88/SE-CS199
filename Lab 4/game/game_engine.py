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

DEFAULT_COLS, DEFAULT_ROWS = 15, 13

class GameEngine:
    def __init__(self):
        pygame.init()
        self.cols = DEFAULT_COLS
        self.rows = DEFAULT_ROWS
        self.width = self.cols * CELL
        self.height = self.rows * CELL + 60
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 19)
        self.big_font = pygame.font.SysFont("monospace", 32, bold=True)
        self.leaderboard_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "leaderboard.json")
        self.leaderboard = self.load_leaderboard()

        self.state = "SELECT"
        self.walls = []
        self.solution_path = []
        self.player = None
        self.exit_rect = None
        self.elapsed = 0
        self.won = False
        self.show_path = False
        self.fog_enabled = True

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

    def get_difficulty_buttons(self):
        cx = self.width // 2
        btn_w, btn_h = 280, 52
        btn_easy = pygame.Rect(cx - btn_w // 2, 170, btn_w, btn_h)
        btn_med = pygame.Rect(cx - btn_w // 2, 240, btn_w, btn_h)
        btn_hard = pygame.Rect(cx - btn_w // 2, 310, btn_w, btn_h)
        return [
            ("Easy (10x8)", 10, 8, btn_easy),
            ("Medium (15x13)", 15, 13, btn_med),
            ("Hard (20x18)", 20, 18, btn_hard),
        ]

    def start_game(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.width = cols * CELL
        self.height = rows * CELL + 60
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.state = "PLAYING"
        self.reset()

    def open_difficulty_select(self):
        self.state = "SELECT"
        self.width = DEFAULT_COLS * CELL
        self.height = DEFAULT_ROWS * CELL + 60
        self.screen = pygame.display.set_mode((self.width, self.height))

    def reset(self):
        self.walls = generate_maze(self.cols, self.rows)
        self.player = Player(0, 0)
        self.exit_rect = pygame.Rect((self.cols-1)*CELL+5, (self.rows-1)*CELL+5, CELL-10, CELL-10)
        self.start_time = time.time()
        self.elapsed = 0
        self.won = False
        self.show_path = False
        self.fog_enabled = True
        self.solution_path = solve_maze(self.walls, (0,0), (self.rows-1, self.cols-1))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if self.state == "SELECT":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for label, cols, rows, rect in self.get_difficulty_buttons():
                        if rect.collidepoint(event.pos):
                            self.start_game(cols, rows)
                            break
            elif self.state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_h:
                        self.show_path = not self.show_path
                    elif event.key == pygame.K_f:
                        self.fog_enabled = not self.fog_enabled
                    elif event.key in (pygame.K_m, pygame.K_ESCAPE):
                        self.open_difficulty_select()
        return True

    def update(self):
        if self.state != "PLAYING" or self.won:
            return
        keys = pygame.key.get_pressed()
        self.player.move(keys, self.walls, self.rows, self.cols)
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
        fog_surf = pygame.Surface((self.width, self.rows * CELL), pygame.SRCALPHA)
        fog_surf.fill((10, 10, 20, 255))
        radius = 3 * CELL
        pygame.draw.circle(fog_surf, (0, 0, 0, 0), self.player.rect.center, radius)
        self.screen.blit(fog_surf, (0, 0))

    def draw_maze(self):
        wall_w = 3
        for r in range(self.rows):
            for c in range(self.cols):
                x, y = c*CELL, r*CELL
                w = self.walls[r][c]
                if w[0]: pygame.draw.line(self.screen, WALL_COLOR, (x,y), (x+CELL,y), wall_w)
                if w[1]: pygame.draw.line(self.screen, WALL_COLOR, (x,y+CELL), (x+CELL,y+CELL), wall_w)
                if w[2]: pygame.draw.line(self.screen, WALL_COLOR, (x+CELL,y), (x+CELL,y+CELL), wall_w)
                if w[3]: pygame.draw.line(self.screen, WALL_COLOR, (x,y), (x,y+CELL), wall_w)

    def draw_select(self):
        self.screen.fill(BG)
        title = self.big_font.render("MAZE RUNNER", True, WALL_COLOR)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 55))

        subtitle = self.font.render("Select Difficulty", True, (70, 70, 90))
        self.screen.blit(subtitle, (self.width // 2 - subtitle.get_width() // 2, 110))

        mouse_pos = pygame.mouse.get_pos()
        for label, cols, rows, rect in self.get_difficulty_buttons():
            is_hover = rect.collidepoint(mouse_pos)
            color = (70, 130, 220) if is_hover else (50, 90, 160)
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, (25, 45, 90), rect, width=2, border_radius=8)

            txt = self.font.render(label, True, (255, 255, 255))
            self.screen.blit(txt, (rect.centerx - txt.get_width() // 2, rect.centery - txt.get_height() // 2))

        hint = self.font.render("Click a button to start", True, (120, 120, 140))
        self.screen.blit(hint, (self.width // 2 - hint.get_width() // 2, 395))
        pygame.display.flip()

    def draw(self):
        if self.state == "SELECT":
            self.draw_select()
            return

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

        hud = pygame.Rect(0, self.rows*CELL, self.width, 60)
        pygame.draw.rect(self.screen, (30,30,50), hud)
        time_surf = self.font.render(f"Time: {self.elapsed:.1f}s  R=New  H=Hint  F=Fog  M=Menu", True, (200,200,200))
        self.screen.blit(time_surf, (10, self.rows*CELL+18))

        if self.won:
            overlay = pygame.Surface((self.width, self.rows*CELL), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            msg = self.big_font.render(f"Solved in {self.elapsed:.2f}s!", True, (80, 240, 80))
            self.screen.blit(msg, (self.width//2 - msg.get_width()//2, max(15, self.rows*CELL//12)))

            lb_title = self.font.render("--- TOP 5 LEADERBOARD ---", True, (255, 215, 0))
            self.screen.blit(lb_title, (self.width//2 - lb_title.get_width()//2, max(55, self.rows*CELL//12 + 40)))

            y_offset = max(90, self.rows*CELL//12 + 75)
            for rank, score in enumerate(self.leaderboard, 1):
                entry_str = f"#{rank}: {score:.2f}s"
                color = (100, 255, 100) if score == round(self.elapsed, 2) else (220, 220, 220)
                entry_surf = self.font.render(entry_str, True, color)
                self.screen.blit(entry_surf, (self.width//2 - entry_surf.get_width()//2, y_offset))
                y_offset += 26

            sub = self.font.render("Press R: New Maze | M: Menu", True, (200, 200, 200))
            self.screen.blit(sub, (self.width//2 - sub.get_width()//2, self.rows*CELL - 35))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
