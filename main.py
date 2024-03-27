import os
from fastapi import FastAPI, HTTPException,File, UploadFile
import httpx
import logging
from typing import List

from pydantic import BaseModel
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

@app.get("/healthCheck")
async def health_check():
    
    external_url = "/healthCheck"
    external_response = await make_external_request(external_url)

    
    return {"internal_status": "Server response: OK - all good", "external_response": external_response.json()}


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
