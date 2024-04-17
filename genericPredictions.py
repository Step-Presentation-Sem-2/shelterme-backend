from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image
import torch
import os

def makeGenericPredictions(question):
    
    folder_path = "scraped_images"
    for filename in os.listdir(folder_path):
        if os.path.isfile(os.path.join(folder_path, filename)):
            try:
                image = Image.open(os.path.join(folder_path, filename))
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    if question == 'AGE' or question == 'age':
        text = f"What is the age of the person in the image?"
        result = run_inference(image, text)
        print(result)
    if question == 'GENDER' or question == 'gender':
        text = f"What is the gender of the person in the image?"
        result = run_inference(image, text)
        print(result)
    if question == 'ETHNICITY' or question == 'ethnicity':
        text = f"What is the ethnicity of the person in the image?"
        result = run_inference(image, text)
        print(result)
    if question == 'EYECOLOR' or question == 'eyeColor':
        text = f"What is the eyecolor of the person in the image?"
        result = run_inference(image, text)
        print(result)
    if question == 'WRINKLES' or question == 'wrinkles':
        text = f"Does the person in the image have wrinkles?"
        result = run_inference(image, text)
        print(result)
    return result

def run_inference(image, text):
    model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

    inputs = processor(image, text, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    idx = logits.argmax(-1).item()
    return  model.config.id2label[idx]
