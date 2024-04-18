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
from genericPredictions import makeGenericPredictions
from enums import Questions
import shutil
from fastapi.responses import JSONResponse
from prediction_model import PredictionModel
# from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

# from fastapi import HTTPException
class AllowMixedContentMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        # This CSP allows images, scripts, AJAX, etc., from any URL (including http)
        response.headers['Content-Security-Policy'] = "default-src https: http: data: 'unsafe-inline' 'unsafe-eval'"
        return response
    
app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("Application is starting...")
    PredictionModel()
    


@app.on_event("shutdown")
async def shutdown_event():
    print("Application is shutting down...")


origins = ["*"]
# app.add_middleware(AllowMixedContentMiddleware)
app.add_middleware(
    # AllowMixedContentMiddleware,
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to AuthentiScan"}

#This modification reads each uploaded file asynchronously, saves it to a directory, and 
# then calls `get_image` with the file path to obtain the probability. The probabilities are 
# collected into a list and returned along with the success message. Adjust the `conf_score`
#  parameter as needed according to your requirements.
@app.post("/upload/")
async def upload(files: List[UploadFile] = File(...), draw_faces: bool = True, conf_score: float = 0.9):
    try:
        # Clear existing files in the directory
        folder_path = "scraped_images"
        clean(folder_path)
        all_predictions = []
        for file in files:
            contents = await file.read()
            filename = file.filename.replace(" ", "-")
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "wb") as f:
                f.write(contents)
            print(file_path)
            
            # Predictions
            prediction = predict_model(draw_faces, conf_score)
            print("Preed i upload: ",prediction[0])
            val_prediction=prediction[0]
            all_predictions.extend(prediction)
            print("All_prediction: ", all_predictions)
            return_value = float(all_predictions[0][0])
            print("Return value:",return_value)

        return {return_value}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="There was an error uploading the file(s)")
    
    
def clean(folder_path):
    for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if file_path is not None:
                os.remove(file_path)
    
def predict_model(draw_faces: bool = True, conf_score: float = 0.9):
    all_predictions = []
    input_folders = 'scraped_images'
    output_folders = ["preprocessed_images"]
    #for input_folder, output_folder in zip(input_folders, output_folders):
    value = get_image(input_folders, draw_faces, conf_score)
    print("pred",value[0])
    return value
        

@app.get("/healthCheck")
def health_check():
    # response.status_code = HTTP_200_OK
    return {"Healthcheck Success"}

def getLatestModelFromS3():
    relative_folder_path = "model"
    os.makedirs(relative_folder_path, exist_ok=True)
    

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# Takes values as 'age', 'gender', 'ethnicity', 'eyeColor', 'wrinkles'
@app.post("/genericPredictions")
def genericPredictions(question):
    try:
        # Type checking
        if question not in [member.value for member in Questions] and question not in [member.name for member in Questions]:
            raise TypeError('question must be an instance of Question Enum')
        result = makeGenericPredictions(question)
    except TypeError as e:
        return HTTPException(status_code=404, detail=str(e))
    return {"message": result}

