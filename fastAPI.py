# Install dependencies: pip install fastapi uvicorn python-multipart


from fastapi import FastAPI, File, UploadFile
import shutil

app = FastAPI()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Save the file to a temporary directory or process it directly
    with open(f"uploaded_{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}
