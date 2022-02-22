import pandas as pd
import python_scripts.football_utility_functions as nfl
import utils.unit_keys as Units


def classify_unclassified_row(classification_all, classify_numeric=False):
    if pd.isna(classification_all):
        return 'Bust' if not classify_numeric else 0
        # Player apparently didn't make the NFL roster of the team that draft him, so classify as Bust
    else:
        return classification_all


def merge_and_save_data(unit_key):
    college_data = pd.read_csv('../processed_data/' + unit_key + '/' + unit_key + '_college_data.csv').iloc[:, 1:]
    nfl_data = pd.read_csv('../processed_data/' + unit_key + '/' + unit_key + '_nfl_data.csv').iloc[:, 1:]

    merged_data = college_data.merge(nfl_data, how='outer', left_on=['name', 'unit_key'],
                                     right_on=['full_player_name', 'unit_key'])

    merged_data['full_player_name'] = merged_data['name']
    merged_data['Classification_All'] = merged_data.apply(
        lambda x: classify_unclassified_row(x['Classification_All']), axis=1)
    merged_data['Classification_All_num'] = merged_data.apply(
        lambda x: classify_unclassified_row(x['Classification_All_num'], True), axis=1)
    merged_data.dropna(inplace=True, subset=['name'])
    nfl.write_nfl_players_to_csv(merged_data, unit_key)


# Merge players for the given positions from college and NFL
def merge_player_data_from_files():
    merge_and_save_data(Units.WR.KEY)
    merge_and_save_data(Units.RB.KEY)
    merge_and_save_data(Units.TE.KEY)
    merge_and_save_data(Units.QB.KEY)
    merge_and_save_data(Units.LB.KEY)
    merge_and_save_data(Units.DB.KEY)
    merge_and_save_data(Units.DL.KEY)
