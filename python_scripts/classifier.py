from enum import Enum
import utils.unit_keys as Units


# Classify players by all the given classifiers combined
def classify_dataframe(data, classifiers, unit=Units.WR):
    data['Classification_All'] = data.apply(axis=1, func=lambda x: classify_row(x, classifiers, unit))


def classify_by_single_classifier(data, classifiers, unit=Units.WR):
    for classifier in classifiers:
        data[classifier.__str__()] = data.apply(axis=1, func=lambda x: classify_row(x, [classifier], unit))

    # data['Classification_YearsInNFL'] = data.apply(axis=1, func=lambda x: classify_row(x, Classifier.BY_YEARS_IN_NFL))
    # data['Classification_Total_Yards'] = data.apply(axis=1, func=lambda x: classify_row(x, Classifier.BY_TOTAL_YARDS))


def classify_row(row, classifiers, unit):
    if len(classifiers) == 0:
        return 'Good'

    classification_threshold = 0.5
    if unit == Units.QB:
        classification_threshold = 0.4

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

    if result / len(classifiers) >= classification_threshold:
        return 'Good'
    else:
        return 'Bust'


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


def convert_to_string_list(classifiers):
    classifier_columns = []
    for cs in classifiers:
        classifier_columns.append(cs.__str__())
    return classifier_columns

# endregion


class Classifier(Enum):
    BY_YEARS_IN_NFL = 1
    BY_TOTAL_YARDS = 2
    BY_TDs = 3
    BY_RECEPTIONS = 4
    BY_INTERCEPTIONS = 5
    BY_COMPLETIONS = 6

    def __eq__(self, other):
        if self.value == other:
            return True
        return False

    def __str__(self):
        return 'Classification_' + self.name
