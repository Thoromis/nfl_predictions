from enum import Enum

import pandas as pd

import utils.unit_keys as Units


# Classify players by all the given classifiers combined
def classify_dataframe(data, classifiers, unit=Units.WR):
    data['Classification_All'] = data.apply(axis=1, func=lambda x: classify_row(x, classifiers, unit))
    data['Classification_All_num'] = data.apply(axis=1, func=lambda x: classify_row(x, classifiers, unit, True))


def classify_by_single_classifier(data, classifiers, unit=Units.WR):
    for classifier in classifiers:
        data[classifier.__str__()] = data.apply(axis=1, func=lambda x: classify_row(x, [classifier], unit))


def classify_row(row, classifiers, unit, classify_numeric=False):
    if len(classifiers) == 0:
        return 1 if classify_numeric else 'Good'

    classification_threshold = unit.CLASSIFICATION_THRESHOLD

    result = 0
    for classifier in classifiers:
        if classifier == Classifier.BY_YEARS_IN_NFL:  # isinstance(Classifier.BY_YEARS_IN_NFL, classifier):
            result += classify_by_time(row, unit.MAX_SEASON_THRESHOLD)
        elif classifier == Classifier.BY_TOTAL_YARDS:  # isinstance(Classifier.BY_TOTAL_YARDS, classifier):
            result += classify_by_total_yards(row, unit.MAX_YARD_THRESHOLD)
        elif classifier == Classifier.BY_TDs:  # isinstance(Classifier.BY_YARDS_PER_GAME, classifier):
            result += classify_by_touchdowns(row, unit.MAX_TD_THRESHOLD)
        elif classifier == Classifier.BY_RECEPTIONS:
            result += classify_by_receptions(row, unit.MAX_REC_THRESHOLD)
        elif classifier == Classifier.BY_INTERCEPTIONS:
            result += classify_by_interceptions(row, unit.MAX_INT_THRESHOLD)
        elif classifier == Classifier.BY_COMPLETIONS:
            result += classify_by_completions(row, unit.MAX_COMP_THRESHOLD)
        elif classifier == Classifier.BY_SOLO_TACKLES:
            result += classify_by_solo_tackles(row, unit.MAX_SOLO_TACKLE_THRESHOLD)
        elif classifier == Classifier.BY_ASSISTED_TACKLES:
            result += classify_by_assisted_tackles(row, unit.MAX_ASS_TACKLES_THRESHOLD)
        elif classifier == Classifier.BY_TOTAL_TACKLES:
            result += classify_by_total_tackles(row, unit.MAX_TOT_TACKLES_THRESHOLD)
        elif classifier == Classifier.BY_TFL:
            result += classify_by_tfls(row, unit.MAX_TFL_THRESHOLD)
        elif classifier == Classifier.BY_SACKS:
            result += classify_by_sacks(row, unit.MAX_SACK_THRESHOLD)
        elif classifier == Classifier.BY_FORCED_FUMBLES:
            result += classify_by_forced_fumbles(row, unit.MAX_FORCED_FUMBLES_THRESHOLD)
        elif classifier == Classifier.BY_QB_HITS:
            result += classify_by_qb_hits(row, unit.MAX_QB_HITS_THRESHOLD)
        elif classifier == Classifier.BY_PASS_DEF:
            result += classify_by_def_pass_incompletions(row, unit.MAX_INCOMPLETE_PASSES_THRESHOLD)
        elif classifier == Classifier.BY_INTERCEPTIONS_CAUGHT:
            result += classify_by_caught_interceptions(row, unit.MAX_CAUGHT_INTS_THRESHOLD)
        if pd.isna(result):
            print("Result is NA for " + row['full_player_name'])
            print(str(row))

    if result / len(classifiers) >= classification_threshold:
        return 'Good' if not classify_numeric else (result / len(classifiers))
    else:
        return 'Bust' if not classify_numeric else (result / len(classifiers))


def classify_by_interceptions(row, max_threshold=Units.QB.MAX_INT_THRESHOLD):
    value = min(row['Interceptions'], max_threshold)
    return 1 - (1 / max_threshold * value)


# max threshold


def classify_by_completions(row, max_threshold=Units.QB.MAX_COMP_THRESHOLD):
    value = min(row['Completions'], max_threshold)
    return 1 / max_threshold * value


# let's go with 5 TDs being average for a WR, so 10 for maximum, times 2.8
def classify_by_touchdowns(row, max_threshold=Units.WR.MAX_TD_THRESHOLD):
    value = min(row['TDs'], max_threshold)
    return 1 / max_threshold * value


def classify_by_receptions(row, max_threshold=Units.WR.MAX_REC_THRESHOLD):
    value = min(row['Receptions'], max_threshold)
    return 1 / max_threshold * value


# Classify by time spent in the NFL, maximum achievable time is set to 10 [years].
# Becomes less relative to this 10 year threshold, 10 years ==> 1, 1 year ==> 0.1
def classify_by_time(row, max_threshold=Units.WR.MAX_SEASON_THRESHOLD):
    value = min(row['season_helper'], max_threshold)
    return 1 / max_threshold * value


# around 1000 yards is the threshold for being good in a season, 2.8 * 1000 * 2 for max
def classify_by_total_yards(row, max_threshold=Units.WR.MAX_YARD_THRESHOLD):
    value = min(row['Total_Yards'], max_threshold)
    return 1 / max_threshold * value


def classify_by_caught_interceptions(row, max_treshold=Units.DB.MAX_CAUGHT_INTS_THRESHOLD):
    value = min(row['interceptions'], max_treshold)
    return 1 / max_treshold * value


def classify_by_def_pass_incompletions(row, max_treshold=Units.DB.MAX_INCOMPLETE_PASSES_THRESHOLD):
    value = min(row['incomplete_passes_against'], max_treshold)
    return 1 / max_treshold * value


def classify_by_sacks(row, max_threshold=Units.DL.MAX_SACK_THRESHOLD):
    value = min(row['sacks'], max_threshold)
    return 1 / max_threshold * value


def classify_by_qb_hits(row, max_threshold=Units.DL.MAX_QB_HITS_THRESHOLD):
    value = min(row['qb_hits'], max_threshold)
    return 1 / max_threshold * value


def classify_by_forced_fumbles(row, max_threshold=Units.DL.MAX_FORCED_FUMBLES_THRESHOLD):
    value = min(row['forced_fumbles'], max_threshold)
    return 1 / max_threshold * value


def classify_by_total_tackles(row, max_threshold=Units.LB.MAX_TOT_TACKLES_THRESHOLD):
    value = min(row['total_tackles'], max_threshold)
    return 1 / max_threshold * value


def classify_by_assisted_tackles(row, max_threshold=Units.LB.MAX_ASS_TACKLES_THRESHOLD):
    value = min(row['tackles_assist'], max_threshold)
    return 1 / max_threshold * value


def classify_by_solo_tackles(row, max_threshold=Units.LB.MAX_SOLO_TACKLE_THRESHOLD):
    value = min(row['solo_tackles'], max_threshold)
    return 1 / max_threshold * value


def classify_by_tfls(row, max_threshold=Units.DL.MAX_TFL_THRESHOLD):
    value = min(row['tackles_for_loss'], max_threshold)
    return 1 / max_threshold * value


# region Standard classifier sets
def standard_classifiers_wr():
    return [Classifier.BY_TOTAL_YARDS, Classifier.BY_YEARS_IN_NFL, Classifier.BY_TDs, Classifier.BY_RECEPTIONS]


def standard_classifiers_rb():
    return [Classifier.BY_TOTAL_YARDS, Classifier.BY_YEARS_IN_NFL, Classifier.BY_TDs, Classifier.BY_RECEPTIONS]


def standard_classifiers_te():
    return [Classifier.BY_TOTAL_YARDS, Classifier.BY_YEARS_IN_NFL, Classifier.BY_TDs, Classifier.BY_RECEPTIONS]


def standard_classifiers_qb():
    return [Classifier.BY_TOTAL_YARDS, Classifier.BY_YEARS_IN_NFL, Classifier.BY_TDs,  # Classifier.BY_INTERCEPTIONS,
            Classifier.BY_COMPLETIONS]


def standard_classifiers_lb():
    return [Classifier.BY_TOTAL_TACKLES, Classifier.BY_ASSISTED_TACKLES, Classifier.BY_SOLO_TACKLES, Classifier.BY_TFL,
            Classifier.BY_SACKS, Classifier.BY_QB_HITS, Classifier.BY_FORCED_FUMBLES, Classifier.BY_PASS_DEF,
            Classifier.BY_INTERCEPTIONS_CAUGHT, Classifier.BY_YEARS_IN_NFL]


def standard_classifiers_dl():
    return [Classifier.BY_TOTAL_TACKLES, Classifier.BY_ASSISTED_TACKLES, Classifier.BY_SOLO_TACKLES, Classifier.BY_TFL,
            Classifier.BY_SACKS, Classifier.BY_QB_HITS, Classifier.BY_FORCED_FUMBLES, Classifier.BY_YEARS_IN_NFL]


def standard_classifiers_db():
    return [Classifier.BY_TOTAL_TACKLES, Classifier.BY_ASSISTED_TACKLES, Classifier.BY_SOLO_TACKLES, Classifier.BY_TFL,
            Classifier.BY_SACKS, Classifier.BY_FORCED_FUMBLES, Classifier.BY_PASS_DEF,
            Classifier.BY_INTERCEPTIONS_CAUGHT, Classifier.BY_YEARS_IN_NFL]


def convert_to_string_list(classifiers):
    classifier_columns = []
    for cs in classifiers:
        classifier_columns.append(cs.__str__())
    return classifier_columns


# endregion


class Classifier(Enum):
    # General classifiers
    BY_YEARS_IN_NFL = 1

    # Offensive Classifiers
    BY_TOTAL_YARDS = 2
    BY_TDs = 3
    BY_RECEPTIONS = 4
    BY_INTERCEPTIONS = 5
    BY_COMPLETIONS = 6

    # Defensive Classifiers
    BY_TOTAL_TACKLES = 7
    BY_ASSISTED_TACKLES = 8
    BY_SOLO_TACKLES = 9
    BY_TFL = 10
    BY_SACKS = 11
    BY_QB_HITS = 12
    BY_FORCED_FUMBLES = 13
    BY_RECOVERED_FUMBLES = 14
    BY_PASS_DEF = 15
    BY_INTERCEPTIONS_CAUGHT = 16

    def __eq__(self, other):
        if self.value == other:
            return True
        return False

    def __str__(self):
        return 'Classification_' + self.name
