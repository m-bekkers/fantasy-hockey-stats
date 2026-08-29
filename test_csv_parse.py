from __future__ import annotations

DATA_FILES = ["skaters.csv", "goalies.csv", "skaters_2008_to_2024.csv", "goalies_2008_to_2024.csv"]
PREFIX = "C:\\Users\\matth\\OneDrive\\Code\\fantasy-hockey-stats\\data\\"

'''
Format:
Non-goalies: list[dict
                        {
                            player_id: int, -> PRIMARY KEY
                            player_name: string
                            seasons: list[dict{
                                                season: int
                                                team: string
                                                position: string,
                                                games_played: int,
                                                situation: list[dict{
                                                                    situation: string
                                                                    icetime: int
                                                                    shifts: int
                                                                    gameScore: float
                                                                    onIce_xGoalsPercentage: float
                                                                    offIce_xGoalsPercentage: float
                                                                    onIce_corsiPercentage: float
                                                                    offIce_corsiPercentage: float
                                                                    iceTimeRank: int
                                                                    I_F_xOnGoal: float
                                                                    I_F_xGoal: float
                                                                    I_F_xRebounds: float
                                                                    I_F_xPlayContinuedInZone: float
                                                                    I_F_shotsOnGoal: int
                                                                    I_F_shotAttempts: int
                                                                    I_F_points: int
                                                                    I_F_goals: int
                                                                    I_F_assists: int
                                                                    I_F_rebounds: int
                                                                    I_F_reboundGoals: int
                                                                    I_F_playContrinuedInZone: int
                                                                    }
                                                                ]
                                                }
                                    ]
                        }
                ]
'''

class Season:
    def __init__(self, season: int, team: str, games_played: int):
        self.season = season
        self.team = team
        self.games_played = games_played
        self.situations = []

class Situation:
    def __init__(self, situation: str, icetime: float, headers: list[str], header_entries: list[str]):
        self.situation = situation
        self.icetime = icetime
        if len(headers) != len(header_entries):
            raise ValueError("Headers and header entries don't match!")
        for header, entry in zip(headers, header_entries):
            setattr(self, header, entry)

class Player:
    def __init__(self, id: int, name: str, position: str = "G") -> None:
        self.id = id
        self.name = name
        self.position = position # Defaults to goalie, forwards and defenders pass their positions on init
        self.seasons = []

    def _check_season_record_exists(self, season: int) -> bool:
        for s in self.seasons:
            if getattr(s, 'season', None) == season:
                return True
        return False
    
    def add_season(self, season: int, team: str, games_played: int) -> None:

        # Check to see if we have an existing entry for this season, if not, create one
        if not self._check_season_record_exists(season):
            season_record = Season(season, team, games_played)
            self.seasons.append(season_record)

class Forward(Player):
    def __init__(self, id: int, name: str, position: str):
        super().__init__(id, name, position)
        self.position = position

    def add_situation(self, situation: str, icetime: float, fileline: list[str]) -> None:
        headers = f_d_headers[8:]
        header_entries = fileline[8:]

        # Here, we make the assumption that there we will never encounter a duplicate situation record for a given season
        situation_record = Situation(situation, icetime, headers, header_entries)

        # We will also assume that anytime we attempt to add a situation record, a matching season has already been added.
        for season_record in self.seasons:
            if season_record.season == season:
                season_record.situations.append(situation_record)
                break
            


class Defender(Player):
    def __init__(self, id, name, position: str):
        super().__init__(id, name, position)

class Goalie(Player):
    def __init__(self, id, name):
        super().__init__(id, name)

f_d_headers = []
g_headers = []
forwards: list[Forward] = []
defences = []
goalies = []
seen_players = []

def find_player_by_id(player_id, players) -> Player | None:
    for player in players:
        if player.id == player_id:
            return player

    return None

for file in DATA_FILES:
    header_seen = False
    filename = PREFIX + file
    with open(filename, "r") as f:
        for line in f:

            seen = False

            line = line.split(",")

            if not header_seen:
                line[-1] = line[-1][:-2]
                if file in ["goalies.csv", "goalies_2008_to_2024.csv"] and g_headers == []:
                    g_headers = line
                elif file in ["skaters.csv", "skaters_2008_to_2024.csv"] and f_d_headers == []:
                    f_d_headers = line
                header_seen = True
                continue

            player_id = int(line[0])
            season = int(line[1])
            player_name = line[2]
            position = line[4]
            team = line[3]
            situation = line[5]
            games_played = int(line[6])
            icetime = float(line[7])

            # create player record if first time seen
            if player_id not in seen_players:
                seen_players.append(player_id)
                if position in ["C", "L", "R"]:
                    player = Forward(player_id, player_name, position)
                    forwards.append(player)
                elif position == "D":
                    player = Defender(player_id, player_name, position)
                    defences.append(player)
                else: # assume G
                    player = Goalie(player_id, player_name)
                    goalies.append(player)

            # resolve the player object reference for this row
            if position in ["C", "L", "R"]:
                player = find_player_by_id(player_id, forwards)
            elif position == "D":
                player = find_player_by_id(player_id, defences)
            else: # assume G
                player = find_player_by_id(player_id, goalies)

            # always attach season and situation for skaters so multiple rows accumulate
            if player is not None and position in ["C", "L", "R"]:
                player.add_season(season, team, games_played)
                player.add_situation(situation, icetime, line)

    f.close()

forwards.sort(key=lambda player: player.id)
goalies.sort(key=lambda player: player.id)
defences.sort(key=lambda player: player.id)

#print(f_d_headers)

'''
print("\n\n\n*************************************************")
print("FORWARDS")
print("*************************************************")
for player in forwards:
    print(player.name)


print("\n\n\n*************************************************")
print("DEFENCES")
print("*************************************************")
for player in defences:
    print(player.name)

print("\n\n\n*************************************************")
print("GOALIES")
print("*************************************************")
for player in goalies:
    print(player.name)

print(f"\n\nTotal forwards: {len(forwards)}")
print(f"Total defences: {len(defences)}")
print(f"Total goalies: {len(goalies)}")
'''

#for head in table_headers:
#    print(head)


def print_player_stats(player):
    # header
    print(f"Player id: {player.id}, name: {player.name}, position: {player.position}")

    if not player.seasons:
        print("  (no seasons)")
    else:
        for season in player.seasons:
            print(f"  Season: {season.season}, Team: {season.team}, Games: {season.games_played}")
            situations = getattr(season, 'situations', []) or []
            if not situations:
                print("    (no situations)")
            for sit in situations:
                sit_situation = getattr(sit, 'situation', '')
                sit_icetime = getattr(sit, 'icetime', '')
                print(f"    Situation: {sit_situation}, Icetime: {sit_icetime}")
                for k, v in vars(sit).items():
                    if k in ('situation', 'icetime'):
                        continue
                    print(f"      {k}: {v}")

    print()

for player in forwards:
    if len(player.seasons) == 1:
        print_player_stats(player)
        break