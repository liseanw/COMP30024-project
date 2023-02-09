"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This module contains some helper functions for printing actions and boards.
Feel free to use and/or modify them to help you develop your program.
"""

from itertools import islice
import numpy as np


def heuristic(start_x, start_y, goal_x, goal_y):
    start_z = -(start_x + start_y)
    goal_z = -(goal_x + goal_y)
    return max(abs(start_x - goal_x), abs(start_y - goal_y), abs(start_z - goal_z))


def create_board_dict(data):
    board = []
    for i in data["board"]:
        board += i
    start = ["s"] + data["start"]
    goal = ["g"] + data["goal"]
    board += start
    board += goal
    # Every 3 elements combines into format (r, q): s
    # where (r, q) are the coordinates
    # and s is the symbol.
    board_dict = {
        (board[j + 1], board[j + 2]): board[j] for j in range(0, len(board), 3)
    }
    return board_dict


def initialise_state(data):
    board_dict = create_board_dict(data)
    state = {}
    for r in range(0, data["n"]):
        for q in range(0, data["n"]):
            state[(r, q)] = {
                "f": np.inf,
                "g": np.inf,
                "h": heuristic(r, q, data["goal"][0], data["goal"][1]),
                "s": "",
                "p": (np.inf, np.inf),
            }

    for coordinate, symbol in board_dict.items():
        if (symbol == "b") or (symbol == "r"):
            state[coordinate]["s"] = symbol

    return state


def create_adjacent(current_hex, data, initial_board_dict):
    temp = []
    left = (current_hex[0], current_hex[1] - 1)
    top_left = (current_hex[0] + 1, current_hex[1] - 1)
    top_right = (current_hex[0] + 1, current_hex[1])
    right = (current_hex[0], current_hex[1] + 1)
    bottom_right = (current_hex[0] - 1, current_hex[1] + 1)
    bottom_left = (current_hex[0] - 1, current_hex[1])
    temp.append(left)
    temp.append(top_left)
    temp.append(top_right)
    temp.append(right)
    temp.append(bottom_right)
    temp.append(bottom_left)

    children = []
    for child in temp:
        if (
            (child[0] >= 0)
            and (child[0] < data["n"])
            and (child[1] >= 0)
            and (child[1] < data["n"])
        ):
            if child in initial_board_dict.keys():
                if (initial_board_dict[child] != "b") and (
                    initial_board_dict[child] != "r"
                ):
                    children.append(child)
            else:
                children.append(child)

    return children


def a_star_search(state, data, initial_board_dict):
    start = (data["start"][0], data["start"][1])
    goal = (data["goal"][0], data["goal"][1])
    open = []
    closed = []
    open.append((data["start"][0], data["start"][1]))
    state[start]["f"] = 0
    state[start]["g"] = 0
    while open:
        current_hex = open[0]
        for node in open:
            if state[node]["f"] < state[current_hex]["f"]:
                current_hex = node
            elif state[node]["f"] == state[current_hex]["f"]:
                if state[node]["h"] < state[current_hex]["h"]:
                    current_hex = node

        open.pop(open.index(current_hex))
        closed.append(current_hex)
        if current_hex == goal:
            path = []
            node = current_hex
            while node != (np.inf, np.inf):
                path.append(node)
                node = state[node]["p"]
            return path[::-1]
        children = create_adjacent(current_hex, data, initial_board_dict)
        for child in children:
            if child in closed:
                continue

            if child in open:
                if state[current_hex]["g"] + 1 > state[child]["g"]:
                    continue
                else:
                    state[child]["p"] = current_hex
                    state[child]["g"] = state[current_hex]["g"] + 1
                    state[child]["f"] = state[child]["g"] + state[child]["h"]

            else:
                state[child]["p"] = current_hex
                state[child]["g"] = state[current_hex]["g"] + 1
                state[child]["f"] = state[child]["g"] + state[child]["h"]
            open.append(child)


def print_solution(path):
    if path:
        print(len(path))
        for p in path:
            print(p)
    else:
        print(0)


def apply_ansi(str, bold=True, color=None):
    """
    Wraps a string with ANSI control codes to enable basic terminal-based
    formatting on that string. Note: Not all terminals will be compatible!
    Don't worry if you don't know what this means - this is completely
    optional to use, and not required to complete the project!

    Arguments:

    str -- String to apply ANSI control codes to
    bold -- True if you want the text to be rendered bold
    color -- Colour of the text. Currently only red/"r" and blue/"b" are
        supported, but this can easily be extended if desired...

    """
    bold_code = "\033[1m" if bold else ""
    color_code = ""
    if color == "r":
        color_code = "\033[31m"
    if color == "b":
        color_code = "\033[34m"
    return f"{bold_code}{color_code}{str}\033[0m"


def print_coordinate(r, q, **kwargs):
    """
    Output an axial coordinate (r, q) according to the format instructions.

    Any keyword arguments are passed through to the print function.
    """
    print(f"({r},{q})", **kwargs)


def print_board(n, board_dict, message="", ansi=False, **kwargs):
    """
    For help with visualisation and debugging: output a board diagram with
    any information you like (tokens, heuristic values, distances, etc.).

    Arguments:

    n -- The size of the board
    board_dict -- A dictionary with (r, q) tuples as keys (following axial
        coordinate system from specification) and printable objects (e.g.
        strings, numbers) as values.
        This function will arrange these printable values on a hex grid
        and output the result.
        Note: At most the first 5 characters will be printed from the string
        representation of each value.
    message -- A printable object (e.g. string, number) that will be placed
        above the board in the visualisation. Default is "" (no message).
    ansi -- True if you want to use ANSI control codes to enrich the output.
        Compatible with terminals supporting ANSI control codes. Default
        False.

    Any other keyword arguments are passed through to the print function.

    Example:

        >>> board_dict = {
        ...     (0, 4): "hello",
        ...     (1, 1): "r",
        ...     (1, 2): "b",
        ...     (3, 2): "$",
        ...     (2, 3): "***",
        ... }
        >>> print_board(5, board_dict, "message goes here", ansi=False)
        # message goes here
        #              .-'-._.-'-._.-'-._.-'-._.-'-.
        #             |     |     |     |     |     |
        #           .-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #          |     |     |  $  |     |     |
        #        .-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #       |     |     |     | *** |     |
        #     .-'-._.-'-._.-'-._.-'-._.-'-._.-'
        #    |     |  r  |  b  |     |     |
        #  .-'-._.-'-._.-'-._.-'-._.-'-._.-'
        # |     |     |     |     |hello|
        # '-._.-'-._.-'-._.-'-._.-'-._.-'

    """

    stitch_pattern = ".-'-._"
    edge_col_len = 3
    v_divider = "|"
    h_spacing = len(stitch_pattern)
    output = message + "\n"

    # Helper function to only selectively apply ansi formatting if enabled
    apply_ansi_s = apply_ansi if ansi else lambda str, **_: str

    # Generator to repeat pattern string (char by char) infinitely
    def repeat(pattern):
        while True:
            for c in pattern:
                yield c

    # Generate stitching pattern given some offset and length
    def stitching(offset, length):
        return "".join(islice(repeat(stitch_pattern), offset, length))

    # Loop through each row i from top (print ordering)
    # Note that n - i - 1 is equivalent to r in axial coordinates
    for i in range(n):
        x_padding = (n - i - 1) * int(h_spacing / 2)
        stitch_length = (n * h_spacing) - 1 + (int(h_spacing / 2) + 1 if i > 0 else 0)
        mid_stitching = stitching(0, stitch_length)

        # Handle coloured borders for ansi outputs
        # Fairly ugly code, but there is no "simple" solution
        if i == 0:
            mid_stitching = apply_ansi_s(mid_stitching, color="r")
        else:
            mid_stitching = (
                apply_ansi_s(mid_stitching[:edge_col_len], color="b")
                + mid_stitching[edge_col_len:-edge_col_len]
                + apply_ansi_s(mid_stitching[-edge_col_len:], color="b")
            )

        output += " " * (x_padding + 1) + mid_stitching + "\n"
        output += " " * x_padding + apply_ansi_s(v_divider, color="b")

        # Loop through each column j from left to right
        # Note that j is equivalent to q in axial coordinates
        for j in range(n):
            coord = (n - i - 1, j)
            value = str(board_dict.get(coord, ""))
            contents = value.center(h_spacing - 1)
            if ansi:
                contents = apply_ansi_s(contents, color=value)
            output += contents + (v_divider if j < n - 1 else "")
        output += apply_ansi_s(v_divider, color="b")
        output += "\n"

    # Final/lower stitching (note use of offset here)
    stitch_length = (n * h_spacing) + int(h_spacing / 2)
    lower_stitching = stitching(int(h_spacing / 2) - 1, stitch_length)
    output += apply_ansi_s(lower_stitching, color="r") + "\n"

    # Print to terminal (with optional args forwarded)
    print(output, **kwargs)
