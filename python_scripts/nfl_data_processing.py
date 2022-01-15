import math

import pandas as pd
import utils.unit_keys as Units
import football_utility_functions as nfl
import classifier as classifier


def unify_position(position_x, position_y, position):
    if not pd.isna(position_x):
        return position_x
    elif not pd.isna(position_y):
        return position_y
    else:
        return position


def summarise_columns(col1, col2, col3=0.0):
    if pd.isna(col1):
        col1 = 0.0
    if pd.isna(col2):
        col2 = 0.0
    if pd.isna(col3):
        col3 = 0.0
    return col1 + col2 + col3


# Classify NFL players based on read statistics for the players
def process_nfl_offensive_data():
    combined_roster = nfl.read_nfl_rosters_in_year_range(2009, 2019)

    # read offensive statistics
    receiving_stats = nfl.read_receiver_stats_for_players(combined_roster)
    rushing_stats = nfl.read_rushing_stats_for_players(combined_roster)
    passing_stats = nfl.read_passing_stats_for_players(combined_roster)

    combined_offensive_stats = receiving_stats.merge(passing_stats, how='outer', left_on=['gsis_id'],
                                           right_on=['gsis_id']).merge(rushing_stats, how='outer',
                                                                       left_on=['gsis_id'],
                                                                       right_on=['gsis_id'])
    combined_offensive_stats['position_key'] = combined_offensive_stats.apply(
        lambda x: unify_position(x['position_x'], x['position_y'], x['position']), axis=1)
    combined_offensive_stats['Total_Yards'] = combined_offensive_stats.apply(
        lambda x: summarise_columns(x['Total_Yards_x'], x['Total_Yards_y'], x['Total_Yards']), axis=1)
    combined_offensive_stats['Fumbles'] = combined_offensive_stats.apply(
        lambda x: summarise_columns(x['Fumbles_y'], x['Fumbles_x']), axis=1)
    combined_offensive_stats['TDs'] = combined_offensive_stats.apply(
        lambda x: summarise_columns(x['TDs_x'], x['TDs_y'], x['TDs']), axis=1)
    combined_offensive_stats['season_helper'] = combined_offensive_stats.apply(
        lambda x: max(x['rec_season_helper'], x['rush_season_helper'], x['pass_season_helper']), axis=1)

    # Total_Yards_x + Total_Yards_y + Total_Yards (rushing)
    # Fumbles_y + Fumbles_x
    # TDs_x + TDs_y + TDs (rushing)
    # season_helper = rec_season_helper + rush_season_helper + pass_season_helper

    # combined stats holds for all offensive groups now statistics with proper unit key
    # TODO unify unit key (should likely still be FB, RB, etc.)
    dataset_offensive_stats = nfl.normalize_positions_of_players(combined_offensive_stats, 'position_key') # after this, 'unit_key' shall be used

    # TODO split up units into single dataframes
    wr_stats = nfl.get_position_specific_data(dataset_offensive_stats, Units.WR.KEY)
    rb_stats = nfl.get_position_specific_data(dataset_offensive_stats, Units.RB.KEY)
    te_stats = nfl.get_position_specific_data(dataset_offensive_stats, Units.TE.KEY)
    qb_stats = nfl.get_position_specific_data(dataset_offensive_stats, Units.QB.KEY)

    # TODO classify single unit dataframes
    classifier.classify_dataframe(rb_stats, classifier.standard_classifiers_rb(), Units.RB)
    classifier.classify_by_single_classifier(rb_stats, classifier.standard_classifiers_rb(), Units.RB)

    classifier.classify_dataframe(wr_stats, classifier.standard_classifiers_wr(), Units.WR)
    classifier.classify_by_single_classifier(wr_stats, classifier.standard_classifiers_wr(), Units.WR)

    classifier.classify_dataframe(te_stats, classifier.standard_classifiers_te(), Units.TE)
    classifier.classify_by_single_classifier(te_stats, classifier.standard_classifiers_te(), Units.TE)

    classifier.classify_dataframe(qb_stats, classifier.standard_classifiers_qb(), Units.QB)
    classifier.classify_by_single_classifier(qb_stats, classifier.standard_classifiers_qb(), Units.QB)

    # TODO save classified units into files
    nfl.write_nfl_players_to_csv_no_stats(rb_stats, Units.RB.KEY, None) # classifier.convert_to_string_list(classifier.standard_classifiers_rb()))
    nfl.write_nfl_players_to_csv_no_stats(te_stats, Units.TE.KEY, None) # classifier.convert_to_string_list(classifier.standard_classifiers_wr()))
    nfl.write_nfl_players_to_csv_no_stats(wr_stats, Units.WR.KEY, None) # classifier.convert_to_string_list(classifier.standard_classifiers_te()))
    nfl.write_nfl_players_to_csv_no_stats(qb_stats, Units.QB.KEY, None) # classifier.convert_to_string_list(classifier.standard_classifiers_qb()))


def process_nfl_defensive_data():
    defensive_stats = nfl.read_csv('../unprocessed_nfl_data/statistics/defensive_statistics.csv')
    defensive_stats['gsis_id'] = defensive_stats['player_id']
    defensive_stats['full_player_name'] = defensive_stats['player_name']
    defensive_stats.drop(columns=['player_id', 'player_name'])

    lb_stats = nfl.get_position_specific_data(defensive_stats, Units.LB.KEY)
    classifier.classify_by_single_classifier(lb_stats, classifier.standard_classifiers_lb(), Units.LB)

    db_stats = nfl.get_position_specific_data(defensive_stats, Units.DB.KEY)
    classifier.classify_by_single_classifier(db_stats, classifier.standard_classifiers_db(), Units.DB)

    dl_stats = nfl.get_position_specific_data(defensive_stats, Units.DL.KEY)
    classifier.classify_by_single_classifier(dl_stats, classifier.standard_classifiers_dl(), Units.DL)

    classifier.classify_dataframe(lb_stats, classifier.standard_classifiers_lb(), Units.LB)
    classifier.classify_dataframe(db_stats, classifier.standard_classifiers_db(), Units.DB)
    classifier.classify_dataframe(dl_stats, classifier.standard_classifiers_dl(), Units.DL)

    nfl.write_nfl_players_to_csv_no_stats(lb_stats, Units.LB.KEY, None)
    nfl.write_nfl_players_to_csv_no_stats(db_stats, Units.DB.KEY, None)
    nfl.write_nfl_players_to_csv_no_stats(dl_stats, Units.DL.KEY, None)





