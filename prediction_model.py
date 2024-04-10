from tensorflow.keras.models import load_model
import os

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
        #model_name ='model_1708578202.keras'
        model_path = os.path.join(os.getcwd(), "model_1708578202.keras")
        self.model = load_model(model_path)
        print('model is initialized')
        
    def get_prediction(self, input):
        return self.model.predict(input)

    def get_model(self):
        return self.model
