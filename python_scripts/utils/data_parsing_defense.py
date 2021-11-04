# region constants and imports
import pandas as pd

defense_columns = ['player_id', 'player_name', 'interceptions', 'tackles_for_loss', 'solo_tackles', 'tackles_assist',
                   'forced_fumbles', 'sacks', 'qb_hits', 'incomplete_passes_against', 'fumbles_recovered']
agg_defense_columns = defense_columns[2:]


# endregion

# region increase functions
def increase_column_by_x(row, player_id, column_name, by=1):
    if row['player_id'] != player_id:
        return
    row[column_name] += by


# endregion

# region handle column functions
def handle_interceptions(play, player_statistics, current_row):
    player_id = play['interception_player_id']
    player_name = play['interception_player_name']

    if pd.isna(player_id) or pd.isna(player_name):
        return current_row

    # player_statistics = add_new_player(player_statistics, player_id, player_name)
    # player_statistics.apply(lambda x: increase_column_by_x(x, player_id, 'interceptions'), axis=1)

    current_row = add_new_player(current_row, player_id, player_name)
    current_row.apply(lambda x: increase_column_by_x(x, player_id, 'interceptions'), axis=1)

    return current_row


def handle_tackles_for_loss(play, player_statistics, current_row):
    player1_id = play['tackle_for_loss_1_player_id']
    player1_name = play['tackle_for_loss_1_player_name']

    player2_id = play['tackle_for_loss_2_player_id']
    player2_name = play['tackle_for_loss_2_player_name']

    if not pd.isna(player1_id) and not pd.isna(player1_name):
        # player_statistics = add_new_player(player_statistics, player1_id, player1_name)
        # player_statistics.apply(lambda x: increase_column_by_x(x, player1_id, 'tackles_for_loss'), axis=1)

        current_row = add_new_player(current_row, player1_id, player1_name)
        current_row.apply(lambda x: increase_column_by_x(x, player1_id, 'tackles_for_loss'), axis=1)

    if not pd.isna(player2_id) and not pd.isna(player2_name):
        # player_statistics = add_new_player(player_statistics, player2_id, player2_name)
        # player_statistics.apply(lambda x: increase_column_by_x(x, player1_id, 'tackles_for_loss'), axis=1)

        current_row = add_new_player(current_row, player2_id, player2_name)
        current_row.apply(lambda x: increase_column_by_x(x, player1_id, 'tackles_for_loss'), axis=1)

    return current_row


def handle_solo_tackles(play, player_statistics, current_row):
    player1_id = play['solo_tackle_1_player_id']
    player1_name = play['solo_tackle_1_player_name']

    player2_id = play['solo_tackle_2_player_id']
    player2_name = play['solo_tackle_2_player_name']

    if not pd.isna(player1_id) and not pd.isna(player1_name):
        # player_statistics = add_new_player(player_statistics, player1_id, player1_name)
        # player_statistics.apply(lambda x: increase_column_by_x(x, player1_id, 'solo_tackles'), axis=1)

        current_row = add_new_player(current_row, player1_id, player1_name)
        current_row.apply(lambda x: increase_column_by_x(x, player1_id, 'solo_tackles'), axis=1)

    if not pd.isna(player2_id) and not pd.isna(player2_name):
        # player_statistics = add_new_player(player_statistics, player2_id, player2_name)
        # player_statistics.apply(lambda x: increase_column_by_x(x, player1_id, 'solo_tackles'), axis=1)

        current_row = add_new_player(current_row, player2_id, player2_name)
        current_row.apply(lambda x: increase_column_by_x(x, player1_id, 'solo_tackles'), axis=1)

    return current_row


def handle_assisted_tackles(play, player_statistics, current_row):
    for i in range(1, 5):
        player_id = play['assist_tackle_' + str(i) + '_player_id']
        player_name = play['assist_tackle_' + str(i) + '_player_name']

        if not pd.isna(player_id) and not pd.isna(player_name):
            # player_statistics = add_new_player(player_statistics, player_id, player_name)
            # player_statistics.apply(lambda x: increase_column_by_x(x, player_id, 'tackles_assist'), axis=1)

            current_row = add_new_player(current_row, player_id, player_name)
            current_row.apply(lambda x: increase_column_by_x(x, player_id, 'tackles_assist'), axis=1)

    return current_row


def handle_forced_fumbles(play, player_statistics, current_row):
    for i in range(1, 3):
        player_id = play['forced_fumble_player_' + str(i) + '_player_id']
        player_name = play['forced_fumble_player_' + str(i) + '_player_name']

        if not pd.isna(player_id) and not pd.isna(player_name):
            # player_statistics = add_new_player(player_statistics, player_id, player_name)
            # player_statistics.apply(lambda x: increase_column_by_x(x, player_id, 'forced_fumbles'), axis=1)

            current_row = add_new_player(current_row, player_id, player_name)
            current_row.apply(lambda x: increase_column_by_x(x, player_id, 'forced_fumbles'), axis=1)

    return current_row


def handle_qb_hits(play, player_statistics, current_row):
    for i in range(1, 3):
        player_id = play['qb_hit_' + str(i) + '_player_id']
        player_name = play['qb_hit_' + str(i) + '_player_name']

        if not pd.isna(player_id) and not pd.isna(player_name):
            # player_statistics = add_new_player(player_statistics, player_id, player_name)
            # player_statistics.apply(lambda x: increase_column_by_x(x, player_id, 'qb_hits'), axis=1)

            current_row = add_new_player(current_row, player_id, player_name)
            current_row.apply(lambda x: increase_column_by_x(x, player_id, 'qb_hits'), axis=1)

    return current_row


def handle_sacks(play, player_statistics, current_row):
    sack_helper_columns = ['player_name', 'player_id', 'full_sack']
    sack_players = pd.DataFrame(columns=sack_helper_columns)

    # Check TFL
    for i in range(1, 3):
        player_id = play['tackle_for_loss_' + str(i) + '_player_id']
        player_name = play['tackle_for_loss_' + str(i) + '_player_name']

        if not pd.isna(player_id) and not pd.isna(player_name):
            sack_players = sack_players.append({'player_id': player_id, 'player_name': player_name, 'full_sack': 1},
                                               ignore_index=True)

    # Check Solo tackles
    for i in range(1, 3):
        player_id = play['solo_tackle_' + str(i) + '_player_id']
        player_name = play['solo_tackle_' + str(i) + '_player_name']

        if len(sack_players.loc[sack_players['player_id'] == player_id]) > 0:
            continue  # If the player is already accounted a full sack he won't get another

        if not pd.isna(player_id) and not pd.isna(player_name):
            sack_players = sack_players.append({'player_id': player_id, 'player_name': player_name, 'full_sack': 1},
                                               ignore_index=True)

    # Check Tackle assists
    for i in range(1, 5):
        player_id = play['assist_tackle_' + str(i) + '_player_id']
        player_name = play['assist_tackle_' + str(i) + '_player_name']

        if len(sack_players.loc[sack_players['player_id'] == player_id]) > 0:
            continue  # If the player is already accounted a full sack he won't get a half one instead

        if not pd.isna(player_id) and not pd.isna(player_name):
            sack_players = sack_players.append({'player_id': player_id, 'player_name': player_name, 'full_sack': 0},
                                               ignore_index=True)

    for index, row in sack_players.iterrows():
        sack_amount = 1
        if row['full_sack'] == 0:
            sack_amount = 0.5
        # player_statistics = add_new_player(player_statistics, row['player_id'], row['player_name'])
        # player_statistics.apply(lambda x: increase_column_by_x(x, row['player_id'], 'sacks', by=sack_amount), axis=1)

        current_row = add_new_player(current_row, row['player_id'], row['player_name'])
        current_row.apply(lambda x: increase_column_by_x(x, row['player_id'], 'sacks', by=sack_amount), axis=1)

    return current_row


def handle_incomplete_passes(play, player_statistics, current_row):
    for i in range(1, 3):
        player_id = play['pass_defense_' + str(i) + '_player_id']
        player_name = play['pass_defense_' + str(i) + '_player_name']

        if not pd.isna(player_id) and not pd.isna(player_name):
            current_row = add_new_player(current_row, player_id, player_name)
            current_row.apply(lambda x: increase_column_by_x(x, player_id, 'incomplete_passes_against'), axis=1)
    return current_row


def handle_fumble_recoveries(play, current_row):
    for i in range(1, 3):
        player_id = play['fumble_recovery_' + str(i) + '_player_id']
        player_name = play['fumble_recovery_' + str(i) + '_player_name']

        if not pd.isna(player_id) and not pd.isna(player_name):
            current_row = add_new_player(current_row, player_id, player_name)
            current_row.apply(lambda x: increase_column_by_x(x, player_id, 'fumbles_recovered'), axis=1)

    return current_row

# TODO

# endregion


# region other helper functions
def add_new_player(player_statistics, player_id, player_name):
    if len(player_statistics[player_statistics['player_id'] == player_id]) == 0:  # player doesn't have statistics yet
        new_player = pd.DataFrame(data=[[player_id, player_name, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                                  columns=defense_columns)
        return player_statistics.append(new_player)
    return player_statistics


def add_row_to_stats(player_statistics, new_row):
    if len(player_statistics[
               player_statistics['player_id'] == new_row['player_id']]) == 0:  # player doesn't have statistics yet
        player_statistics = player_statistics.append(new_row)
    else:
        current_row = player_statistics[player_statistics['player_id'] == new_row['player_id']]
        new_df = pd.DataFrame(data=current_row, columns=defense_columns)
        new_df = new_df.append(new_row)
        new_df = new_df.groupby(['player_id', 'player_name'], as_index=False).sum()
        player_statistics.loc[player_statistics['player_id'] == new_df['player_id'][0], defense_columns] = new_df[
            defense_columns]

    return player_statistics


def reset_to_one(x):
    if isinstance(x, str):
        return x
    elif x > 1:
        return 1
    else:
        return x


# Reset every cell > 1 to 1, as e.g. a player can't make 2 tackles in the same play
def sanitize_stat_row(row):
    row = row.apply(lambda x: reset_to_one(x))
    return row
# endregion
