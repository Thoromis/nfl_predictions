from enum import Enum


# Classify players by all the given classifiers combined
def classify_dataframe(data, classifiers):
    data['Classification_All'] = data.apply(axis=1, func=lambda x: classify_row(x, classifiers))


def classify_by_single_classifier(data, classifiers):
    for classifier in classifiers:
        data['Classification' + classifier.name] = data.apply(axis=1, func=lambda x: classify_row(x, [classifier]))

    # data['Classification_YearsInNFL'] = data.apply(axis=1, func=lambda x: classify_row(x, Classifier.BY_YEARS_IN_NFL))
    # data['Classification_Total_Yards'] = data.apply(axis=1, func=lambda x: classify_row(x, Classifier.BY_TOTAL_YARDS))


def classify_row(row, classifiers):
    if len(classifiers) == 0:
        return 'Good'

    result = 0
    for classifier in classifiers:
        if classifier == Classifier.BY_YEARS_IN_NFL:  # isinstance(Classifier.BY_YEARS_IN_NFL, classifier):
            result += classify_by_time(row)
        elif classifier == Classifier.BY_TOTAL_YARDS:  # isinstance(Classifier.BY_TOTAL_YARDS, classifier):
            result += classify_by_total_yards(row)
        elif classifier == Classifier.BY_YARDS_PER_GAME:  # isinstance(Classifier.BY_YARDS_PER_GAME, classifier):
            result += classify_by_ypg(row)

    if result / len(classifiers) >= 0.5:
        return 'Good'
    else:
        return 'Bust'


# data not here yet.
def classify_by_ypg(row):
    return 1


# Classify by time spent in the NFL, maximum achievable time is set to 10 [years].
# Becomes less relative to this 10 year threshold, 10 years ==> 1, 1 year ==> 0.1
def classify_by_time(row):
    max_season_threshold = 10
    value = min(row['season_helper'], max_season_threshold)

    return 1 / max_season_threshold * value


def classify_by_total_yards(row):
    max_yard_threshold = 10000
    value = min(row['Total_Yards'], max_yard_threshold)

    return 1 / max_yard_threshold * value


# region Standard classifier sets
def standard_classifiers_wr():
    return [Classifier.BY_TOTAL_YARDS, Classifier.BY_YEARS_IN_NFL]


# endregion


class Classifier(Enum):
    BY_YEARS_IN_NFL = 1
    BY_TOTAL_YARDS = 2
    BY_YARDS_PER_GAME = 3

    def __eq__(self, other):
        if self.value == other:
            return True
        return False
