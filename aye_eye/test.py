"""
Write any tests inside the test function below.
The code in `__main__.py` calls `test()`.
"""

from aye_eye.player import Player
from search.util import print_board
from aye_eye.util import print_state


def test():
    while True:
        colour = str(input('Enter "red" or "blue" player: '))
        if colour not in ["red", "blue"]:
            print('Colour must be either "red" or "blue"')
            continue
        break
    n = int(input("Enter board size n: "))
    player = Player(colour, n)
    print(f"Player {player.player} initialised")
    print(f"Board size {n} initialised:")
    print_board(n, board_dict={}, ansi=True)
    print_state(player.state)
