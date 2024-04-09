from ..common import Common
from trueskill import Rating

class Team(Common):
    position : int
    grade : float

    def __init__(self, name : str, position : int = 0, grade : float = 0.0):
        super().__init__(name)
        self.position = position
        self.grade = grade

    def __repr__(self):
        return f"{self.name}: {self.position}º @ {self.grade:.0f}"

    @property
    def to_dict(self):
        return {
            "name": self.name,
            "grade": self.grade
        }

class TrueSkillTeam(Team):
    rating : Rating

    def __init__(self, name : str, mu : float = None, sigma : float = None):
        self.name = name
        self.position = 0
        if mu and sigma:
            self.rating = Rating(mu, sigma)
        else:
            self.rating = Rating()


    def __repr__(self):
        return f"{self.name}: {self.position}º @ {self.rating.mu:.0f}, {self.rating.sigma:.0f} -> {self.grade:.0f}"

    @property
    def mu(self):
        return self.rating.mu
    
    @property
    def sigma(self):
        return self.rating.sigma

    @property
    def grade(self):
        return self.mu - 3*self.sigma
    
