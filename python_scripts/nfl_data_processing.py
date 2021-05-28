import pandas as pd
import football_utility_functions as nfl
import classifier as classifier


def process_nfl_data():
    combined_roster = nfl.read_nfl_rosters_in_year_range(2009, 2019)
    receivering_stats = nfl.read_receiver_stats_for_players(combined_roster)

    # Combined receiver stats with names, now classify as either BUST or GOOD
    classifiers = classifier.standard_classifiers_wr()

    classifier.classify_dataframe(receivering_stats, classifiers)
    # classifier.classify_by_single_classifier(receivering_stats, classifiers)
    # obsolete
    # receivering_stats['Classification'] = receivering_stats.apply(axis=1, func=lambda x: nfl.classify_receiver(x))

    nfl.write_nfl_players_to_csv_no_stats(receivering_stats, 'wr_nfl_data.csv')