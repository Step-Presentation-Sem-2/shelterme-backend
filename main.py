import os
from fastapi import FastAPI, HTTPException, File, UploadFile
from typing import List
import httpx
import logging
from preprocessingmain import get_image
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile
from typing import List
import shutil
from fastapi.responses import JSONResponse
from prediction_model import PredictionModel

# from fastapi import HTTPException

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("Application is starting...")
    PredictionModel()
    


@app.on_event("shutdown")
async def shutdown_event():
    print("Application is shutting down...")


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def root():
    return {"message": "Hello World"}
'''
@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    probabilities = []
    for file in files:
        try:
            contents = await file.read()  # Use await when reading the file asynchronously
            relative_folder_path = "scraped_images"
            os.makedirs(relative_folder_path, exist_ok=True)
            filename = file.filename.replace(" ", "-")
            file_path = os.path.join(relative_folder_path, filename)

            with open(file_path, "wb+") as f:
                f.write(contents)

            # Call get_image with the file_path
            probability = get_image(file_path, draw_faces=True, conf_score=0.5)  # Adjust conf_score as needed
            probabilities.append(probability)

        except Exception as e:
            print(e)
            return {"message": "There was an error uploading the file(s)"}
        finally:
            file.close()
        if probabilities[0] >= 0.5:
            result="real"
        else:
            result=print("fake")
    return {"message": "The Image uploaded is : "+result}
'''
#This modification reads each uploaded file asynchronously, saves it to a directory, and then calls `get_image` with the file path to obtain the probability. The probabilities are collected into a list and returned along with the success message. Adjust the `conf_score` parameter as needed according to your requirements.
@app.post("/upload/")
async def upload(files: List[UploadFile] = File(...), draw_faces: bool = True, conf_score: float = 0.9):
    try:
        all_predictions = []
        for file in files:
            contents = await file.read()
            relative_folder_path = "scraped_images"
            os.makedirs(relative_folder_path, exist_ok=True)
            filename = file.filename.replace(" ", "-")
            file_path = os.path.join(relative_folder_path, filename)

            with open(file_path, "wb+") as f:
                f.write(contents)
            print(file_path)
            
            # Predictions
            prediction = predict_model(draw_faces, conf_score)
            all_predictions.extend(prediction)

        return {"predictions": all_predictions}
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": "There was an error uploading the file(s)"})


@app.post("/predictmodel")
async def predict_model(draw_faces: bool = True, conf_score: float = 0.9):

    input_folders = ["scraped_images"]
    output_folders = ["preprocessed_images"]
    for input_folder, output_folder in zip(input_folders, output_folders):
        get_image(input_folder, draw_faces, conf_score)

    return {"message": "model trained successfully"}


def predict_model(draw_faces: bool = True, conf_score: float = 0.9):
    all_predictions = []
    input_folders = 'scraped_images'
    output_folders = ["preprocessed_images"]
    #for input_folder, output_folder in zip(input_folders, output_folders):
    value = get_image(input_folders, draw_faces, conf_score)
    print("pred",value[0])
        

@app.get("/healthCheck")
def health_check():
    # response.status_code = HTTP_200_OK
    return {"Healthcheck Success"}


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
