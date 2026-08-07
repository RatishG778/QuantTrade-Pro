from sklearn.metrics import (

    accuracy_score,

    precision_score,

    recall_score,

    f1_score

)


class ModelEvaluator:

    @staticmethod
    def evaluate(

        y_true,

        prediction

    ):

        return {

            "accuracy":

            accuracy_score(

                y_true,

                prediction

            ),

            "precision":

            precision_score(

                y_true,

                prediction

            ),

            "recall":

            recall_score(

                y_true,

                prediction

            ),

            "f1":

            f1_score(

                y_true,

                prediction

            )

        }