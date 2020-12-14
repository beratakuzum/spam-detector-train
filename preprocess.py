import pandas as pd

from sklearn.preprocessing import LabelEncoder


def binarize_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    le = LabelEncoder()
    for category in columns:
        df[category] = le.fit_transform(df[category])

    return df


def split_features_and_labels(features_and_labels_df: pd.DataFrame):
    labels_df = features_and_labels_df[['is_spam']]
    features_df = features_and_labels_df.drop('is_spam', 1)

    return labels_df, features_df


def encode_country_values(features_df: pd.DataFrame) -> pd.DataFrame:
    features_df = pd.concat((features_df, pd.get_dummies(features_df.country)), 1)
    features_df = features_df.drop('country', 1)

    return features_df
