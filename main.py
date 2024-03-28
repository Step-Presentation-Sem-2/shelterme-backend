import os
from fastapi import FastAPI, HTTPException, File, UploadFile
from typing import List
import httpx
import logging
from preprocessingmain import get_image
from pydantic import BaseModel
from fastapi import File, UploadFile
from typing import List
import shutil
#from fastapi import HTTPException

app = FastAPI()

async def root():
    return {"message": "Hello World"}

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    for file in files:
        try:
            contents = await file.read()  # Use await when reading the file asynchronously
            relative_folder_path = "scraped_images/ai_generated_images_b1"
            os.makedirs(relative_folder_path, exist_ok=True)
            filename = file.filename.replace(" ", "-")
            file_path = os.path.join(relative_folder_path, filename)

            
            with open(file_path, 'wb+') as f:
                f.write(contents)
            
        except Exception as e:
            print(e)
            return {"message": "There was an error uploading the file(s)"}
        finally:
            file.close() 
    return {"message": f"Successfully uploaded {[file.filename for file in files]}"}

'''   
@app.post("/facedetection")
def face_detection(imageFileName: str):
    
    external_url = "/realityCheck"
    # external_response = await make_external_request(external_url, {"imageurl": imageurl})

    # NEED TO UPDATE
    external_response = null
   
    probability = 0.75  
    return {"internal_probability": probability, "external_response": external_response.json()}

UPLOAD_FOLDER = "C:/Users/jini/Desktop/authentiScan-latest/shelterme-backend/images"
'''
@app.post("/predictmodel")
async def predict_model():
   
    input_folders = ['scraped_images/scraped_images_b1','scraped_images/ai_generated_images_b1']
    output_folders = ['preprocessed_images/processed_real_images_b1','preprocessed_images/processed_ai_images_b1']
    for input_folder, output_folder in zip(input_folders,output_folders):
        get_image(input_folder,output_folder)
    
    return {"message": "model trained successfully"}

@app.get("/healthCheck")
def health_check():
    # response.status_code = HTTP_200_OK
    return {"Healthcheck Success"}

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
