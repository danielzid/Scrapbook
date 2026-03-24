# 2026-03-21

import os
from random import randint
from time import sleep


class Board:
    char_map = {0: '-', -1: 'O', 1: 'X'}
    DISPLAY_INDEX_OFFSET = 1

    @staticmethod
    def clear() -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def __init__(self, size: int = 3, win_thresh: int = 3) -> None:
        self.size = abs(size)
        self.win_thresh = min(self.size, win_thresh)
        self.board: list[list[int]] = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.occupied_set: set[tuple[int, int]] = set()
        self.invalid_set: set[tuple[int, int]] = set()

    def draw_labels(self) -> None:
        x_label = (chr(ord('A') + i) for i in range(self.size))
        print("   ", end="")
        for label in x_label:
            print(f"  {label} ", end="")
        print()

    def draw_board(self) -> None:
        self.draw_labels()
        line = lambda: print("   -" + "----" * self.size)
        line()
        for idx, row in enumerate(self.board):
            print(f"{idx + self.DISPLAY_INDEX_OFFSET:<2} ", end="")
            for i in row:
                print(f"| {self.char_map[i]} ", end="")
            print("|")
        line()

    def update_board(self, e_input: tuple[int, int], player: str = "player") -> None:
        row, col = e_input
        self.board[row][col] = 1 if player == "player" else -1
        self.occupied_set.add((row, col))

    def get_player_input(self) -> tuple[int, int]:
        while True:
            try:
                col, row = input('Enter move (col row), e.g. "A 1": ').strip().split()
                r = int(row) - 1
                c = ord(col.upper()) - ord('A')
                if not (0 <= r < self.size and 0 <= c < self.size):
                    print("Out of bounds, try again.")
                    continue
                if (r, c) in self.occupied_set:
                    print("Cell already taken, try again.")
                    continue
                return r, c
            except (ValueError, IndexError):
                print("Invalid input. Enter column letter and row number, e.g. 'A 1'.")

    def check_win(self) -> tuple[bool, int]:
        """
        Returns (True, winner) if someone has won, else (False, 0).
        winner: 1 = player, -1 = computer.
        """
        # directions: (row_delta, col_delta) for one side of each axis
        axes = [
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (1, 1),   # diagonal 1
            (1, -1),  # diagonal 2
        ]

        checked: set[tuple[tuple[int, int], tuple[int, int]]] = set()

        for (row, col) in self.occupied_set:
            if (row, col) in self.invalid_set:
                continue

            val = self.board[row][col]

            for dr, dc in axes:
                # Avoid rechecking the same line from a different starting cell
                axis_key = ((row, col), (dr, dc))
                rev_key  = ((row, col), (-dr, -dc))
                if axis_key in checked or rev_key in checked:
                    continue
                checked.add(axis_key)

                count = 1 

                # Walk forward
                for step in range(1, self.win_thresh):
                    nr, nc = row + dr * step, col + dc * step
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == val:
                        count += 1
                    else:
                        break

                # Walk backward
                for step in range(1, self.win_thresh):
                    nr, nc = row - dr * step, col - dc * step
                    if 0 <= nr < self.size and 0 <= nc < self.size and self.board[nr][nc] == val:
                        count += 1
                    else:
                        break

                if count >= self.win_thresh:
                    return True, val

        return False, 0

    def is_full(self) -> bool:
        return len(self.occupied_set) == self.size * self.size

    def get_neighbors(self, pos: tuple[int, int]) -> list[list[tuple[int, int]]]:
        """
        Returns neighbors grouped by axis:
          [0] horizontal, [1] vertical, [2] diagonal 1, [3] diagonal 2
        Only includes cells that are occupied.
        """
        res: list[list[tuple[int, int]]] = [[], [], [], []]
        row, col = pos

        axes = [
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (1, 1),   # diagonal 1
            (1, -1),  # diagonal 2
        ]

        for axis_idx, (dr, dc) in enumerate(axes):
            for sign in (1, -1):
                for step in range(1, self.win_thresh):
                    nr = row + sign * dr * step
                    nc = col + sign * dc * step
                    if 0 <= nr < self.size and 0 <= nc < self.size:
                        if (nr, nc) in self.occupied_set:
                            res[axis_idx].append((nr, nc))
                    else:
                        break  # don't wrap or skip gaps

        return res

    def comp_play(self) -> tuple[int, int]:
        print("Computer thinking...")
        sleep(0.5)
        while True:
            row = randint(0, self.size - 1)
            col = randint(0, self.size - 1)
            if (row, col) not in self.occupied_set:
                return row, col


def main() -> None:
    bd = Board()

    while True:
        Board.clear()
        bd.draw_board()

        # Player move
        p_in = bd.get_player_input()
        bd.update_board(p_in, 'player')

        won, winner = bd.check_win()
        if won:
            Board.clear()
            bd.draw_board()
            print("You win! 🎉" if winner == 1 else "Computer wins!")
            break

        if bd.is_full():
            Board.clear()
            bd.draw_board()
            print("It's a draw!")
            break

        # Computer move
        c_in = bd.comp_play()
        bd.update_board(c_in, 'comp')

        won, winner = bd.check_win()
        if won:
            Board.clear()
            bd.draw_board()
            print("Computer wins! Better luck next time.")
            break

        if bd.is_full():
            Board.clear()
            bd.draw_board()
            print("It's a draw!")
            break


if __name__ == "__main__":
    main()