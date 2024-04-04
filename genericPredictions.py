# from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image
# import torch

def makeGenericPredictions(question):
    # model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
    # processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

    # test = Image.open("iu-perfect-face-v0-2kawyvlr8y1c1.jpg")

    if question == 'AGE' or question == 'age':
        text = f"What is the age of the person in the image?"
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