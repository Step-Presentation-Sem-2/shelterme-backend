# from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image
# import torch
import os

def makeGenericPredictions(question):
    # model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    # processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

    inputFolder = 'scraped_images'
    for filename in os.listdir(inputFolder):
        if os.path.isfile(os.path.join(inputFolder, filename)):
            print(filename)
    test = Image.open("scraped_images/iu-perfect-face-v0-2kawyvlr8y1c1.jpg")

    if question == 'AGE' or question == 'age':
        text = f"What is the age of the person in the image?"
        # result = run_inference(test, text)
        print(text)
    if question == 'GENDER' or question == 'gender':
        text = f"What is the gender of the person in the image?"
        # result = run_inference(test, text)
        print(text)
    if question == 'ETHNICITY' or question == 'ethnicity':
        text = f"What is the ethnicity of the person in the image?"
        # result = run_inference(test, text)
        print(text)
    if question == 'EYECOLOR' or question == 'eyeColor':
        text = f"What is the eyecolor of the person in the image?"
        # result = run_inference(test, text)
        print(text)
    if question == 'WRINKLES' or question == 'wrinkles':
        text = f"Does the person in the image have wrinkles?"
        # result = run_inference(test, text)
        print(text)

# def run_inference(image, text):
#     # Preprocessing
#     inputs = processor(image, text, return_tensors="pt")

#     # Inference
#     with torch.no_grad():
#         outputs = model(**inputs)
    
#     logits = outputs.logits
#     idx = logits.argmax(-1).item()
#     return  model.config.id2label[idx]