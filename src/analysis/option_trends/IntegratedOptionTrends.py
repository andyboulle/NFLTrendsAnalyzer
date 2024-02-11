#################################################################################
# IntegratedOptionTrends.py                                                     #
#                                                                               #
# This file calculates the record for trends that have to do with all possible  #
# combinations of betting information and game information about the given game.# 
# It combines the GameOptionTrends and BettingOptionTrends to get every         #
# combination of game and betting info and gets dataframes matching the         #
# criteria of these combinations. Then it uses BasicTrends to find all basic    #
# trends for the combination dataframes. The toString method prints all of      #
# these records on their own line.                                              #
#                                                                               #
# Examples:                                                                     #
# - games where the spread is 7 and the total is 47.5 or lower and the month is #
#   10 and it is the regular season                                             #
# - games where the spread is 2.0 or more and the total is 52.5 or lower and    # 
#   the day of the week is Sunday and it is a divisional game                   #
# - games where the total is 43.5 and the day of the week is Sunday and it is a # 
#   divisional game                                                             #
#################################################################################
from src.analysis.option_trends.GameOptionTrends import GameOptionTrends
from src.analysis.option_trends.BettingOptionTrends import BettingOptionTrends
from src.analysis.basic_trends.BasicTrends import BasicTrends
from src.analysis.objects.Game import Game
from src.analysis.objects.NamedDataframe import NamedDataframe
import pandas as pd

class IntegratedOptionTrends:
    
    named_df = None
    df = None

    game = None

    game_option_finder = None
    betting_option_finder = None

    spread = None
    total = None

    day_of_week = None
    month = None
    playoff = None
    divisional = None

    trends = None

    def __init__(self, named_df, game):
        self.named_df = named_df
        self.df = named_df.df
        self.game = game
        self.betting_option_finder = BettingOptionTrends(named_df, game)
        self.spread = self.betting_option_finder.spread
        self.total = self.betting_option_finder.total
        self.trends = self.get_all_trends()

    def get_spread_combo_dataframes(self):
        spread_combo_dfs = []

        spread_dataframes = self.betting_option_finder.get_spread_dataframes(self.df, self.spread)

        for df in spread_dataframes:
            spread_string = df.description
            game_options = GameOptionTrends(df, self.game)
            trends = game_options.get_option_combination_dataframes()

            for trend in trends:
                option_string = trend.description[(trend.description.find('in games where') + 13):].strip()
                trend.description = f'{spread_string}and {option_string} '
                spread_combo_dfs.append(trend)

        return spread_combo_dfs
        
    def get_spread_combo_trends(self):
        spread_combo_trends = []
        spread_combo_dataframes = self.get_spread_combo_dataframes()

        for df in spread_combo_dataframes:
            trends = BasicTrends(df, self.game).trends
            spread_combo_trends += trends

        return spread_combo_trends
    
    def get_total_combo_dataframes(self):
        total_combo_dfs = []

        total_dataframes = self.betting_option_finder.get_total_dataframes(self.df, self.total)

        for df in total_dataframes:
            total_string = df.description
            game_options = GameOptionTrends(df, self.game)
            trends = game_options.get_option_combination_dataframes()

            for trend in trends:
                option_string = trend.description[(trend.description.find('in games where') + 13):].strip()
                trend.description = f'{total_string}and {option_string} '
                total_combo_dfs.append(trend)

        return total_combo_dfs
        
    def get_total_combo_trends(self):
        total_combo_trends = []
        total_combo_dataframes = self.get_total_combo_dataframes()

        for df in total_combo_dataframes:
            trends = BasicTrends(df, self.game).trends
            total_combo_trends += trends

        return total_combo_trends
    
    def get_spread_and_total_combo_dataframes(self):
        spread_and_total_combo_dfs = []

        spread_and_total_dataframes = self.betting_option_finder.get_spread_and_total_dataframes(self.df, self.spread, self.total)

        for df in spread_and_total_dataframes:
            spread_and_total_string = df.description
            game_options = GameOptionTrends(df, self.game)
            trends = game_options.get_option_combination_dataframes()

            for trend in trends:
                option_string = trend.description[(trend.description.find('in games where') + 13):].strip()
                trend.description = f'{spread_and_total_string}and {option_string} '
                spread_and_total_combo_dfs.append(trend)

        return spread_and_total_combo_dfs
    
    def get_spread_and_total_combo_trends(self):
        spread_and_total_combo_trends = []
        spread_and_total_combo_dataframes = self.get_spread_and_total_combo_dataframes()

        for df in spread_and_total_combo_dataframes:
            trends = BasicTrends(df, self.game).trends
            spread_and_total_combo_trends += trends

        return spread_and_total_combo_trends
    
    def get_all_dataframes(self):
        spread_combo_dataframes = self.get_spread_combo_dataframes()
        total_combo_dataframes = self.get_total_combo_dataframes()
        spread_and_total_combo_dataframes = self.get_spread_and_total_combo_dataframes()

        return [spread_combo_dataframes, total_combo_dataframes, spread_and_total_combo_dataframes]
    
    def get_all_trends(self):
        all_trends = []

        spread_trends = self.get_spread_combo_trends()
        total_trends = self.get_total_combo_trends()
        spread_and_total_trends = self.get_spread_and_total_combo_trends()

        all_trends += spread_trends
        all_trends += total_trends
        all_trends += spread_and_total_trends

        return all_trends
    
    def __str__(self):
        returner = ''
        for trend in self.trends:
            returner += str(trend) + '\n'
        return returner