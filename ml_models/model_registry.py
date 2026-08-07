from ml_models.models.random_forest import RandomForestModel


class ModelRegistry:

    MODELS = {

        "Random Forest": RandomForestModel,

    }

    @classmethod
    def get_model(cls, name):

        if name not in cls.MODELS:

            raise ValueError(f"Unknown model: {name}")

        return cls.MODELS[name]()