from ml_models.model_registry import ModelRegistry

model = ModelRegistry.get_model("Random Forest")

print(type(model).__name__)