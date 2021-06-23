"""
The Levenshtein distance is a string metric for measuring the difference
between two sequences. It is calculated as the minimum number of single-character edits necessary to
transform one string into another.

"""

import pandas as pd
import itertools
import numpy as np
from Levenshtein import distance

# Read data
link_ad = 'https://data.stadt-zuerich.ch/dataset/sid_stapo_hundenamen/download/20210103_hundenamen.csv'
data = pd.read_csv(link_ad)


def data_cleansing(df):
    """
    -remove parenthesis and string within
    -extract and keep between quotes
    """
    # Remove if contains
    df_ = df.copy()
    df_ = df_[~df_['HUNDENAME'].str.contains("unbekannt")]
    # Remove content in parenthesis
    df_['HUNDENAME'] = df_['HUNDENAME'].str.replace(r"\(.*\)", "")
    # Keep only text within quotes
    within_quotes = df_['HUNDENAME'].str.extract(r"\"([A-Za-z]+)\"")
    last = pd.DataFrame(np.where(within_quotes.isnull(), df_[['HUNDENAME']], within_quotes),
                        index=within_quotes.index,
                        columns=within_quotes.columns)
    dog_ls = last[0].unique()
    return dog_ls


def levenshtein_dog_names(names):
    name = []
    distance_s = []
    for i, j in zip(names, itertools.repeat('Luca')):
        name.append(i)
        distance_s.append(distance(i, j))
    score_df = pd.DataFrame({'name': name, 'distance': distance_s})
    n = score_df['name'].loc[score_df.distance == 1]
    print(n.unique())


if __name__ == '__main__':
    dog_names = data_cleansing(data)
    levenshtein_dog_names(dog_names)

