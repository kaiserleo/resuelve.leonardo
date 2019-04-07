from decimal import Decimal
from resuelvefc.exceptions import *

class Salaries(object):
    goals_per_level_dict = {'A': 5, 'B': 10, 'C': 15, 'Cuauh': 20}
    TWOPLACES = Decimal(10) ** -2

    def __init__(self, all_player_stats):
        self.player_stats = all_player_stats
        self.team_goal = dict()
        self.team_scored = dict()


    def process(self):
        self.resolve_players_level()
        self.grouping_teams()

        for player in self.player_stats:
            player['sueldo_completo'] = self.get_player_salary(player)

        return self.player_stats

    def resolve_players_level(self):
        for player in self.player_stats:
            player_level = player['nivel']

            player_goal = self.goals_per_level(player_level)
            player['goles_minimos'] = player_goal


    def grouping_teams(self):
        for player in self.player_stats:
            player_team = player['equipo']
            player_goal = player['goles_minimos']
            player_scored = player['goles']

            # Scored goals per team
            current_team_scored = self.team_scored.get(player_team, 0)
            new_team_scored = current_team_scored + player_scored
            self.team_scored[player_team] = new_team_scored

            # Team required goals to achieve
            current_team_goal = self.team_goal.get(player_team, 0)
            new_team_goal = player_goal + current_team_goal
            self.team_goal[player_team] = new_team_goal


    def get_player_salary(self, player):
        player_fixed = Decimal(player['sueldo'])
        player_bonus = Decimal(player['bono'])
        player_team = player['equipo']

        player_rate = self.player_rating(player)
        team_rate = self.team_rating(player_team)

        # 50% personal rate + 50% team rate
        final_bonus = player_bonus * (player_rate + team_rate) / 2
        final_salary = player_fixed + final_bonus.quantize(Salaries.TWOPLACES)
        return final_salary


    def team_rating(self, team_name):
        one = Decimal(1)
        rate = Decimal(self.team_scored[team_name]) \
               / Decimal(self.team_goal[team_name])
        if( rate > one ):
            return one
        else:
            return rate


    def player_rating(self, player):
        one = Decimal(1)
        rate = Decimal(player['goles']) \
               / Decimal(player['goles_minimos'])
        if( rate > one ):
            return one
        else:
            return rate


    def goals_per_level(self, level):
        if not level in self.goals_per_level_dict:
            raise LevelNotFoundException(level + ' level does not exist')

        return self.goals_per_level_dict[level]
