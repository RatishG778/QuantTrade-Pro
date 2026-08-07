class WalkForwardSplitter:

    def split(

        self,

        data,

        train_size=500,

        test_size=100,

        step=100

    ):

        windows = []

        start = 0

        while start + train_size + test_size <= len(data):

            train = data.iloc[

                start:

                start + train_size

            ]

            test = data.iloc[

                start + train_size:

                start + train_size + test_size

            ]

            windows.append(

                (

                    train,

                    test

                )

            )

            start += step

        return windows