from sklearn.ensemble import RandomForestClassifier


class MLTrainer:

    def __init__(self, random_state=42):

        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            random_state=random_state
        )

    def train(self, X, y):

        self.model.fit(X, y)

        return self.model

    def predict(self, X):

        return self.model.predict(X)

    def predict_proba(self, X):

        return self.model.predict_proba(X)