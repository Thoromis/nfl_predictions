import pandas as pd
import python_scripts.football_utility_functions as nfl
import utils.unit_keys as Units


def merge_and_save_data(unit_key):
    college_data = pd.read_csv('../processed_data/' + unit_key + '/' + unit_key + '_college_data.csv').iloc[:, 1:]
    nfl_data = pd.read_csv('../processed_data/' + unit_key + '/' + unit_key + '_nfl_data.csv').iloc[:, 1:]

    merged_data = college_data.merge(nfl_data, how='outer', left_on=['name', 'unit_key'],
                                     right_on=['full_player_name', 'unit_key'])
    nfl.write_nfl_players_to_csv(merged_data, unit_key)


def merge_player_data_from_files():
    # wr_college_data = pd.read_csv('../processed_data/wr_college_data.csv').iloc[:, 1:]
    # wr_nfl_data = pd.read_csv('../processed_data/wr_nfl_data.csv').iloc[:, 1:]
    # wr_merged = wr_college_data.merge(wr_nfl_data, how='left', left_on=['name', 'unit_key'],
    #                                   right_on=['full_player_name', 'unit_key'])
    # nfl.write_nfl_players_to_csv(wr_merged, 'wr_merged.csv')

    merge_and_save_data(Units.WR.KEY)
    merge_and_save_data(Units.RB.KEY)
    merge_and_save_data(Units.TE.KEY)
    merge_and_save_data(Units.QB.KEY)
