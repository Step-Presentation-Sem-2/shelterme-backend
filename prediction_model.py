def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class PredictionModel:
    def __init__(self):
        # initialize model here
        self.model = "model"

    def get_model(self):
        return self.model
