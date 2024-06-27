from dataclasses import dataclass


@dataclass
class Team:
    ID: int
    year: int
    teamCode: str
    divID: str
    div_ID: int
    teamRank: int
    games: int
    gamesHome: int
    wins: int
    losses: int
    divisionWinnner: str
    leagueWinner: str
    worldSeriesWinnner: str
    runs: int
    hits: int
    homeruns: int
    stolenBases: int
    hitsAllowed: int
    homerunsAllowed: int
    name: str
    park: str
    somma_salari: float

    def __str__(self):
        return f"{self.teamCode} ({self.name})"

    def __repr__(self):
        return self.teamCode

    def __hash__(self):
        return hash(self.ID)