import numpy as np
import mtcnn
from PIL import Image, ImageDraw
import argparse
import os


def detect_faces(image_path):
    """
    Detect faces in an image using MTCNN.

    Args:
        image_path (str): Path to the image file.

    Returns:
        image: An Image object.
        faces: A list of dictionaries containing details of the detected faces.
    """
    try:
        face_detector = mtcnn.MTCNN()
        image = Image.open(image_path)
        image = image.convert("RGB")
        faces = face_detector.detect_faces(np.array(image))
        return image, faces
    except:
        return None, None

def draw_faces(image, faces, image_path, conf_score, show_image=False, save_cropped=False, save_uncropped=False, save_image_path=None):
    """
    Draw bounding boxes and keypoints on the detected faces. Optionally, show the image, save the image with drawn faces,
    and save the cropped faces.

    Args:
        image: An Image object.
        faces: A list of dictionaries containing details of the detected faces.
        image_path (str): Path to the image file.
        conf_score (float): Confidence score threshold for face detection.
        show_image (bool): Flag to control the display of the image with drawn faces.
        save_cropped (bool): Flag to control the saving of the cropped faces.
        save_uncropped (bool): Flag to control the saving of the image with drawn faces.
        save_image_path (str): Path to save the image with drawn faces.
    """
    croped_img_path = None
    draw = ImageDraw.Draw(image)

    for i, face in enumerate(faces):
        box = face["box"]
        conf = round(face["confidence"], 2)
        # print(conf)
        if conf >= conf_score:
            # Save individual faces cropped image here before face detection box is drawn on the image
            if save_cropped:
                cropped_face = image.crop((box[0], box[1], box[0] + box[2], box[1] + box[3]))
                _, tail = os.path.split(image_path)
                if save_image_path is None:
                    cropped_face.save(fp=f'fd_cropped_{i}_{tail}')
                else:
                   #croped_img_path=os.path.join(save_image_path, f'fd_cropped_{i}_{tail}')
                   croped_img_path = os.path.join(save_image_path, f'fd_cropped_{i}_{tail}')
                   #cropped_face.save(fp=os.path.join(save_image_path, f'fd_cropped_{i}_{tail}'))
                   cropped_face.save(fp=croped_img_path)
                   print("Cropped face image saved at:", croped_img_path)

            if not save_cropped:
                keypoints = face["keypoints"]
                draw.rectangle(
                    [(box[0], box[1]), (box[0] + box[2], box[1] + box[3])], outline="green"
                )
                draw.text((box[0], box[1] - 10), "Confidence Score: " + str(conf), fill="red")
                for keypoint in keypoints.values():
                    draw.ellipse(
                        (keypoint[0] - 2, keypoint[1] - 2, keypoint[0] + 2, keypoint[1] + 2),
                        fill="red",
                    )

    if show_image:
        image.show()

    # only makes sense to save one uncropped image with all the faces drawn on the image
    if save_uncropped:
        _, tail = os.path.split(image_path)
        '''  if save_image_path is None:
            image.save(fp=f'fd_uncropped_{tail}')
        else:
            image.save(fp=os.path.join(save_image_path, f'fd_uncropped_{tail}'))
            '''
    return croped_img_path





def face_detection(image_path, draw_faces_flag, conf_score, show_image, save_cropped, save_uncropped, save_image_path=None):
    """
    Main function to detect and draw faces on an image.

    Args:
        image_path (str): Path to the image file.
        draw_faces_flag (bool): Flag to control the activation of the draw_faces function.
        conf_score (float): Confidence score threshold for face detection.
        show_image (bool): Flag to control the display of the image with drawn faces.
        save_cropped (bool): Flag to control the saving of the cropped faces.
        save_uncropped (bool): Flag to control the saving of the image with drawn faces.
        save_image_path (str): Path to save the image with drawn faces.
    """
    image, faces = detect_faces(image_path)
    if draw_faces_flag and image is not None:
        croped_img_path= draw_faces(image, faces, image_path, conf_score, show_image, save_cropped, save_uncropped, save_image_path)
        print("line 108: ",croped_img_path)
    return croped_img_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect and draw faces on an image.")
    parser.add_argument("-i", "--image_path", type=str, help="Path to the image file.")
    parser.add_argument("-c", "--conf_score", type=float, default=0.9, help="Confidence score threshold for face detection. A value between 0-1")
    parser.add_argument("-d", "--draw_faces", action="store_true",
                        help="Flag to control the activation of the draw_faces function.")
    parser.add_argument("-s", "--show_image", action="store_true",
                        help="Flag to control the display of the image with drawn faces.")
    parser.add_argument("-p", "--save_cropped", action="store_true",
                        help="Flag to control the saving of the cropped faces.")
    parser.add_argument("-u", "--save_uncropped", action="store_true",
                        help="Flag to control the saving of the image with drawn faces.")
    parser.add_argument("-o", "--save_image_path", type=str,
                        help="Path to save the image with drawn faces.")
    args = parser.parse_args()
    face_detection(args.image_path, args.draw_faces, args.conf_score, args.show_image, args.save_cropped, args.save_uncropped, args.save_image_path)
