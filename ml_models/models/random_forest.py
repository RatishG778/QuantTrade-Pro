from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from ml_models.models.base_model import BaseModel


class RandomForestModel(BaseModel):

    def __init__(self):

        self.model = RandomForestClassifier(

            n_estimators=200,

            random_state=42

        )

    def train(

        self,

        X_train,

        y_train

    ):

        self.model.fit(

            X_train,

            y_train

        )

    def predict(self, X):

        return self.model.predict(X)

    def evaluate(

        self,

        X_test,

        y_test

    ):

        prediction = self.predict(X_test)

        return accuracy_score(

            y_test,

            prediction

        )