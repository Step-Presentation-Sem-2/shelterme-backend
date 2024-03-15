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
def upload(files: List[UploadFile] = File(...)):
    try:
        if os.path.isdir('images') != True:
            os.mkdir("images")
        print(os.getcwd())
    except Exception as e:
        print(e)
    
    for file in files:
        try:
            contents = file.file.read()
            file_name = os.getcwd()+"/images/"+file.filename.replace(" ", "-")
            print(file_name)
            with open(file_name, 'wb+') as f:
                f.write(contents)
            
        except Exception as e:
            print(e)
            return {"message": "There was an error uploading the file(s)"}
        finally:
            file.file.close()

    return {"message": f"Successfully uploaded {[file.filename for file in files]}"}

async def make_external_request(url, data=None):
    async with httpx.AsyncClient() as client:
        try:
            if data:
                response = await client.post(url, json=data)
            else:
                response = await client.get(url)
            response.raise_for_status()  
            return response
        except httpx.RequestError as exc:
            
            raise HTTPException(status_code=500, detail=f"Error making external request: {exc}")
        except httpx.HTTPStatusError as exc:
            
            raise HTTPException(status_code=exc.response.status_code, detail=f"External request failed: {exc}")

@app.post("/realityCheck")
async def reality_check(imageurl: str):
    
    external_url = "/realityCheck"
    external_response = await make_external_request(external_url, {"imageurl": imageurl})

   
    probability = 0.75  
    return {"internal_probability": probability, "external_response": external_response.json()}

UPLOAD_FOLDER = "C:/Users/jini/Desktop/authentiScan-latest/shelterme-backend/images"

@app.post("/generateAiImage")
async def generate_ai_image():
   
    input_folders = ['scraped_images/scraped_images_b1','scraped_images/ai_generated_images_b1']
    output_folders = ['preprocessed_images/processed_real_images_b1','preprocessed_images/processed_ai_images_b1']
    for input_folder, output_folder in zip(input_folders,output_folders):
        get_image(input_folder,output_folder)
    
    return {"message": "Fake image generated and model trained successfully"}

@app.get("/healthCheck")
def health_check():
    # response.status_code = HTTP_200_OK
    return {"Healthcheck Success"}

@app.post("/matchImageMeta")
async def match_image_meta(meta_data: dict):
    
    external_url = "/matchImageMeta"
    external_response = await make_external_request(external_url, {"meta_data": meta_data})

    
    return {"message": "Image meta data saved successfully", "external_response": external_response.json()}



# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Testing methods will remove in future


@app.get("/fetch_data")
async def fetch_data():
    url = "https://jsonplaceholder.typicode.com/posts"  # Example endpoint from JSONPlaceholder

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        data = response.json()
        return {"data": data}
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")

@app.get("/fetch_post_data/{post_id}")
async def fetch_post_data(post_id: int):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        data = response.json()
        return {"post_data": data}
    else:
        error_detail = f"Failed to fetch post data. Server returned status code {response.status_code}."
        raise HTTPException(status_code=response.status_code, detail=error_detail)




class PostPayload(BaseModel):
    title: str
    body: str
    userId: int

@app.post("/create_post")
async def create_post(payload: PostPayload):
    url = "https://jsonplaceholder.typicode.com/posts"
    payload_json = payload.json()

    logging.info(f"Sending request to {url} with payload: {payload_json}")

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload_json)

    logging.info(f"Received response: {response.status_code} - {response.text}")

    if response.status_code == 201:
        data = response.json()
        return {"post_created": data}
    else:
        error_detail = f"Failed to create post. Server returned status code {response.status_code}."
        raise HTTPException(status_code=response.status_code, detail=error_detail)


# Testing methods end
