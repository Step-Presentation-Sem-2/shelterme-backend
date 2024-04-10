from preprocessing import preprocess_input
import os
from PIL import Image
import numpy as np
from face_detection import face_detection
import argparse
from tensorflow.keras.models import load_model
from prediction_model import PredictionModel


def get_image(input_directory_path, draw_face, conf_score):
    """
    Process all images within the specified directory.
    Reads each file or image from the input directory path and then creates the image path
    image path is the path of the directory + that of the image
    passes the image path with the output size for the resizing and the directory to save the preprocessed images
    """
    predictions = []
    croped_face = 'cropped_image'
    for filename in os.listdir(input_directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(input_directory_path, filename)
            print(image_path)

            # Call face_detection function here
            cropped_face_path = face_detection(image_path, draw_face, conf_score, show_image=False,
                                               save_cropped=True, save_uncropped=True, save_image_path=croped_face)
            print("Cropped image:", cropped_face_path)
            image = Image.open(cropped_face_path)
            # image = image.resize(output_size)     # Load and resize the image
            image_np = np.array(image, dtype=np.float32)

            # model = load_model("C:/Users/jini/Downloads/model_1708578202 (1).keras")
            # model = models.load_model("C:/Users/jini/Downloads/model_1708578202 (1).keras")

            # processed_array = preprocess_input(image_np, data_format= None)
            input_data = preprocess_input(image)

            '''if not os.path.exists(output_directory_path): os.makedirs(output_directory_path)
            # Save the processed image
            image_name = os.path.basename(image_path)
            save_path = os.path.join(output_directory_path, image_name)
            Image.fromarray(np.clip(input_data, 0, 255).astype('uint8')).save(save_path)

            print(f"Processed image saved to: {save_path}")
            
            # Run inference
            predictions = model.predict(input_data)

            if predictions[0] >= 0.5:
                print("real")
            else:
                print("fake")
            '''
            predictions.append(PredictionModel().get_prediction(input_data)[0])
            if predictions[-1] >= 0.5:
                print("Real")
            else:
                print("Fake")
    return predictions
