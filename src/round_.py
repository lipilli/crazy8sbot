# %%
class Round:
    def __init__(self, players, scores=None):
        """Input:
        players is a list of player ids
        scores is a list of scoes of equal lenght to players
        """
        self.players = players

        if scores:
            self.scores = scores
        else:
            self.scores = [0 for player in players]

    @property
    def won_by(self):
        # calculate maximum score and remember the player
        max_score = 0
        for player, score in zip(self.players, self.scores):
            if score > max_score:
                max_score = score
                winning_player = player
        
        return winning_player
# %%
