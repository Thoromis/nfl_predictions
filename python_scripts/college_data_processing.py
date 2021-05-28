import pandas as pd
import football_utility_functions as nfl


def process_college_data():
    draft_data_sharpe = nfl.read_and_normalize_draft_file(
        "../unprocessed_college_data/draft_picks/leesharpe/draft_picks.csv", 'position')
    draft_data_taylor = nfl.read_and_normalize_draft_file(
        "../unprocessed_college_data/draft_picks/seanjtaylor/drafts.csv", 'pos')

    # %%

    combine_data_taylor = nfl.read_and_normalize_combine_data(
        '../unprocessed_college_data/draft_picks/seanjtaylor/combines.csv')

    # %% Read in player data in a loop

    player_data = pd.DataFrame()

    for i in range(2005, 2014):
        data_for_year = nfl.read_and_normalize_player_data_for_year(i, 'Position')
        player_data = player_data.append(data_for_year)

    # %% Merge player data with draft picks and rounds

    sharpe_merged_player_data = player_data.merge(draft_data_sharpe, left_on=['name', 'draft_season', 'unit_key'],
                                                  right_on=['full_name', 'season', 'unit_key'])

    # left join so we keep also players that weren't drafted
    taylor_merged_player_data = player_data.merge(draft_data_taylor, how='left',
                                                  left_on=['name', 'draft_season', 'unit_key'],
                                                  right_on=['player', 'season', 'unit_key'])
    taylor_merged_player_data = taylor_merged_player_data.merge(combine_data_taylor, how='left',
                                                                left_on=['draft_season', 'player', 'unit_key'],
                                                                right_on=['season', 'player', 'unit_key'])

    # %% Pick columns we need from the merged sets (Using TAYLOR's data)

    taylor_merged_player_data = taylor_merged_player_data[
        ['Player Code', 'Team Code', 'name', 'unit_key', 'season_x', 'draft_season', 'round', 'pick', 'team', 'age',
         'to']]

    max_season = taylor_merged_player_data['season_x'].max()
    min_season = taylor_merged_player_data['season_x'].min()
    player_statistics = nfl.read_player_statistics_for_years(min_season, 2007)
    player_statistics = player_statistics.drop(columns=['Game Code'])

    # %% get aggregated stats to find out stats for different player positions

    aggregated_stats = player_statistics.groupby('Player Code', as_index=False).sum()
    aggregated_stats = taylor_merged_player_data.merge(aggregated_stats, how='left', on='Player Code')

    # %%

    dl_data = nfl.get_position_specific_data(aggregated_stats, 'DL')
    wr_data = nfl.get_position_specific_data(aggregated_stats, 'WR')
    rb_data = nfl.get_position_specific_data(aggregated_stats, 'RB')
    lb_data = nfl.get_position_specific_data(aggregated_stats, 'LB')
    qb_data = nfl.get_position_specific_data(aggregated_stats, 'QB')
    db_data = nfl.get_position_specific_data(aggregated_stats, 'DB')
    ol_data = nfl.get_position_specific_data(aggregated_stats, 'OL')
    te_data = nfl.get_position_specific_data(aggregated_stats, 'TE')
    ki_data = nfl.get_position_specific_data(aggregated_stats, 'K')

    dl_data = nfl.drop_position_irrelevant_columns(dl_data, 'DL')
    wr_data = nfl.drop_position_irrelevant_columns(wr_data, 'WR')
    rb_data = nfl.drop_position_irrelevant_columns(rb_data, 'RB')
    lb_data = nfl.drop_position_irrelevant_columns(lb_data, 'LB')
    qb_data = nfl.drop_position_irrelevant_columns(qb_data, 'QB')
    db_data = nfl.drop_position_irrelevant_columns(db_data, 'DB')
    ol_data = nfl.drop_position_irrelevant_columns(ol_data, 'OL')
    te_data = nfl.drop_position_irrelevant_columns(te_data, 'TE')
    ki_data = nfl.drop_position_irrelevant_columns(ki_data, 'K')

    # TODO: Add team statistics for OLiner to have some stats

    # %% Create map with positional key and the data for it then

    positional_data = {
        'DL': dl_data,
        'WR': wr_data,
        'RB': rb_data,
        'LB': lb_data,
        'QB': qb_data,
        'DB': db_data,
        'OL': ol_data,
        'TE': te_data,
        'KI': ki_data,
    }

    wr_data.to_csv(path_or_buf='../processed_data/wr_college_data.csv')
