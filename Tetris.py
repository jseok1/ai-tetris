import Grid
import Randomizer
import Tetromino
import Timer


class Tetris:

    def __init__(self, width, height):
        """Initialize a new instance of Tetris."""
        self.game_state = 1
        self.randomizer = Randomizer.Randomizer()
        self.current_tetromino = self.randomizer.get_tetromino()
        self.next_tetromino = [self.randomizer.get_tetromino()]
        self.grid = Grid.Grid(width, height)
        self.fall_down = Timer.Timer(40)
        self.clear_lines = Timer.Timer(30)  # 500 ms
        self.lines_cleared = 0

    def move_left(self):
        """Move the current tetromino left, if possible."""
        if self.grid.can_place(self.current_tetromino, -1, 0, 0):
            self.current_tetromino.move(-1, 0)

    def move_right(self):
        """Move the current tetromino right, if possible."""
        if self.grid.can_place(self.current_tetromino, 1, 0, 0):
            self.current_tetromino.move(1, 0)

    def move_down(self):
        """Move the current tetromino down, if possible. Otherwise,"""
        if self.grid.can_place(self.current_tetromino, 0, 1, 0):
            self.current_tetromino.move(0, 1)
        else:
            self.grid.place_tetromino(self.current_tetromino)
            if self.grid.can_clear():
                self.game_state = 2
            else:
                self.reset_tetromino()
                self.fall_down.reset()

    def drop_down(self):
        while self.grid.can_place(self.current_tetromino, 0, 1, 0):
            self.current_tetromino.move(0, 1)
        self.grid.place_tetromino(self.current_tetromino)
        if self.grid.can_clear():
            self.game_state = 2
        else:
            self.reset_tetromino()
            self.fall_down.reset()

    def rotate_clockwise(self):
        if self.grid.can_place(self.current_tetromino, 0, 0, 1):
            self.current_tetromino.rotate(1)

    def rotate_counterclockwise(self):
        if self.grid.can_place(self.current_tetromino, 0, 0, -1):
            self.current_tetromino.rotate(-1)

    def reset_tetromino(self):
        self.current_tetromino = self.next_tetromino.pop(0)
        self.next_tetromino.append(self.randomizer.get_tetromino())
        if not self.grid.can_place(self.current_tetromino, 0, 0, 0):
            self.game_state = 0

    def update(self):
        if self.game_state == 1:
            if self.fall_down.tick() == 0:
                self.move_down()
        elif self.game_state == 2:
            n = self.clear_lines.tick()
            if n == 0:
                self.grid.shift_lines()
                self.reset_tetromino()
                self.fall_down.reset()
                self.game_state = 1
            elif n > 1:
                self.grid.clear_lines()
