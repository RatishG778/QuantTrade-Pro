import pandas as pd
from sklearn.model_selection import train_test_split


class DatasetBuilder:

    def __init__(self, data):

        self.data = data.copy()

    def classification_dataset(
        self,
        features,
        target="Target",
        test_size=0.2,
        shuffle=False
    ):

        df = self.data.dropna()

        X = df[features]

        y = df[target]

        return train_test_split(
            X,
            y,
            test_size=test_size,
            shuffle=shuffle
        )
    