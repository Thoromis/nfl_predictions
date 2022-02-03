import pandas as pd
from python_scripts.football_utility_functions import base_columns


def use_qb_columns_only(dataset):
    qb_columns = base_columns.copy()
    qb_columns.extend(
        ['Rush Att', 'Rush Yard', 'Rush TD', 'Pass Att', 'Pass Comp', 'Pass Yard', 'Pass TD', 'Pass Int'])
    cols = dataset[qb_columns]
    return cols


# Takes dataset with WRs, that was previously formatted using [use_wr_columns_only] function
def merge_duplicate_qb_rows(dataset):
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
        'Pass Att': 'sum',
        'Pass Comp': 'sum',
        'Pass Yard': 'sum',
        'Pass TD': 'sum',
        'Pass Int': 'sum',
    }
    merged_dataset = dataset.groupby(dataset['Player Code']).aggregate(aggregation_functions)
    return merged_dataset
