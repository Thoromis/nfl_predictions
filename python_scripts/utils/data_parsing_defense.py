# region constants and imports
import pandas as pd

defense_columns = ['player_id', 'player_name', 'interceptions', 'tackles_for_loss', 'solo_tackles', 'tackles_assist',
                   'forced_fumbles', 'sacks', 'qb_hits']


# endregion

# region increase functions
def increase_column_by_x(row, player_id, column_name, by=1):
    if row['player_id'] != player_id:
        return
    row[column_name] += by


# endregion

# region handle column functions
def handle_interceptions(play, player_statistics):
    player_id = play['interception_player_id']
    player_name = play['interception_player_name']

    if pd.isna(player_id) or pd.isna(player_name):
        return player_statistics

    player_statistics = add_new_player(player_statistics, player_id, player_name)
    player_statistics.apply(lambda x: increase_column_by_x(x, player_id, 'interceptions'), axis=1)
    return player_statistics


def handle_tackles_for_loss(play, player_statistics):
    player1_id = play['tackle_for_loss_1_player_id']
    player1_name = play['tackle_for_loss_1_player_name']

    player2_id = play['tackle_for_loss_2_player_id']
    player2_name = play['tackle_for_loss_2_player_name']

    if not pd.isna(player1_id) and not pd.isna(player1_name):
        player_statistics = add_new_player(player_statistics, player1_id, player1_name)
        player_statistics.apply(lambda x: increase_column_by_x(x, player1_id, 'tackles_for_loss'), axis=1)

    if not pd.isna(player2_id) and not pd.isna(player2_name):
        player_statistics = add_new_player(player_statistics, player2_id, player2_name)
        player_statistics.apply(lambda x: increase_column_by_x(x, player1_id, 'tackles_for_loss'), axis=1)

    return player_statistics


def handle_solo_tackles(play, player_statistics):
    player1_id = play['solo_tackle_1_player_id']
    player1_name = play['solo_tackle_1_player_name']

    player2_id = play['solo_tackle_2_player_id']
    player2_name = play['solo_tackle_2_player_name']

    if not pd.isna(player1_id) and not pd.isna(player1_name):
        player_statistics = add_new_player(player_statistics, player1_id, player1_name)
        player_statistics.apply(lambda x: increase_column_by_x(x, player1_id, 'solo_tackles'), axis=1)

    if not pd.isna(player2_id) and not pd.isna(player2_name):
        player_statistics = add_new_player(player_statistics, player2_id, player2_name)
        player_statistics.apply(lambda x: increase_column_by_x(x, player1_id, 'solo_tackles'), axis=1)

    return player_statistics


def handle_assisted_tackles(play, player_statistics):
    for i in range(1, 5):
        player_id = play['assist_tackle_' + str(i) + '_player_id']
        player_name = play['assist_tackle_' + str(i) + '_player_name']

        if not pd.isna(player_id) and not pd.isna(player_name):
            player_statistics = add_new_player(player_statistics, player_id, player_name)
            player_statistics.apply(lambda x: increase_column_by_x(x, player_id, 'tackles_assist'), axis=1)

    return player_statistics


def handle_forced_fumbles(play, player_statistics):
    for i in range(1, 3):
        player_id = play['forced_fumble_player_' + str(i) + '_player_id']
        player_name = play['forced_fumble_player_' + str(i) + '_player_name']

        if not pd.isna(player_id) and not pd.isna(player_name):
            player_statistics = add_new_player(player_statistics, player_id, player_name)
            player_statistics.apply(lambda x: increase_column_by_x(x, player_id, 'forced_fumbles'), axis=1)

    return player_statistics


def handle_qb_hits(play, player_statistics):
    for i in range(1, 3):
        player_id = play['qb_hit_' + str(i) + '_player_id']
        player_name = play['qb_hit_' + str(i) + '_player_name']

        if not pd.isna(player_id) and not pd.isna(player_name):
            player_statistics = add_new_player(player_statistics, player_id, player_name)
            player_statistics.apply(lambda x: increase_column_by_x(x, player_id, 'qb_hits'), axis=1)

    return player_statistics



def handle_sacks(play, player_statistics):
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
        player_statistics = add_new_player(player_statistics, row['player_id'], row['player_name'])
        player_statistics.apply(lambda x: increase_column_by_x(x, row['player_id'], 'sacks', by=sack_amount), axis=1)

    return player_statistics


# endregion


# region other helper functions
def add_new_player(player_statistics, player_id, player_name):
    if len(player_statistics[player_statistics['player_id'] == player_id]) == 0:  # player doesn't have statistics yet
        new_player = pd.DataFrame(data=[[player_id, player_name, 0, 0, 0, 0, 0, 0, 0]],
                                  columns=defense_columns)
        return player_statistics.append(new_player)
    return player_statistics

# endregion
