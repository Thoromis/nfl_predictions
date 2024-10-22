import numpy as np
import pandas as pd
import python_scripts.utils.unit_keys as Units

# base_columns = ['Player Code', 'Team Code', 'name', 'unit_key', 'season_x', 'draft_season', 'round', 'pick', 'age']
base_columns = ['Player Code', 'Team Code', 'name', 'unit_key', 'draft_season']


def align_positions(position):
    if position == 'T' or position == 'G' or position == 'C' \
            or position == 'OL' or position == 'OT' or position == 'OG':
        return Units.OL
    elif position == 'DB' or position == 'CB' or position == 'FS' or position == 'S' or position == 'SS' or position == 'SAF':
        return Units.DB.KEY
    elif position == 'DL' or position == 'NT' or position == 'DE' or position == 'DT':
        return Units.DL.KEY
    elif position == 'LB' or position == 'OLB' or position == 'MLB' or position == 'ILB':
        return Units.LB.KEY
    elif position == 'RB' or position == 'FB' or position == 'TB':
        return Units.RB.KEY
    elif position == 'WR' or position == 'SE':
        return Units.WR.KEY
    elif position == 'K' or position == 'P':
        return Units.K
    else:
        return position


def merge_transferred_players(aggregated_stats):
    aggregated_stats['pk_id'] = np.NaN
    for (index, row) in aggregated_stats.iterrows():
        # see if player exists multiple times in dataframe
        working_df = aggregated_stats[aggregated_stats['name'] == row['name']][
            aggregated_stats['unit_key'] == row['unit_key']]
        if working_df.shape[0] <= 1:
            aggregated_stats.at[index, 'pk_id'] = aggregated_stats.at[
                index, 'Player Code']  # set local pk for aggregating later
            continue  # Player only exists once

        # player exists multiple times (and is less than 3 years apart in college (likely to be the same player)
        elif (working_df['draft_season'].max() - working_df['draft_season'].min()) < 3:
            # get index of other rows
            for (_, working_df_row) in working_df.iterrows():
                aggregated_stats.at[working_df_row.name, 'pk_id'] = working_df['Player Code'].iloc[0]
                # Set to first appearing id
            # aggregated_stats.at[index, 'pk_id'] = working_df['Player Code'][0]
            continue  # Difference between active seasons too big - probably not a transfer
    return aggregated_stats.dropna(subset=['pk_id'])


# support for units: WR, RB, QB, DL, LB, DB, TE
# ,Team Code,name,unit_key,draft_season,Fum Ret,Fum Ret Yard,Fum Ret TD,Int Ret,
# Int Ret Yard,Int Ret TD,Tackle Solo,Tackle Assist,Tackle For Loss,Sack,QB Hurry,
# Fumble Forced,Pass Broken Up,full_player_name,gsis_id,Classification_All,Classification_All_num
def select_features_for_unit(ml_dataset, unit_key):
    if unit_key == Units.WR.KEY:
        return ml_dataset[
            ['full_player_name', 'Rush Yard', 'Rush TD', 'Rec Yards', 'Rec TD']]
    if unit_key == Units.RB.KEY:
        return ml_dataset[
            ['full_player_name', 'Rush Yard', 'Rush TD', 'Rec Yards', 'Rec TD']]
    if unit_key == Units.LB.KEY:
        return ml_dataset[
            ['full_player_name', 'Tackle Solo', 'Tackle Assist', 'Sack', 'QB Hurry', 'Fumble Forced', 'Int Ret',
             'Tackle For Loss', 'Pass Broken Up']]
    if unit_key == Units.DL.KEY:
        return ml_dataset[
            ['full_player_name', 'Tackle Solo', 'Sack', 'QB Hurry', 'Fumble Forced',]]
            # Rush Att, Rec, 'Pass Broken Up'
    if unit_key == Units.DB.KEY:
        return ml_dataset[
            ['full_player_name', 'Tackle Solo', 'Tackle Assist', 'Tackle For Loss', 'Fumble Forced',
             'Pass Broken Up', 'Int Ret', 'Sack', ]]
    if unit_key == Units.QB.KEY:
        return ml_dataset[
            ['full_player_name', 'Rush Att', 'Rush Yard', 'Rush TD', 'Pass Comp', 'Pass TD',
             'Pass Int', 'Comp Percentage']]  # 'Pass Yard', 'Pass Att',
    if unit_key == Units.TE.KEY:
        return ml_dataset[['full_player_name', 'Rec', 'Rec Yards', 'Rec TD']]


def normalize_positions_of_players(data, position_column_key):
    data["unit_key"] = data[position_column_key].apply(align_positions)
    return data


def read_and_normalize_draft_file(file, position_column, after=2005, before=2020):
    draft_data = pd.read_csv(file)
    draft_data.dropna()
    draft_data = draft_data[after < draft_data.season]
    draft_data = draft_data[before > draft_data.season]
    draft_data = normalize_positions_of_players(draft_data, position_column)
    return draft_data


def read_merged_file_for_unit(unit_key):
    return read_csv('../processed_data/' + unit_key + '/' + unit_key + '_merged.csv')


def read_csv(file):
    return pd.read_csv(file)


def write_nfl_players_to_csv(data, unit_key):
    data.to_csv('../processed_data/' + unit_key + '/' + unit_key + '_merged.csv')


def write_nfl_players_to_csv_no_stats(data, unit_key, classifier_columns=None):
    standard_columns = ['full_player_name', 'unit_key', 'gsis_id', 'Classification_All', 'Classification_All_num']

    # only 'all' classification done - therefore no need for other classifier columns
    if classifier_columns is not None:
        standard_columns.extend(classifier_columns)

    csv_data = data[standard_columns]
    csv_data.to_csv('../processed_data/' + unit_key + '/' + unit_key + '_nfl_data.csv')


def combine_statistics(receivering_stats, rushing_stats, passing_stats):
    result = receivering_stats.merge(rushing_stats, left_on=['gsis_id'], right_on=['gsis_id'])
    result = result.merge(passing_stats, left_on=['gsis_id'], right_on=['gsis_id'])
    return result


def read_passing_stats_for_players(players_df):
    passing_stats = pd.read_csv("../unprocessed_nfl_data/statistics/season_passing_df.csv")
    passing_stats = passing_stats[
        ['Passer_ID', 'Attempts', 'Completions', 'Drives', 'Total_Yards', 'Interceptions', 'TDs']]
    passing_stats['pass_season_helper'] = 1
    passing_stats = passing_stats.groupby(['Passer_ID']).sum()
    passing_stats = passing_stats.merge(players_df, left_on=['Passer_ID'], right_on=['gsis_id'])
    return passing_stats


def read_rushing_stats_for_players(players_df):
    rushing_stats = pd.read_csv("../unprocessed_nfl_data/statistics/season_rushing_df.csv")
    rushing_stats = rushing_stats[
        ['Rusher_ID', 'Carries', 'Total_Yards', 'Fumbles', 'TDs']]
    rushing_stats['rush_season_helper'] = 1
    rushing_stats = rushing_stats.groupby(['Rusher_ID']).sum()
    rushing_stats = rushing_stats.merge(players_df, left_on=['Rusher_ID'], right_on=['gsis_id'])
    return rushing_stats


def read_receiver_stats_for_players(players_df):
    receiving_stats = pd.read_csv("../unprocessed_nfl_data/statistics/season_receiving_df.csv")
    receiving_stats = receiving_stats[
        ['Receiver_ID', 'Targets', 'Receptions', 'Drives', 'Total_Yards', 'Total_Raw_YAC', 'Total_Caught_YAC',
         'Fumbles', 'TDs', 'AC_TDs', 'Total_Caught_AirYards']]
    receiving_stats['rec_season_helper'] = 1
    receiving_stats = receiving_stats.groupby(['Receiver_ID']).sum()
    receiving_stats = receiving_stats.merge(players_df, left_on=['Receiver_ID'], right_on=['gsis_id'])
    return receiving_stats


def read_nfl_rosters_in_year_range(from_year, to_year):
    roster = pd.DataFrame()
    for i in range(from_year, to_year):
        yearly_roster = read_nfl_rosters_for_year(i)
        roster = roster.append(yearly_roster)
    roster = roster.drop(axis=1, labels=['season', 'season_type', 'team'])
    roster = roster.drop_duplicates(subset=["gsis_id"])
    return roster


def read_nfl_rosters_for_year(year):
    yearly_roster = pd.read_csv("../unprocessed_nfl_data/rosters/reg_roster_" + str(year) + ".csv")
    return yearly_roster


def read_nfl_statistics_file(file):
    statistics = pd.read_csv("../unprocessed_nfl_data/statistics/" + str(file))
    return statistics


def read_and_normalize_player_data_for_year(year, position_column):
    player_data_for_year = pd.read_csv(
        "../unprocessed_college_data/collegefootballstatistics/cfbstats-com-" + str(year) + "-1-5-0/player.csv")
    player_data_for_year["season"] = year
    player_data_for_year["draft_season"] = year + 1
    player_data_for_year["season_counter"] = 1
    player_data_for_year["name"] = player_data_for_year["First Name"] + " " + player_data_for_year["Last Name"]
    player_data_for_year = normalize_positions_of_players(player_data_for_year, position_column)
    return player_data_for_year


def read_and_normalize_combine_data(file):
    combine_data = pd.read_csv(file)
    combine_data = normalize_positions_of_players(combine_data, 'pos')
    return combine_data


def read_player_statistics_for_years(including_from, excluding_to):
    df = pd.DataFrame()
    for i in range(including_from, excluding_to):
        yearly_stats = pd.read_csv('../unprocessed_college_data/collegefootballstatistics/cfbstats-com-' + str(
            i) + '-1-5-0/player-game-statistics.csv')
        yearly_stats['season_count'] = 1
        df = df.append(yearly_stats)
    return df


def get_position_specific_data(dataset, unit_key):
    return dataset.query("unit_key=='" + unit_key + "'")


def drop_rows_with_sum_lower_than(dataset, columns, threshold=200):
    return dataset.drop(dataset[dataset[columns].sum(axis=1) < threshold].index, inplace=False)


def use_rb_columns_only(dataset):
    rb_columns = base_columns.copy()
    rb_specific_columns = ['Rush Att', 'Rush Yard', 'Rush TD', 'Rec', 'Rec Yards', 'Rec TD', 'Kickoff Ret',
                           'Kickoff Ret Yard',
                           'Kickoff Ret TD', 'Punt Ret Yard', 'Punt Ret TD', 'Fumble', 'Fumble Lost']
    rb_columns.extend(rb_specific_columns)
    dataset = drop_rows_with_sum_lower_than(dataset, rb_specific_columns, 200)
    rb_cols = dataset[rb_columns]
    return rb_cols


def use_wr_columns_only(dataset):
    wr_columns = base_columns.copy()
    wr_specific_columns = ['Rush Att', 'Rush Yard', 'Rush TD', 'Rec', 'Rec Yards', 'Rec TD', 'Kickoff Ret',
                           'Kickoff Ret Yard',
                           'Kickoff Ret TD', 'Punt Ret Yard', 'Punt Ret TD']
    dataset = drop_rows_with_sum_lower_than(dataset, wr_specific_columns, 200)
    wr_columns.extend(wr_specific_columns)
    wr_cols = dataset[wr_columns]
    return wr_cols


def use_dl_columns_only(dataset):
    dl_columns = base_columns.copy()
    dl_specific_columns = ['Fum Ret', 'Fum Ret Yard', 'Fum Ret TD', 'Int Ret', 'Int Ret Yard', 'Int Ret TD', 'Rush Att',
                           'Rush Yard', 'Tackle Solo', 'Tackle Assist', 'Tackle For Loss', 'Tackle For Loss Yard',
                           'Sack', 'Sack Yard', 'QB Hurry', 'Fumble Forced', 'Pass Broken Up']
    dl_columns.extend(dl_specific_columns)
    dataset = drop_rows_with_sum_lower_than(dataset, dl_specific_columns, 10)
    dl_cols = dataset[dl_columns]
    return dl_cols


def use_lb_columns_only(dataset):
    lb_columns = base_columns.copy()
    lb_specific_columns = ['Fum Ret', 'Fum Ret Yard', 'Fum Ret TD', 'Int Ret', 'Int Ret Yard', 'Int Ret TD', 'Rush Att',
                           'Rush Yard', 'Tackle Solo', 'Tackle Assist', 'Tackle For Loss', 'Tackle For Loss Yard',
                           'Sack', 'Sack Yard', 'QB Hurry', 'Fumble Forced', 'Pass Broken Up']
    lb_columns.extend(lb_specific_columns)
    dataset = drop_rows_with_sum_lower_than(dataset, lb_specific_columns, 20)
    lb_cols = dataset[lb_columns]
    return lb_cols


def use_qb_columns_only(dataset):
    qb_columns = base_columns.copy()
    qb_specific_columns = ['Rush Att', 'Rush Yard', 'Rush TD', 'Pass Att', 'Pass Comp', 'Pass Yard', 'Pass TD',
                           'Pass Int', 'Pass Conv', 'Comp Percentage']
    qb_columns.extend(qb_specific_columns)
    dataset = drop_rows_with_sum_lower_than(dataset, qb_specific_columns, 750)
    qb_cols = dataset[qb_columns]
    return qb_cols


def use_db_columns_only(dataset):
    db_columns = base_columns.copy()
    db_specific_columns = ['Fum Ret', 'Fum Ret Yard', 'Fum Ret TD', 'Int Ret', 'Int Ret Yard', 'Int Ret TD', 'Rush Att',
                           'Rush Yard', 'Tackle Solo', 'Tackle Assist', 'Tackle For Loss', 'Tackle For Loss Yard',
                           'Sack', 'Sack Yard', 'QB Hurry', 'Fumble Forced', 'Pass Broken Up']
    db_columns.extend(db_specific_columns)
    dataset = drop_rows_with_sum_lower_than(dataset, db_specific_columns, 20)
    db_cols = dataset[db_columns]
    return db_cols


# No columns yet
def use_ol_columns_only(dataset):
    ol_columns = base_columns.copy()
    # columns.extend([])
    ol_cols = dataset[ol_columns]
    return ol_cols


def use_kicker_columns_only(dataset):
    kicker_columns = base_columns.copy()
    kicker_columns.extend(['Field Goal Att', 'Field Goal Made', 'Punt', 'Punt Yard'])
    kicker_cols = dataset[kicker_columns]
    return kicker_cols


def drop_position_irrelevant_columns(dataset, position=None):
    if position == Units.RB.KEY:
        return use_rb_columns_only(dataset)
    if position == Units.WR.KEY:
        return use_wr_columns_only(dataset)
    if position == Units.DL.KEY:
        return use_dl_columns_only(dataset)
    if position == Units.LB.KEY:
        return use_lb_columns_only(dataset)
    if position == Units.QB.KEY:
        return use_qb_columns_only(dataset)
    if position == Units.DB.KEY:
        return use_db_columns_only(dataset)
    if position == Units.OL:
        return use_ol_columns_only(dataset)
    if position == Units.TE.KEY:
        return use_wr_columns_only(dataset)
    if position == Units.K:
        return use_kicker_columns_only(dataset)
    return None


def get_college_player_aggregation_function():
    return {
        'Player Code': 'first',
        'Rush Att': 'sum',
        'Rush Yard': 'sum',
        'Rush TD': 'sum',
        'Pass Att': 'sum',
        'Pass Comp': 'sum',
        'Pass Yard': 'sum',
        'Pass TD': 'sum',
        'Pass Int': 'sum',
        'Pass Conv': 'sum',
        'Rec': 'sum',
        'Rec Yards': 'sum',
        'Rec TD': 'sum',
        'Kickoff Ret': 'sum',
        'Kickoff Ret Yard': 'sum',
        'Kickoff Ret TD': 'sum',
        'Punt Ret': 'sum',
        'Punt Ret Yard': 'sum',
        'Punt Ret TD': 'sum',
        'Fum Ret': 'sum',
        'Fum Ret Yard': 'sum',
        'Fum Ret TD': 'sum',
        'Int Ret': 'sum',
        'Int Ret Yard': 'sum',
        'Int Ret TD': 'sum',
        'Misc Ret': 'sum',
        'Misc Ret Yard': 'sum',
        'Misc Ret TD': 'sum',
        'Field Goal Att': 'sum',
        'Field Goal Made': 'sum',
        'Off XP Kick Att': 'sum',
        'Off XP Kick Made': 'sum',
        'Off 2XP Att': 'sum',
        'Off 2XP Made': 'sum',
        'Def 2XP Att': 'sum',
        'Def 2XP Made': 'sum',
        'Safety': 'sum',
        'Points': 'sum',
        'Punt': 'sum',
        'Punt Yard': 'sum',
        'Kickoff': 'sum',
        'Kickoff Yard': 'sum',
        'Kickoff Touchback': 'sum',
        'Kickoff Out-Of-Bounds': 'sum',
        'Kickoff Onside': 'sum',
        'Fumble': 'sum',
        'Fumble Lost': 'sum',
        'Tackle Solo': 'sum',
        'Tackle Assist': 'sum',
        'Tackle For Loss': 'sum',
        'Tackle For Loss Yard': 'sum',
        'Sack': 'sum',
        'Sack Yard': 'sum',
        'QB Hurry': 'sum',
        'Fumble Forced': 'sum',
        'Pass Broken Up': 'sum',
        'Kick/Punt Blocked': 'sum',
        'Team Code': 'last',
        'Last Name': 'first',
        'First Name': 'first',
        'Uniform Number': 'last',
        'Class': 'last',
        'Position': 'last',
        'Height': 'last',
        'Weight': 'last',
        'Home Town': 'last',
        'Home State': 'last',
        'Home Country': 'last',
        'Last School': 'last',
        'season': 'last',
        'draft_season': 'last',
        'season_counter': 'last',
        'name': 'last',
        'unit_key': 'last'
    }
