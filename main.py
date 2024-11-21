from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware
from evaluatorTool.evaluator import process_image

app = FastAPI()

# Updated CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process_image/")
async def process_uploaded_image(file: UploadFile = File(...)):
    """
    Process uploaded image and return JSON result
    """
    temp_file_path = f"temp_{file.filename}"
    try:
        # Save uploaded file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process the image
        processed_result = process_image(temp_file_path)
        
        # Debug logging
        print(f"Processed result type: {type(processed_result)}")
        print(f"Processed result content: {processed_result}")

        if processed_result is None:
            return JSONResponse(
                status_code=500,
                content={"error": "Failed to process image - null result"},
                headers={"Content-Type": "application/json"}
            )

        # Return successful response
        response_data = {"foods": processed_result}
        print(f"Sending response: {response_data}")
        
        return JSONResponse(
            content=response_data,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        )

    except Exception as e:
        print(f"Server error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
            headers={"Content-Type": "application/json"}
        )

    finally:
        # Cleanup
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)