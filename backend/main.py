from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import uuid
from chains import run_image_story_graph

app = FastAPI()

# CORS 설정 (개발용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate_story/")
async def generate_story(
    image: UploadFile,
    user_input: str = Form(...),
    genre: str = Form(...)
):
    temp_filename = f"temp_images/{uuid.uuid4().hex}_{image.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    result = run_image_story_graph(image_path=temp_filename, user_input=user_input, genre=genre)

    return JSONResponse({
        "image_caption": result["image_caption"],
        "story": result["story"],
        "reflection": result["reflection"]
    })
