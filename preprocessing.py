import numpy as np
from keras import backend as kb
from PIL import Image
import config as cg
import os

def preprocess_input(x, data_format=None):
    # resize and convert to numpy
    x_resized = x.resize((224, 224), Image.BILINEAR)
    x_temp = np.copy(np.array(x_resized).astype(np.float64))

    if data_format is None:
        data_format = kb.image_data_format()
    assert data_format in {'channels_last', 'channels_first'}

    if data_format == 'channels_first':
        x_temp = x_temp[:, ::-1, ...]
        x_temp[:, 0, :, :] -= 91.4953
        x_temp[:, 1, :, :] -= 103.8827
        x_temp[:, 2, :, :] -= 131.0912
    else:
        x_temp = x_temp[..., ::-1]
        x_temp[..., 0] -= 91.4953
        x_temp[..., 1] -= 103.8827
        x_temp[..., 2] -= 131.0912

    return np.expand_dims(x_temp, axis=0)
