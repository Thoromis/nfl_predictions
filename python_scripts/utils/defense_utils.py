from python_scripts.football_utility_functions import base_columns


def use_defense_columns_only(dataset):
    print("WR function called")
    def_columns = base_columns.copy()
    def_columns.extend(
        ['Fum Ret', 'Fum Ret Yard', 'Fum Ret TD', 'Int Ret', 'Int Ret Yard', 'Int Ret TD', 'Tackle Solo',
         'Tackle Assist', 'Tackle for Loss', 'Sack', 'QB Hurry', 'Fumble Forced', 'Pass Broken Up'])
    cols = dataset[def_columns]
    return cols


def merge_duplicate_defense_rows(dataset):
    aggregation_functions = {
        # Standard columns first (TODO: move to football_utility_functions)
        'Team Code': 'first',
        'name': 'first',
        'unit_key': 'first',
        # 'season_x': 'first',
        'draft_season': 'first',
        # 'round': 'first',
        # 'pick': 'first',
        # 'age': 'first',
        # Position specific columns
        'Fum Ret': 'sum',
        'Fum Ret Yard': 'sum',
        'Fum Ret TD': 'sum',
        'Int Ret': 'sum',
        'Int Ret Yard': 'sum',
        'Int Ret TD': 'sum',
        'Tackle Solo': 'sum',
        'Tackle Assist': 'sum',
        'Tackle For Loss': 'sum',
        'Sack': 'sum',
        'QB Hurry': 'sum',
        'Fumble Forced': 'sum',
        'Pass Broken Up': 'sum',
    }
    merged_dataset = dataset.groupby(dataset['Player Code']).aggregate(aggregation_functions)
    return merged_dataset
