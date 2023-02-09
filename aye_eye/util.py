import numpy as np


def initialise_state(n):
    """
    Initialises and returns an empty board of size n.

    Arguments:

    n -- The size of the board

    """
    state = {}
    for r in range(0, n):
        for q in range(0, n):
            state[(r, q)] = {
                "f": np.inf,
                "g": np.inf,
                "h": np.inf,
                "s": "",
                "p": (np.inf, np.inf),
            }
    return state


def print_state(state):
    """
    Prints the state in `(r, q): {}` format.

    Arguments:

    state -- The state

    """
    for k, v in state.items():
        print(f"{k}: {v}")


def adjacent(parent, n):
    temp = []
    left = (parent[0], parent[1] - 1)
    top_left = (parent[0] + 1, parent[1] - 1)
    top_right = (parent[0] + 1, parent[1])
    right = (parent[0], parent[1] + 1)
    bottom_right = (parent[0] - 1, parent[1] + 1)
    bottom_left = (parent[0] - 1, parent[1])
    temp.append(left)
    temp.append(top_left)
    temp.append(top_right)
    temp.append(right)
    temp.append(bottom_right)
    temp.append(bottom_left)

    children = []
    for child in temp:
        if (child[0] >= 0) and (child[0] < n) and (child[1] >= 0) and (child[1] < n):
            children.append(child)

    return children


def handle_captures(player, action):
    # two = (action[1]+1, action[2]+1)
    # four = (action[1]-1, action[2]+2)
    # six = (action[1]-2, action[2]+1)
    # eight = (action[1]-1, action[2]-1)
    # ten = (action[1]+1, action[2]-2)
    # twelve = (action[1]+2, action[2]-1)

    outer_temp = [
        (action[1] + 1, action[2] + 1),
        (action[1] - 1, action[2] + 2),
        (action[1] - 2, action[2] + 1),
        (action[1] - 1, action[2] - 1),
        (action[1] + 1, action[2] - 2),
        (action[1] + 2, action[2] - 1),
    ]

    outer = [
        o
        for o in outer_temp
        if ((o[0] >= 0) and (o[0] < player.n) and (o[1] >= 0) and (o[1] < player.n))
    ]

    temp = []
    inner = adjacent((action[1], action[2]), player.n)
    for i in inner:
        if player.state[i]["s"] == player.state[(action[1], action[2])]["s"]:
            temp.append(list(set(inner).intersection(set(adjacent(i, player.n)))))
    for o in outer:
        if player.state[o]["s"] == player.state[(action[1], action[2])]["s"]:
            temp.append(list(set(inner).intersection(set(adjacent(o, player.n)))))

    pairs = []
    for pair in temp:
        if len(pair) == 2 and (
            player.state[pair[0]]["s"]
            and player.state[pair[1]]["s"]
            and player.state[pair[0]]["s"] != player.state[(action[1], action[2])]["s"]
            and player.state[pair[1]]["s"] != player.state[(action[1], action[2])]["s"]
        ):
            pairs.append(pair)
    for pair in pairs:
        player.state[pair[0]]["s"] = ""
        player.state[pair[1]]["s"] = ""
