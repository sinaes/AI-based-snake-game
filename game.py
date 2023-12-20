import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import config as cf

pygame.init()
font = pygame.font.Font('arial.ttf', 30)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

class SnakeGame:

    def __init__(self, w=1000, h=800):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-cf.BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*cf.BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, (self.w-cf.BLOCK_SIZE )//cf.BLOCK_SIZE )*cf.BLOCK_SIZE
        y = random.randint(0, (self.h-cf.BLOCK_SIZE )//cf.BLOCK_SIZE )*cf.BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(cf.SPEED)
        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - cf.BLOCK_SIZE or pt.x < 0 or pt.y > self.h - cf.BLOCK_SIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False


    def _update_ui(self):
        self.display.fill(cf.BACKGROUND)

        for pt in self.snake:
            pygame.draw.rect(self.display, cf.SNAKE_IN_COLOR, pygame.Rect(pt.x, pt.y, cf.BLOCK_SIZE, cf.BLOCK_SIZE))
            pygame.draw.rect(self.display, cf.SNAKE_OUT_COLOR, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, cf.FOOD_COLOR, pygame.Rect(self.food.x, self.food.y, cf.BLOCK_SIZE, cf.BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, cf.FONT_COLOR)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += cf.BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= cf.BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += cf.BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= cf.BLOCK_SIZE

        self.head = Point(x, y)