
# %% imports
import card

# %% learning MinMax search
class Node():
    def __init__(self, data = None, children:set = set()):
        self.children = children
        self.data = data

# %% defining test nodes
n = Node()

n1 = Node(1)
n2 = Node(2)

na = Node(2)
nb = Node(6)
nc = Node(3)
nd = Node(5)

n.children = [n1, n2]
n1.children = [na, nb]
n2.children = [nc, nd]

# %% minmax

def minmax(nodes, depth=5, eval_min=min, eval_max=max): # TODO: This assumes 2 players. I need to modify it to account for up to 5
    """Minmax search in a tree of nodes. 
    
    Each branch must have the same length. Evaluation functions must be comparable by equality.
    
    Input:
    nodes (Node): Iterable of nodes. Their data and that of their children will be searched.
    
    depth: at what point should the search stop
    
    eval_min: function to evaluation the minimum value for data of child
    
    eval_max: same as eval_min for maximum
    
    Output:
    data of final child, as the evaluation functions return it
    """

    # base case for recursion: no more children or depth reached
    if len(nodes[0].children) == 0 or depth == 0:
        return eval_max([node.data for node in nodes])
    
    # recursive case
    else:
        node_values = []
        for node in nodes:
            value = minmax(node.children, depth=depth-1, eval_min=eval_max, eval_max=eval_min)
            node_values.append(value)
        return eval_max(node_values)

def best_move(hands, current_player, player_order):
    """Best move for crazy8 game.

    Input:
    hands: dict from int->set(Cards)
    current_player: one key of hands
    play_order: list of keys of hands
    
    Output:
    Best card for current player to play"""

    # TODO: Problem: Wie berechnen wir den Zufall beim Ziehen mit ein?

    starting_position = player_order.index(player)
    return
# %%
