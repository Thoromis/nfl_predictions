import pandas as pd
import python_scripts.football_utility_functions as nfl


def merge_player_data_from_files():
    wr_college_data = pd.read_csv('../processed_data/wr_college_data.csv').iloc[:, 1:]
    wr_nfl_data = pd.read_csv('../processed_data/wr_nfl_data.csv').iloc[:, 1:]

    wr_merged = wr_college_data.merge(wr_nfl_data, how='left', left_on=['name', 'unit_key'],
                                      right_on=['full_player_name', 'position'])

    # combine with other player data

    # write back to csv