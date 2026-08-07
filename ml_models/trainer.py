class ModelTrainer:

    def __init__(self, model):

        self.model = model

    def fit(

        self,

        X_train,

        y_train

    ):

        self.model.train(

            X_train,

            y_train

        )

        return self.model