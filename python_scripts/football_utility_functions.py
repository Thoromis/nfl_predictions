import pandas as pd

base_columns = ['Player Code', 'Team Code', 'name', 'unit_key', 'season_x', 'draft_season', 'round', 'pick', 'age']


def align_positions(position):
    if position == 'T' or position == 'G' or position == 'C' \
            or position == 'OL' or position == 'OT' or position == 'OG':
        return 'OL'
    elif position == 'DB' or position == 'CB' or position == 'FS' or position == 'S' or position == 'SS':
        return 'DB'
    elif position == 'DL' or position == 'NT' or position == 'DE' or position == 'DT':
        return 'DL'
    elif position == 'LB' or position == 'OLB' or position == 'MLB' or position == 'ILB':
        return 'LB'
    elif position == 'RB' or position == 'FB' or position == 'TB':
        return 'RB'
    elif position == 'WR' or position == 'SE':
        return 'WR'
    elif position == 'K' or position == 'P':
        return 'K'
    else:
        return position


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


def write_nfl_players_to_csv(data, filename):
    data.to_csv('../processed_data/' + filename)


def write_nfl_players_to_csv_no_stats(data, filename):
    csv_data = data[['full_player_name', 'position', 'gsis_id', 'Classification_All']]
    csv_data.to_csv('../processed_data/' + filename)


def classify_receiver(row):
    if row['Total_Yards'] > 5000:
        return 'Good'
    return 'Bust'


def read_receiver_stats_for_players(players_df):
    receiving_stats = pd.read_csv("../unprocessed_nfl_data/statistics/season_receiving_df.csv")
    # receiving_stats.drop(axis=1, labels=['Season', 'Player_Name', 'Targets_per_Drive', 'Rec_per_Drive', 'Yards_per_Drive', 'Yards_per_Rec', 'Yards_per_Target', 'YAC_per_Target', 'Caught_YAC_per_Target', 'Dropped_YAC_per_Target', 'YAC_per_Rec', 'Caught_YAC_per_Rec', 'Dropped_YAC_per_Rec', 'YAC_per_Drive'])
    receiving_stats = receiving_stats[
        ['Receiver_ID', 'Targets', 'Receptions', 'Drives', 'Total_Yards', 'Total_Raw_YAC', 'Total_Caught_YAC',
         'Fumbles', 'TDs', 'AC_TDs', 'Total_Caught_AirYards']]
    receiving_stats['season_helper'] = 1
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
        df = df.append(yearly_stats)
    return df


def get_position_specific_data(dataset, unit_key):
    return dataset.query("unit_key=='" + unit_key + "'")


def use_rb_columns_only(dataset):
    print("RB function called")
    rb_columns = base_columns.copy()
    rb_columns.extend(
        ['Rush Att', 'Rush Yard', 'Rush TD', 'Rec', 'Rec Yards', 'Rec TD', 'Kickoff Ret', 'Kickoff Ret Yard',
         'Kickoff Ret TD', 'Punt Ret Yard', 'Punt Ret TD', 'Fumble', 'Fumble Lost'])
    rb_cols = dataset[rb_columns]
    return rb_cols


def use_wr_columns_only(dataset):
    print("WR function called")
    wr_columns = base_columns.copy()
    wr_columns.extend(
        ['Rush Att', 'Rush Yard', 'Rush TD', 'Rec', 'Rec Yards', 'Rec TD', 'Kickoff Ret', 'Kickoff Ret Yard',
         'Kickoff Ret TD', 'Punt Ret Yard', 'Punt Ret TD'])
    wr_cols = dataset[wr_columns]
    return wr_cols


def use_dl_columns_only(dataset):
    print("DL function called")
    dl_columns = base_columns.copy()
    dl_columns.extend(
        ['Rush Att', 'Rush Yard', 'Tackle Solo', 'Tackle Assist', 'Tackle For Loss', 'Tackle For Loss Yard',
         'Sack', 'Sack Yard', 'QB Hurry', 'Fumble Forced', 'Pass Broken Up'])
    dl_cols = dataset[dl_columns]
    return dl_cols


def use_lb_columns_only(dataset):
    print("LB function called")
    lb_columns = base_columns.copy()
    lb_columns.extend(
        ['Rush Att', 'Rush Yard', 'Tackle Solo', 'Tackle Assist', 'Tackle For Loss', 'Tackle For Loss Yard',
         'Sack', 'Sack Yard', 'QB Hurry', 'Fumble Forced', 'Pass Broken Up'])
    lb_cols = dataset[lb_columns]
    return lb_cols


def use_qb_columns_only(dataset):
    print("QB function called")
    qb_columns = base_columns.copy()
    qb_columns.extend(
        ['Rush Att', 'Rush Yard', 'Pass Att', 'Pass Comp', 'Pass Yard', 'Pass TD', 'Pass Int', 'Pass Conv'])
    qb_cols = dataset[qb_columns]
    return qb_cols


def use_db_columns_only(dataset):
    print("DB function called")
    db_columns = base_columns.copy()
    db_columns.extend(
        ['Rush Att', 'Rush Yard', 'Tackle Solo', 'Tackle Assist', 'Tackle For Loss', 'Tackle For Loss Yard',
         'Sack', 'Sack Yard', 'QB Hurry', 'Fumble Forced', 'Pass Broken Up'])
    db_cols = dataset[db_columns]
    return db_cols


# No columns yet
def use_ol_columns_only(dataset):
    print("OL function called")
    ol_columns = base_columns.copy()
    # columns.extend([])
    ol_cols = dataset[ol_columns]
    return ol_cols


def use_kicker_columns_only(dataset):
    print("Kicker function called")
    kicker_columns = base_columns.copy()
    kicker_columns.extend(['Field Goal Att', 'Field Goal Made', 'Punt', 'Punt Yard'])
    kicker_cols = dataset[kicker_columns]
    return kicker_cols


def drop_position_irrelevant_columns(dataset, position=None):
    if position == 'RB':
        return use_rb_columns_only(dataset)
    if position == 'WR':
        return use_wr_columns_only(dataset)
    if position == 'DL':
        return use_dl_columns_only(dataset)
    if position == 'LB':
        return use_lb_columns_only(dataset)
    if position == 'QB':
        return use_qb_columns_only(dataset)
    if position == 'DB':
        return use_db_columns_only(dataset)
    if position == 'OL':
        return use_ol_columns_only(dataset)
    if position == 'TE':
        return use_wr_columns_only(dataset)
    if position == 'K':
        return use_kicker_columns_only(dataset)
    return None
    # switcher = {
    #     'RB': use_rb_columns_only(dataset),
    #     'WR': use_wr_columns_only(dataset),
    #     'DL': use_dl_columns_only(dataset),
    #     'LB': use_lb_columns_only(dataset),
    #     'QB': use_qb_columns_only(dataset),
    #     'DB': use_db_columns_only(dataset),
    #     'OL': use_ol_columns_only(dataset),
    #     'TE': use_wr_columns_only(dataset),
    #     'K': use_kicker_columns_only(dataset),
    #     None: dataset,
    # }
    # return switcher.get(position, lambda: "invalid position")
