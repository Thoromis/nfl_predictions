import pandas as pd
from python_scripts.football_utility_functions import base_columns


def use_offense_columns_only(dataset):
    print("WR function called")
    wr_columns = base_columns.copy()
    wr_columns.extend(
        ['Rush Att', 'Rush Yard', 'Rush TD', 'Rec', 'Rec Yards', 'Rec TD', 'Kickoff Ret', 'Kickoff Ret Yard',
         'Kickoff Ret TD', 'Punt Ret Yard', 'Punt Ret TD'])
    wr_cols = dataset[wr_columns]
    return wr_cols


# Takes dataset with WRs, that was previously formatted using [use_wr_columns_only] function
def merge_duplicate_offense_rows(dataset):
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
        'Rush Att': 'sum',
        'Rush Yard': 'sum',
        'Rush TD': 'sum',
        'Rec': 'sum',
        'Rec Yards': 'sum',
        'Rec TD': 'sum',
        'Kickoff Ret': 'sum',
        'Kickoff Ret Yard': 'sum',
        'Kickoff Ret TD': 'sum',
        'Punt Ret Yard': 'sum',
        'Punt Ret TD': 'sum',
    }
    merged_dataset = dataset.groupby(dataset['Player Code']).aggregate(aggregation_functions)
    return merged_dataset
