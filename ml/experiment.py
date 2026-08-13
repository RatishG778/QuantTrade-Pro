from ml.trainer import ModelTrainer
from ml.predictor import Predictor
from ml.evaluator import ModelEvaluator


class MLExperiment:

    def __init__(

        self,

        model

    ):

        self.model = model

    def run(

        self,

        X_train,

        X_test,

        y_train,

        y_test

    ):

        trainer = ModelTrainer(

            self.model

        )

        trainer.fit(

            X_train,

            y_train

        )

        predictor = Predictor(

            self.model

        )

        prediction = predictor.predict(

            X_test

        )

        return ModelEvaluator.evaluate(

            y_test,

            prediction

        )