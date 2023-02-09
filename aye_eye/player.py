from aye_eye.util import handle_captures, initialise_state, print_state
import random


class Player:
    turns = 1

    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        self.player = player
        self.state = initialise_state(n)
        self.n = n

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        valid = [k for k, v in self.state.items() if not v["s"]]
        if self.n % 2 != 0 and Player.turns == 1:
            valid.remove((self.n // 2, self.n // 2))
        action = random.choice(valid)
        return ("PLACE", action[0], action[1])

    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of
        their chosen action. Update your internal representation of the
        game state based on this. The parameter action is the chosen
        action itself.

        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """
        self.state[(action[1], action[2])]["s"] = player
        handle_captures(self, action)
        # print_state(self.state)
        Player.turns += 1
