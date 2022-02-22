import pandas as pd
import football_utility_functions as nfl
import utils.offense_utils as offense_utils
import utils.defense_utils as defense_utils
import utils.qb_utils as qb_utils
import utils.unit_keys as Units


def save_position_specific_statistics(aggregated_stats):
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

    # %% Create map with positional key and the data for it then
    # The mapping of aggregation functions would need to be further up (instead of aggregated_stats aggr.) to be of use
    # If needed: remove aggregated_stats aggregation, and only split into positional groups - then use this mapping
    # If thats the case then also add mean instead of sum everywhere
    wr_data = offense_utils.merge_duplicate_offense_rows(wr_data)
    te_data = offense_utils.merge_duplicate_offense_rows(te_data)
    rb_data = offense_utils.merge_duplicate_offense_rows(rb_data)

    qb_data = qb_utils.merge_duplicate_qb_rows(qb_data)
    qb_data.dropna(inplace=True, subset=['Comp Percentage'])

    dl_data = defense_utils.merge_duplicate_defense_rows(dl_data)
    db_data = defense_utils.merge_duplicate_defense_rows(db_data)
    lb_data = defense_utils.merge_duplicate_defense_rows(lb_data)

    wr_data.to_csv(path_or_buf='../processed_data/' + Units.WR.KEY + '/' + Units.WR.KEY + '_college_data.csv')
    rb_data.to_csv(path_or_buf='../processed_data/' + Units.RB.KEY + '/' + Units.RB.KEY + '_college_data.csv')
    te_data.to_csv(path_or_buf='../processed_data/' + Units.TE.KEY + '/' + Units.TE.KEY + '_college_data.csv')

    qb_data.to_csv(path_or_buf='../processed_data/' + Units.QB.KEY + '/' + Units.QB.KEY + '_college_data.csv')

    lb_data.to_csv(path_or_buf='../processed_data/' + Units.LB.KEY + '/' + Units.LB.KEY + '_college_data.csv')
    db_data.to_csv(path_or_buf='../processed_data/' + Units.DB.KEY + '/' + Units.DB.KEY + '_college_data.csv')
    dl_data.to_csv(path_or_buf='../processed_data/' + Units.DL.KEY + '/' + Units.DL.KEY + '_college_data.csv')


def process_college_data():
    # Read in player names
    player_data = pd.DataFrame()

    for i in range(2005, 2014):
        data_for_year = nfl.read_and_normalize_player_data_for_year(i, 'Position')
        player_data = player_data.append(data_for_year)

    player_data = player_data.drop_duplicates(subset=['Player Code'])

    # Read in Statistics
    player_statistics = nfl.read_player_statistics_for_years(2005, 2014)
    player_statistics = player_statistics.drop(columns=['Game Code'])

    # TODO Try aggregation functions method here as well, (e.g. to keep throwing accuracy)
    # Combine statistics and names
    aggregated_stats = player_statistics.groupby('Player Code', as_index=False).sum()
    aggregated_stats = aggregated_stats.merge(player_data, how='left', on='Player Code')

    aggregated_stats = nfl.merge_transferred_players(aggregated_stats)
    aggregated_stats = aggregated_stats.groupby('pk_id', as_index=False).agg(
        nfl.get_college_player_aggregation_function())

    aggregated_stats['Comp Percentage'] = aggregated_stats['Pass Comp'] / aggregated_stats['Pass Att']

    save_position_specific_statistics(aggregated_stats)


def legacy_process_college_data():
    draft_data_taylor = nfl.read_and_normalize_draft_file(
        "../unprocessed_college_data/draft_picks/seanjtaylor/drafts.csv", 'pos')

    player_data = pd.DataFrame()

    for i in range(2005, 2014):
        data_for_year = nfl.read_and_normalize_player_data_for_year(i, 'Position')
        player_data = player_data.append(data_for_year)

    # left join so we keep also players that weren't drafted
    taylor_merged_player_data = player_data.merge(draft_data_taylor, how='left',
                                                  left_on=['name', 'draft_season', 'unit_key'],
                                                  right_on=['player', 'season', 'unit_key'])

    # %% Pick columns we need from the merged sets (Using TAYLOR's data)

    taylor_merged_player_data = taylor_merged_player_data[
        ['Player Code', 'Team Code', 'name', 'unit_key', 'season_x', 'draft_season', 'round', 'pick', 'team', 'age',
         'to']]
    taylor_merged_player_data = taylor_merged_player_data.dropna()

    max_season = taylor_merged_player_data['season_x'].max()
    min_season = taylor_merged_player_data['season_x'].min()
    player_statistics = nfl.read_player_statistics_for_years(min_season, max_season + 1)
    player_statistics = player_statistics.drop(columns=['Game Code'])

    # %% get aggregated stats to find out stats for different player positions

    # TODO Try aggregation functions method here as well, (e.g. to keep throwing accuracy)
    aggregated_stats = player_statistics.groupby('Player Code', as_index=False).sum()
    aggregated_stats = aggregated_stats.merge(taylor_merged_player_data, how='left', on='Player Code')

    # %%
    save_position_specific_statistics(aggregated_stats)
