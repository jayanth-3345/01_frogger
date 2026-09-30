"""Own the frog and vehicles, and run one frame of game logic."""

import random

import pygame

from game.frog import Frog
from game.vehicle import Vehicle
from game.collisions import check_collision
from game.renderer import (
    GRID_COLS, GRID_ROWS, GOAL_ROW, ROAD_ROWS, START_ROW, CELL_SIZE, WIDTH, HEIGHT,
)

LANE_SPEEDS = [1.5, -2, 2, -2.5, 1.5, -2]   # one entry per road row, alternating direction
STARTING_LIVES = 3
HIT_DURATION_MS = 900
ATTEMPT_DURATION_MS = 30_000


class GameEngine:
    def __init__(self):
        self.lives = STARTING_LIVES
        self.score = 0
        self.won = False
        self.hit_until_ms = 0
        self.attempt_deadline_ms = pygame.time.get_ticks() + ATTEMPT_DURATION_MS
        self._build_entities()

    @property
    def game_over(self):
        return self.lives <= 0

    @property
    def time_remaining_seconds(self):
        remaining_ms = max(0, self.attempt_deadline_ms - pygame.time.get_ticks())
        return (remaining_ms + 999) // 1000

    def restart(self):
        self.lives = STARTING_LIVES
        self.score = 0
        self.won = False
        self.hit_until_ms = 0
        self.attempt_deadline_ms = pygame.time.get_ticks() + ATTEMPT_DURATION_MS
        self._build_entities()

    def _build_entities(self):
        start_col = GRID_COLS // 2
        self.frog = Frog(
            col=start_col, row=START_ROW,
            start_col=start_col, start_row=START_ROW,
            cols=GRID_COLS, start_row_limit=START_ROW,
        )
        frog_x_range = (start_col * CELL_SIZE, start_col * CELL_SIZE + CELL_SIZE)

        self.vehicles = []
        for i, row in enumerate(ROAD_ROWS):
            speed = LANE_SPEEDS[i % len(LANE_SPEEDS)]
            vehicle_width = 40 if i % 2 == 0 else 70   # mix of cars and wider trucks
            spacing = 300
            count = 2

            # Try a few random phases and keep the first one that doesn't
            # already overlap the frog's starting column - guarantees a
            # safe first lane instead of leaving it to chance.
            for _attempt in range(20):
                phase = random.randint(0, spacing - 1)
                positions = []
                safe = True
                for n in range(count):
                    offset = phase + n * spacing
                    x = offset if speed > 0 else WIDTH - offset - vehicle_width
                    positions.append(x)
                    if not (x + vehicle_width <= frog_x_range[0] or x >= frog_x_range[1]):
                        safe = False
                if safe:
                    break

            for x in positions:
                self.vehicles.append(Vehicle(x=x, row=row, width=vehicle_width,
                                              height=CELL_SIZE - 8, speed=speed))

    def handle_keydown(self, key):
        if key == pygame.K_r:
            self.restart()
            return
        if self.game_over or self.won or pygame.time.get_ticks() < self.hit_until_ms:
            return

        if key == pygame.K_UP:
            self.frog.move(0, -1)
        elif key == pygame.K_DOWN:
            self.frog.move(0, 1)
        elif key == pygame.K_LEFT:
            self.frog.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.frog.move(1, 0)

    def update(self):
        if self.game_over or self.won:
            return

        now_ms = pygame.time.get_ticks()
        if now_ms >= self.attempt_deadline_ms:
            self.lives -= 1
            self.frog.reset()
            self.attempt_deadline_ms = now_ms + ATTEMPT_DURATION_MS
            return

        for v in self.vehicles:
            v.update(road_width_px=WIDTH)

        if now_ms >= self.hit_until_ms and check_collision(self.frog, self.vehicles):
            self.lives -= 1
            self.frog.reset()
            self.hit_until_ms = now_ms + HIT_DURATION_MS
            self.attempt_deadline_ms = now_ms + ATTEMPT_DURATION_MS

        if self.frog.row == GOAL_ROW:
            self.score += 1
            self.won = True

    def draw(self, surface, font):
        from game import renderer
        hit_visible = not self.game_over and pygame.time.get_ticks() < self.hit_until_ms
        renderer.draw_scene(surface, self.frog, self.vehicles, frog_hit=hit_visible)
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 10))
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 34))
        renderer.draw_text(surface, font, f"Time: {self.time_remaining_seconds}s", (10, 58))
        renderer.draw_text(surface, font, "Arrow keys to move. R to restart.", (10, HEIGHT - 24))
        if hit_visible:
            renderer.draw_banner(surface, font, "HIT!")
        if self.game_over:
            renderer.draw_game_over(surface, font)
        elif self.won:
            renderer.draw_victory(surface, font, self.score)
