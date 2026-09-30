"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

CELL_SIZE = 50
GRID_COLS = 12
GRID_ROWS = 8

WIDTH = CELL_SIZE * GRID_COLS
HEIGHT = CELL_SIZE * GRID_ROWS
WINDOW_SIZE = (WIDTH, HEIGHT)

GOAL_ROW = 0
ROAD_ROWS = list(range(1, GRID_ROWS - 1))   # rows 1..6
START_ROW = GRID_ROWS - 1                     # row 7

COLOR_BG = (20, 20, 25)
COLOR_GOAL = (40, 130, 60)
COLOR_ROAD = (45, 45, 50)
COLOR_START = (40, 90, 60)
COLOR_LANE_LINE = (90, 90, 90)
COLOR_FROG = (80, 220, 100)
COLOR_FROG_HIT = (255, 220, 80)
COLOR_VEHICLE = (220, 80, 70)
COLOR_TEXT = (255, 255, 255)


def draw_scene(surface, frog, vehicles, frog_hit=False):
    surface.fill(COLOR_BG)

    for row in range(GRID_ROWS):
        rect = pygame.Rect(0, row * CELL_SIZE, WIDTH, CELL_SIZE)
        if row == GOAL_ROW:
            pygame.draw.rect(surface, COLOR_GOAL, rect)
        elif row == START_ROW:
            pygame.draw.rect(surface, COLOR_START, rect)
        else:
            pygame.draw.rect(surface, COLOR_ROAD, rect)
            pygame.draw.line(surface, COLOR_LANE_LINE, (0, row * CELL_SIZE), (WIDTH, row * CELL_SIZE), 1)

    for v in vehicles:
        pygame.draw.rect(surface, COLOR_VEHICLE, v.get_rect(CELL_SIZE), border_radius=6)

    frog_color = COLOR_FROG_HIT if frog_hit else COLOR_FROG
    pygame.draw.rect(surface, frog_color, frog.get_rect(CELL_SIZE), border_radius=8)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)


def draw_game_over(surface, font):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    surface.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont("consolas", 42, bold=True)
    title = title_font.render("GAME OVER", True, (255, 100, 90))
    title_rect = title.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 18))
    surface.blit(title, title_rect)

    prompt = font.render("Press R to restart", True, COLOR_TEXT)
    prompt_rect = prompt.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 24))
    surface.blit(prompt, prompt_rect)


def draw_victory(surface, font, score):
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    surface.blit(overlay, (0, 0))

    title_font = pygame.font.SysFont("consolas", 42, bold=True)
    title = title_font.render("You Won!", True, (120, 240, 140))
    title_rect = title.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 - 30))
    surface.blit(title, title_rect)

    score_text = font.render(f"Score: {score}", True, COLOR_TEXT)
    score_rect = score_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 4))
    surface.blit(score_text, score_rect)

    prompt = font.render("Press R to play again", True, COLOR_TEXT)
    prompt_rect = prompt.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 32))
    surface.blit(prompt, prompt_rect)
