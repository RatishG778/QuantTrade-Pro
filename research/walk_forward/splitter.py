class WalkForwardSplitter:

    def split(
        self,
        data,
        train_size=0.70
    ):

        split_index = int(
            len(data) * train_size
        )

        train = data.iloc[:split_index]

        test = data.iloc[split_index:]

        return train, test