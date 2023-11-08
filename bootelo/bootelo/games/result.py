from ..common import Common
from .score import Score

class Result(Common):
    winner : int
    score : Score
    def __init__(self, winner : int, score : Score):
        self.winner = winner
        self.score = score